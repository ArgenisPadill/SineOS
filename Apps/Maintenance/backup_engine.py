#!/usr/bin/env python3

import json
import os
import sqlite3
import shutil
import stat
import subprocess
import time
from datetime import datetime
from pathlib import Path


APP_FILE = Path(__file__).resolve()
REPO_ROOT = APP_FILE.parents[2]


class BackupError(RuntimeError):
    pass


def run(command, timeout=30, cwd=None, env=None):
    try:
        return subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False, cwd=str(cwd) if cwd else None, env=env)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise BackupError(str(exc)) from exc


def git_remote_env():
    env = dict(os.environ)
    runtime_dir = Path(
        env.get("XDG_RUNTIME_DIR") or f"/run/user/{os.getuid()}"
    )
    gcr_socket = runtime_dir / "gcr" / "ssh"

    if gcr_socket.exists():
        env["SSH_AUTH_SOCK"] = str(gcr_socket)

    env["GIT_TERMINAL_PROMPT"] = "0"
    env["SSH_ASKPASS_REQUIRE"] = "never"
    env["GIT_SSH_COMMAND"] = "ssh -o BatchMode=yes"

    return env


def build_tag(moment=None):
    moment = moment or datetime.now()
    return f"SineOsBackups-{moment.strftime('%d%m%y-%H%M')}"


def normalize_source(source):
    return source.split("[", 1)[0].strip()


def physical_disk(device):
    result = run(["lsblk", "-no", "PKNAME", device])
    if result.returncode != 0:
        raise BackupError("No se pudo identificar el disco físico.")
    parent = result.stdout.strip().splitlines()
    return f"/dev/{parent[0]}" if parent and parent[0] else device


def root_disk():
    result = run(["findmnt", "-no", "SOURCE", "/"])
    if result.returncode != 0 or not result.stdout.strip():
        raise BackupError("No se pudo identificar el dispositivo raíz.")
    source = normalize_source(result.stdout.strip())
    return physical_disk(source)


def validate_password_file(path=None):
    password = Path(path or "~/.config/sineos/restic-password").expanduser()
    if not password.is_file():
        raise BackupError("No existe la credencial de Restic.")
    info = password.stat()
    if stat.S_IMODE(info.st_mode) != 0o600:
        raise BackupError("La credencial de Restic debe tener permisos 600.")
    if info.st_uid != os.getuid():
        raise BackupError("La credencial de Restic no pertenece al usuario actual.")
    return password


def validate_tools():
    required = ("restic", "findmnt", "lsblk", "git", "podman", "sha256sum")
    missing = [name for name in required if shutil.which(name) is None]
    if missing:
        raise BackupError("Faltan herramientas requeridas: " + ", ".join(missing))
    return required


def validate_target(root):
    if not root:
        raise BackupError("SINEOS_BACKUP_ROOT no está configurado.")
    target = Path(root).expanduser()
    if target.name != "SineOsBackups":
        raise BackupError("El destino debe terminar exactamente en SineOsBackups.")
    if not target.is_dir():
        raise BackupError("El destino externo no está conectado o montado.")
    return target


def mount_information(target):
    result = run(["findmnt", "-no", "SOURCE,FSTYPE,OPTIONS,TARGET", "-T", str(target)])
    if result.returncode != 0 or not result.stdout.strip():
        raise BackupError("No se pudo identificar el montaje del destino externo.")

    parts = result.stdout.strip().split(None, 3)
    if len(parts) != 4:
        raise BackupError("La información de montaje del destino es incompleta.")

    return {
        "source": normalize_source(parts[0]),
        "fstype": parts[1],
        "options": parts[2].split(","),
        "target": parts[3],
    }


def block_value(device, field):
    result = run(["lsblk", "-dn", "-o", field, device])
    if result.returncode != 0:
        raise BackupError(f"No se pudo consultar {field} de {device}.")
    return result.stdout.strip()


def validate_identity(source, backup_disk, expected_uuid, expected_serial):
    if not expected_uuid or not expected_serial:
        raise BackupError("Falta configurar UUID o serial del disco de backup.")

    actual_uuid = block_value(source, "UUID")
    actual_serial = block_value(backup_disk, "SERIAL")

    if actual_uuid != expected_uuid:
        raise BackupError(
            f"UUID del destino inesperado: {actual_uuid or 'vacío'}."
        )

    if actual_serial != expected_serial:
        raise BackupError(
            f"Serial del disco inesperado: {actual_serial or 'vacío'}."
        )

    return {
        "uuid": actual_uuid,
        "serial": actual_serial,
    }


def validate_repository(root, password_file, expected_repository_id):
    required = ("config", "data", "index", "keys", "snapshots")
    missing = [name for name in required if not (root / name).exists()]
    if missing:
        raise BackupError("Repositorio Restic incompleto: " + ", ".join(missing))

    result = run([
        "restic",
        "-r", str(root),
        "--password-file", str(password_file),
        "--no-lock",
        "snapshots",
        "--latest", "1",
    ], timeout=60)

    if result.returncode != 0:
        raise BackupError(
            result.stderr.strip()
            or result.stdout.strip()
            or "No se pudo abrir el repositorio Restic."
        )

    if not expected_repository_id:
        raise BackupError("Falta configurar el ID del repositorio Restic.")

    config_result = run([
        "restic",
        "-r", str(root),
        "--password-file", str(password_file),
        "--no-lock",
        "cat", "config",
    ], timeout=60)

    if config_result.returncode != 0:
        raise BackupError(
            config_result.stderr.strip()
            or config_result.stdout.strip()
            or "No se pudo leer la identidad del repositorio Restic."
        )

    try:
        repository_id = json.loads(config_result.stdout)["id"]
    except (json.JSONDecodeError, KeyError, TypeError):
        raise BackupError("El repositorio Restic no devolvió un ID válido.")

    if repository_id != expected_repository_id:
        raise BackupError(
            f"ID de repositorio Restic inesperado: {repository_id}."
        )

    return repository_id


def preflight(*, root, expected_uuid=None, expected_serial=None, expected_repository_id=None, require_writable=False):
    validate_tools()
    target = validate_target(root)
    password = validate_password_file()

    mount = mount_information(target)
    source = mount["source"]

    if not source.startswith("/dev/"):
        raise BackupError("El destino no está respaldado por un dispositivo de bloques local.")

    backup_disk = physical_disk(source)
    system_disk = root_disk()

    if backup_disk == system_disk:
        raise BackupError("El destino de backup está en el mismo disco físico que el sistema.")

    identity = validate_identity(source, backup_disk, expected_uuid, expected_serial)

    if require_writable and "rw" not in mount["options"]:
        raise BackupError("El destino externo está montado solo lectura.")

    repository_id = validate_repository(target, password, expected_repository_id)

    return {
        "root": str(target),
        "source": source,
        "fstype": mount["fstype"],
        "mountpoint": mount["target"],
        "writable": "rw" in mount["options"],
        "backup_disk": backup_disk,
        "system_disk": system_disk,
        "uuid": identity["uuid"],
        "serial": identity["serial"],
        "repository_id": repository_id,
        "password_file": str(password),
    }


def run_to_file(command, destination, timeout=120):
    try:
        with destination.open("wb") as handle:
            result = subprocess.run(
                command,
                stdout=handle,
                stderr=subprocess.PIPE,
                timeout=timeout,
                check=False,
            )
    except (OSError, subprocess.TimeoutExpired) as exc:
        destination.unlink(missing_ok=True)
        raise BackupError(str(exc)) from exc

    if result.returncode != 0:
        destination.unlink(missing_ok=True)
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise BackupError(message or "Falló la generación del archivo.")

    return destination


def postgres_state(container):
    result = run([
        "podman", "inspect", container,
        "--format", "{{.State.Status}}",
    ])
    if result.returncode != 0:
        raise BackupError(
            result.stderr.strip()
            or f"No se pudo consultar {container}."
        )
    return result.stdout.strip()


def wait_postgres(container, db_user, db_name, attempts=30):
    for _ in range(attempts):
        result = run([
            "podman", "exec", container,
            "pg_isready",
            "-U", db_user,
            "-d", db_name,
        ], timeout=5)
        if result.returncode == 0:
            return True
        time.sleep(1)

    raise BackupError("PostgreSQL no quedó disponible a tiempo.")


def create_postgres_staging(
    container="sineos-postgres",
    db_user="sineos",
    db_name="sineos",
    staging_root=None,
):
    root = Path(
        staging_root
        or "~/.local/state/sineos/backup/staging"
    ).expanduser()

    root.mkdir(parents=True, exist_ok=True)
    os.chmod(root, 0o700)

    original_state = postgres_state(container)
    if original_state not in ("running", "exited"):
        raise BackupError(
            f"Estado PostgreSQL no soportado: {original_state}."
        )

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    staging = root / f"postgresql-{stamp}"
    staging.mkdir(mode=0o700)

    started_by_us = False

    try:
        if original_state == "exited":
            result = run(["podman", "start", container], timeout=60)
            if result.returncode != 0:
                raise BackupError(
                    result.stderr.strip()
                    or "No se pudo iniciar PostgreSQL."
                )
            started_by_us = True

        wait_postgres(container, db_user, db_name)

        database_dump = staging / "database.dump"
        globals_sql = staging / "globals.sql"

        run_to_file([
            "podman", "exec", container,
            "pg_dump",
            "-U", db_user,
            "-d", db_name,
            "-Fc",
        ], database_dump)

        run_to_file([
            "podman", "exec", container,
            "pg_dumpall",
            "-U", db_user,
            "--globals-only",
        ], globals_sql)

        os.chmod(database_dump, 0o600)
        os.chmod(globals_sql, 0o600)

        hashes = run(
            ["sha256sum", "database.dump", "globals.sql"],
            cwd=staging,
        )
        if hashes.returncode != 0:
            raise BackupError("No se pudieron generar SHA256SUMS.")

        checksum_file = staging / "SHA256SUMS"
        checksum_file.write_text(hashes.stdout, encoding="utf-8")
        os.chmod(checksum_file, 0o600)

    finally:
        if started_by_us:
            result = run(
                ["podman", "stop", "-t", "30", container],
                timeout=45,
            )
            if result.returncode != 0:
                raise BackupError(
                    "No se pudo devolver PostgreSQL a estado detenido."
                )

    final_state = postgres_state(container)
    if final_state != original_state:
        raise BackupError(
            f"PostgreSQL cambió de estado: {original_state} -> {final_state}."
        )

    return staging


def validate_postgres_staging(
    staging,
    image="docker.io/library/postgres:18",
):
    staging = Path(staging)

    for name in ("database.dump", "globals.sql", "SHA256SUMS"):
        if not (staging / name).is_file():
            raise BackupError(f"Falta {name} en el staging PostgreSQL.")

    hashes = run(["sha256sum", "-c", "SHA256SUMS"], cwd=staging)
    if hashes.returncode != 0:
        raise BackupError(
            hashes.stderr.strip()
            or hashes.stdout.strip()
            or "Falló la validación SHA256."
        )

    archive = run([
        "podman", "run", "--rm",
        "--network", "none",
        "--entrypoint", "pg_restore",
        "-v", f"{staging}:/backup:ro",
        image,
        "--list", "/backup/database.dump",
    ], timeout=120)

    if archive.returncode != 0:
        raise BackupError(
            archive.stderr.strip()
            or "pg_restore no pudo leer database.dump."
        )

    return {
        "staging": str(staging),
        "database_dump": (staging / "database.dump").stat().st_size,
        "globals_sql": (staging / "globals.sql").stat().st_size,
        "archive_entries": len(archive.stdout.splitlines()),
    }


def backup_sources(postgres_staging):
    home = Path.home()
    staging = Path(postgres_staging).expanduser().resolve()
    expected_parent = (
        home / ".local" / "state" / "sineos" / "backup" / "staging"
    ).resolve()

    if staging.parent != expected_parent:
        raise BackupError(
            "El staging PostgreSQL no pertenece al directorio autorizado."
        )

    if not staging.name.startswith("postgresql-"):
        raise BackupError("Nombre de staging PostgreSQL inesperado.")

    sources = [
        REPO_ROOT,
        home / "Obsidian" / "SineOS",
        home / ".config" / "sineos",
        home / ".local" / "state" / "sineos" / "health",
        home / ".local" / "state" / "sineos" / "security",
        home / ".local" / "state" / "sineos-maintenance",
        staging,
    ]

    missing = [str(item) for item in sources if not item.exists()]
    if missing:
        raise BackupError(
            "Faltan fuentes de backup: " + ", ".join(missing)
        )

    return sources


def backup_excludes():
    home = Path.home()

    return [
        home / ".config" / "sineos" / "restic-password",
        REPO_ROOT / "Containers" / "volumes" / "postgres" / "data",
        REPO_ROOT / "Containers" / "volumes" / "open-webui" / "data" / "cache",
        REPO_ROOT / "Containers" / "volumes" / "stirling-pdf" / "configs" / "cache",
        REPO_ROOT / "Containers" / "volumes" / "stirling-pdf" / "logs",
        REPO_ROOT / "Containers" / "volumes" / "stirling-pdf" / "tessdata",
        home / "Obsidian" / "SineOS" / ".opencode" / "node_modules",
    ]


def restic_snapshot_count(root, password_file):
    result = run([
        "restic",
        "-r", str(root),
        "--password-file", str(password_file),
        "--no-lock",
        "snapshots",
        "--json",
    ], timeout=120)

    if result.returncode != 0:
        raise BackupError(
            result.stderr.strip()
            or "No se pudo consultar los snapshots Restic."
        )

    try:
        snapshots = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise BackupError("Restic devolvió JSON inválido.") from exc

    return len(snapshots)


def restic_backup_command(
    root,
    password_file,
    tag,
    sources,
    excludes,
    dry_run=False,
):
    command = [
        "podman", "unshare",
        "restic",
        "-r", str(root),
        "--password-file", str(password_file),
    ]

    if dry_run:
        command.append("--no-lock")

    command.extend([
        "backup",
        "--host", "sineos",
        "--tag", tag,
    ])

    if dry_run:
        command.append("--dry-run")

    for excluded in excludes:
        command.extend(["--exclude", str(excluded)])

    command.extend(str(source) for source in sources)
    return command


def create_restic_snapshot_command(
    root,
    password_file,
    tag,
    sources,
    excludes,
):
    return restic_backup_command(
        root,
        password_file,
        tag,
        sources,
        excludes,
        dry_run=False,
    )


def create_restic_snapshot(
    *,
    root,
    password_file,
    postgres_staging,
    tag,
):
    target = Path(root)
    password = Path(password_file)
    sources = backup_sources(postgres_staging)
    excludes = backup_excludes()

    before = restic_snapshot_count(target, password)

    result = run(
        create_restic_snapshot_command(
            target,
            password,
            tag,
            sources,
            excludes,
        ),
        timeout=900,
    )

    if result.returncode != 0:
        raise BackupError(
            result.stderr.strip()
            or result.stdout.strip()
            or "Falló la creación del snapshot Restic."
        )

    after = restic_snapshot_count(target, password)

    if after != before + 1:
        raise BackupError(
            f"Se esperaba exactamente un snapshot nuevo: {before} -> {after}."
        )

    snapshots = run([
        "restic",
        "-r", str(target),
        "--password-file", str(password),
        "--no-lock",
        "snapshots",
        "--json",
        "--tag", tag,
    ], timeout=120)

    if snapshots.returncode != 0:
        raise BackupError("No se pudo localizar el snapshot recién creado.")

    try:
        matches = json.loads(snapshots.stdout)
    except json.JSONDecodeError as exc:
        raise BackupError("Restic devolvió JSON inválido al buscar el snapshot.") from exc

    if len(matches) != 1:
        raise BackupError(
            f"El tag {tag} debe identificar exactamente un snapshot."
        )

    snapshot_id = matches[0].get("id")
    if not snapshot_id:
        raise BackupError("El snapshot recién creado no tiene ID.")

    return {
        "snapshot_id": snapshot_id,
        "tag": tag,
        "snapshots_before": before,
        "snapshots_after": after,
        "output": result.stdout.strip(),
    }


def dry_run_backup(
    *,
    root,
    password_file,
    postgres_staging,
    tag=None,
):
    target = Path(root)
    password = Path(password_file)
    sources = backup_sources(postgres_staging)
    excludes = backup_excludes()
    tag = tag or ("SineOsBackups-DRYRUN-" + datetime.now().strftime("%d%m%y-%H%M"))

    before = restic_snapshot_count(target, password)

    result = run(
        restic_backup_command(
            target,
            password,
            tag,
            sources,
            excludes,
            dry_run=True,
        ),
        timeout=600,
    )

    if result.returncode != 0:
        raise BackupError(
            result.stderr.strip()
            or result.stdout.strip()
            or "Falló Restic dry-run."
        )

    after = restic_snapshot_count(target, password)

    if before != after:
        raise BackupError(
            "El dry-run alteró inesperadamente el número de snapshots."
        )

    return {
        "tag": tag,
        "snapshots_before": before,
        "snapshots_after": after,
        "output": result.stdout.strip(),
    }


def restic_check(root, password_file):
    result = run([
        "restic",
        "-r", str(root),
        "--password-file", str(password_file),
        "--no-lock",
        "check",
    ], timeout=600)

    if result.returncode != 0:
        raise BackupError(
            result.stderr.strip()
            or result.stdout.strip()
            or "Falló restic check."
        )

    return {
        "ok": True,
        "output": (result.stdout + result.stderr).strip(),
    }


def create_restore_target(base=None):
    restore_root = Path(
        base
        or "~/.local/state/sineos/backup/restore-tests"
    ).expanduser()

    restore_root.mkdir(parents=True, exist_ok=True)
    os.chmod(restore_root, 0o700)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = restore_root / f"td023-{stamp}"

    if target.exists():
        raise BackupError("El destino temporal de restore ya existe.")

    target.mkdir(mode=0o700)
    return target


def restore_snapshot(
    *,
    root,
    password_file,
    snapshot_id,
    restore_target=None,
):
    target = (
        Path(restore_target).expanduser()
        if restore_target
        else create_restore_target()
    )

    result = run([
        "podman", "unshare",
        "restic",
        "-r", str(root),
        "--password-file", str(password_file),
        "--no-lock",
        "restore", snapshot_id,
        "--target", str(target),
        "--verify",
    ], timeout=900)

    if result.returncode != 0:
        raise BackupError(
            result.stderr.strip()
            or result.stdout.strip()
            or "Falló el restore de verificación."
        )

    return {
        "snapshot": snapshot_id,
        "target": str(target),
        "output": (result.stdout + result.stderr).strip(),
    }


def validate_restored_layout(restore_target, postgres_staging=None):
    target = Path(restore_target).expanduser()
    live_home = Path.home().resolve()
    restored_home = target / "home" / live_home.name

    required = [
        restored_home / "Workspace" / "SineOS",
        restored_home / "Obsidian" / "SineOS",
        restored_home / ".config" / "sineos",
        restored_home / ".local" / "state" / "sineos-maintenance",
    ]

    missing = [str(item) for item in required if not item.exists()]
    if missing:
        raise BackupError(
            "Restore incompleto. Faltan: " + ", ".join(missing)
        )

    forbidden = [
        restored_home / ".config" / "sineos" / "restic-password",
        restored_home / "Workspace" / "SineOS"
        / "Containers" / "volumes" / "postgres" / "data",
    ]

    present = [str(item) for item in forbidden if item.exists()]
    if present:
        raise BackupError(
            "El restore contiene rutas que debían estar excluidas: "
            + ", ".join(present)
        )

    restored_staging = None

    if postgres_staging:
        staging = Path(postgres_staging).expanduser().resolve()

        try:
            relative = staging.relative_to(live_home)
        except ValueError as exc:
            raise BackupError(
                "El staging PostgreSQL no pertenece al HOME actual."
            ) from exc

        restored_staging = restored_home / relative

        for name in ("database.dump", "globals.sql", "SHA256SUMS"):
            if not (restored_staging / name).is_file():
                raise BackupError(
                    f"Falta {name} en el staging PostgreSQL restaurado."
                )

    return {
        "target": str(target),
        "repository": str(required[0]),
        "vault": str(required[1]),
        "private_config": str(required[2]),
        "maintenance_state": str(required[3]),
        "postgres_staging": (
            str(restored_staging)
            if restored_staging
            else None
        ),
        "restic_password_excluded": True,
        "pgdata_excluded": True,
    }


def cleanup_postgres_test_resources(container, volume):
    run(["podman", "rm", "-f", container], timeout=60)
    run(["podman", "volume", "rm", "-f", volume], timeout=60)


def start_postgres_test_container(staging):
    staging = Path(staging).resolve()

    if not staging.is_dir():
        raise BackupError("No existe el staging PostgreSQL restaurado.")

    token = str(time.time_ns())
    container = "sineos-td023-pg-" + token
    volume = "sineos-td023-pg-" + token

    created = run(["podman", "volume", "create", volume], timeout=60)

    if created.returncode != 0:
        raise BackupError("No se pudo crear el volumen temporal PostgreSQL.")

    started = run([
        "podman", "run", "-d",
        "--name", container,
        "--network", "none",
        "-e", "POSTGRES_HOST_AUTH_METHOD=trust",
        "-v", volume + ":/var/lib/postgresql",
        "-v", str(staging) + ":/backup:ro",
        "docker.io/library/postgres:18",
    ], timeout=120)

    if started.returncode != 0:
        cleanup_postgres_test_resources(container, volume)
        raise BackupError(
            started.stderr.strip()
            or "No se pudo iniciar PostgreSQL temporal."
        )

    return {
        "container": container,
        "volume": volume,
    }


def restore_postgres_test_globals(container):
    wait_postgres(container, "postgres", "postgres", attempts=60)

    result = run([
        "podman", "exec", container,
        "psql",
        "-U", "postgres",
        "-d", "postgres",
        "-v", "ON_ERROR_STOP=1",
        "-f", "/backup/globals.sql",
    ], timeout=120)

    if result.returncode != 0:
        raise BackupError(
            result.stderr.strip()
            or "Falló la restauración de globals.sql."
        )

    role = run([
        "podman", "exec", container,
        "psql",
        "-U", "postgres",
        "-d", "postgres",
        "-Atqc",
        "SELECT count(*) FROM pg_roles WHERE rolname=$$sineos$$;",
    ], timeout=30)

    if role.returncode != 0 or role.stdout.strip() != "1":
        raise BackupError("El rol sineos no fue restaurado.")

    return True


def restore_postgres_test_database(container):
    created = run([
        "podman", "exec", container,
        "createdb",
        "-U", "postgres",
        "-O", "sineos",
        "sineos",
    ], timeout=60)

    if created.returncode != 0:
        raise BackupError(
            created.stderr.strip()
            or "No se pudo crear la base sineos temporal."
        )

    restored = run([
        "podman", "exec", container,
        "pg_restore",
        "-U", "postgres",
        "-d", "sineos",
        "--exit-on-error",
        "/backup/database.dump",
    ], timeout=300)

    if restored.returncode != 0:
        raise BackupError(
            restored.stderr.strip()
            or "Falló la restauración de database.dump."
        )

    check = run([
        "podman", "exec", container,
        "psql",
        "-U", "sineos",
        "-d", "sineos",
        "-Atqc",
        "SELECT current_database() || chr(124) || current_user;",
    ], timeout=30)

    if check.returncode != 0 or check.stdout.strip() != "sineos|sineos":
        raise BackupError(
            "La base restaurada no es utilizable por el rol sineos."
        )

    return True


def stop_postgres_test_container(container):
    stopped = run(
        ["podman", "stop", "-t", "30", container],
        timeout=60,
    )

    if stopped.returncode != 0:
        raise BackupError(
            stopped.stderr.strip()
            or "PostgreSQL temporal no pudo detenerse limpiamente."
        )

    state = run([
        "podman", "inspect", container,
        "--format", "{{.State.ExitCode}}",
    ])

    if state.returncode != 0 or state.stdout.strip() != "0":
        raise BackupError(
            "PostgreSQL temporal terminó con ExitCode distinto de 0."
        )

    return 0


def validate_postgres_restore_functional(restored_staging):
    staging = Path(restored_staging).resolve()
    validate_postgres_staging(staging)

    before = inspect_container_state("sineos-postgres")

    if before["status"] != "exited" or before["exit_code"] != 0:
        raise BackupError(
            "sineos-postgres debe estar detenido limpiamente."
        )

    resources = None

    try:
        resources = start_postgres_test_container(staging)
        container = resources["container"]

        restore_postgres_test_globals(container)
        restore_postgres_test_database(container)
        exit_code = stop_postgres_test_container(container)

    finally:
        if resources:
            cleanup_postgres_test_resources(
                resources["container"],
                resources["volume"],
            )

    after = inspect_container_state("sineos-postgres")

    if (
        after["status"] != before["status"]
        or after["exit_code"] != before["exit_code"]
    ):
        raise BackupError(
            "Cambió el estado de PostgreSQL de producción."
        )

    return {
        "staging": str(staging),
        "database": "sineos",
        "role": "sineos",
        "connection": "sineos|sineos",
        "temporary_exit_code": exit_code,
        "production_before": before["status"],
        "production_after": after["status"],
    }


def cleanup_uptime_test_copy(work):
    result = run(
        ["podman", "unshare", "rm", "-rf", str(Path(work).resolve())],
        timeout=120,
    )

    if result.returncode != 0:
        raise BackupError(
            result.stderr.strip()
            or "No se pudo eliminar la copia temporal de Uptime Kuma."
        )


def prepare_uptime_test_copy(restored_repo):
    repo = Path(restored_repo).resolve()
    source = repo / "Containers/volumes/uptime-kuma/data"

    if not source.is_dir():
        raise BackupError(
            "No existen los datos restaurados de Uptime Kuma."
        )

    root = (
        Path.home()
        / ".local/state/sineos/backup/functional-tests"
    )
    root.mkdir(parents=True, exist_ok=True)
    root.chmod(0o700)

    work = root / ("uptime-kuma-" + str(time.time_ns()))
    work.mkdir(mode=0o700)

    copied = run([
        "podman", "unshare",
        "cp", "-a",
        str(source) + "/.",
        str(work) + "/",
    ], timeout=120)

    if copied.returncode != 0:
        cleanup_uptime_test_copy(work)
        raise BackupError(
            copied.stderr.strip()
            or "No se pudieron copiar los datos de Uptime Kuma."
        )

    return {
        "source": str(source),
        "work": str(work),
    }


def cleanup_uptime_test_container(container):
    result = run(
        ["podman", "rm", "-f", container],
        timeout=60,
    )

    if result.returncode != 0:
        raise BackupError(
            result.stderr.strip()
            or "No se pudo eliminar el contenedor temporal de Uptime Kuma."
        )


def start_uptime_test_container(work):
    work = Path(work).resolve()

    if not work.is_dir():
        raise BackupError(
            "No existe la copia temporal de Uptime Kuma."
        )

    production = inspect_container_state("sineos-uptime-kuma")

    if production["status"] != "exited" or production["exit_code"] != 0:
        raise BackupError(
            "sineos-uptime-kuma debe estar detenido limpiamente."
        )

    container = "sineos-td023-uptime-" + str(time.time_ns())

    started = run([
        "podman", "run", "-d",
        "--name", container,
        "--network", "none",
        "-v", str(work) + ":/app/data",
        production["image"],
    ], timeout=120)

    if started.returncode != 0:
        cleanup_uptime_test_container(container)
        raise BackupError(
            started.stderr.strip()
            or "No se pudo iniciar Uptime Kuma temporal."
        )

    return {
        "container": container,
        "image": production["image"],
    }


def wait_uptime_test_http(container, attempts=60):
    script = (
        "fetch(process.argv[1]).then(r=>{"
        "console.log(r.status);"
        "process.exit(r.status>=200&&r.status<400?0:1);"
        "}).catch(()=>process.exit(1));"
    )

    for _ in range(attempts):
        probe = run([
            "podman", "exec", container,
            "node", "-e", script,
            "http://127.0.0.1:3001/",
        ], timeout=10)

        if probe.returncode == 0:
            lines = probe.stdout.strip().splitlines()

            try:
                status = int(lines[-1]) if lines else 0
            except ValueError:
                status = 0

            if 200 <= status < 400:
                return status

        state = run([
            "podman", "inspect", container,
            "--format", "{{.State.Running}}",
        ])

        if state.returncode != 0 or state.stdout.strip() != "true":
            logs = run([
                "podman", "logs", "--tail", "80", container,
            ], timeout=30)

            raise BackupError(
                "Uptime Kuma temporal terminó durante el arranque. "
                + (logs.stdout.strip() or logs.stderr.strip())
            )

        time.sleep(1)

    raise BackupError(
        "Uptime Kuma temporal no respondió por HTTP a tiempo."
    )


def stop_uptime_test_container(container):
    stopped = run(
        ["podman", "stop", "-t", "30", container],
        timeout=60,
    )

    if stopped.returncode != 0:
        raise BackupError(
            stopped.stderr.strip()
            or "Uptime Kuma temporal no pudo detenerse limpiamente."
        )

    state = run([
        "podman", "inspect", container,
        "--format", "{{.State.ExitCode}}",
    ])

    if state.returncode != 0 or state.stdout.strip() != "0":
        raise BackupError(
            "Uptime Kuma temporal terminó con ExitCode distinto de 0."
        )

    return 0


def validate_uptime_restore_functional(restored_repo):
    before = inspect_container_state("sineos-uptime-kuma")

    if before["status"] != "exited" or before["exit_code"] != 0:
        raise BackupError(
            "sineos-uptime-kuma debe estar detenido limpiamente."
        )

    copy = None
    container = None

    try:
        copy = prepare_uptime_test_copy(restored_repo)

        source_before = run([
            "podman", "unshare", "find",
            copy["source"], "-type", "f",
        ]).stdout.splitlines()

        started = start_uptime_test_container(copy["work"])
        container = started["container"]

        http_initial = wait_uptime_test_http(container, attempts=60)

        time.sleep(15)

        http_stable = wait_uptime_test_http(container, attempts=1)

        exit_code = stop_uptime_test_container(container)

    finally:
        if container:
            cleanup_uptime_test_container(container)

        if copy:
            cleanup_uptime_test_copy(copy["work"])

    source_after = run([
        "podman", "unshare", "find",
        copy["source"], "-type", "f",
    ]).stdout.splitlines()

    if len(source_before) != len(source_after):
        raise BackupError(
            "Cambió el restore original de Uptime Kuma."
        )

    after = inspect_container_state("sineos-uptime-kuma")

    if (
        after["status"] != before["status"]
        or after["exit_code"] != before["exit_code"]
    ):
        raise BackupError(
            "Cambió el estado de Uptime Kuma de producción."
        )

    return {
        "http_initial": http_initial,
        "http_stable": http_stable,
        "temporary_exit_code": exit_code,
        "restored_files": len(source_after),
        "production_before": before["status"],
        "production_after": after["status"],
    }


def cleanup_openwebui_test_copy(work):
    result = run(
        ["podman", "unshare", "rm", "-rf", str(Path(work).resolve())],
        timeout=120,
    )

    if result.returncode != 0:
        raise BackupError(
            result.stderr.strip()
            or "No se pudo eliminar la copia temporal de Open WebUI."
        )


def prepare_openwebui_test_copy(restored_repo):
    repo = Path(restored_repo).resolve()
    source = repo / "Containers/volumes/open-webui/data"

    if not source.is_dir():
        raise BackupError(
            "No existen los datos restaurados de Open WebUI."
        )

    database = source / "webui.db"

    if not database.is_file():
        raise BackupError(
            "No existe webui.db en el restore de Open WebUI."
        )

    root = (
        Path.home()
        / ".local/state/sineos/backup/functional-tests"
    )
    root.mkdir(parents=True, exist_ok=True)
    root.chmod(0o700)

    work = root / ("open-webui-" + str(time.time_ns()))
    work.mkdir(mode=0o700)

    copied = run([
        "podman", "unshare",
        "cp", "-a",
        str(source) + "/.",
        str(work) + "/",
    ], timeout=120)

    if copied.returncode != 0:
        cleanup_openwebui_test_copy(work)
        raise BackupError(
            copied.stderr.strip()
            or "No se pudieron copiar los datos de Open WebUI."
        )

    return {
        "source": str(source),
        "work": str(work),
    }


def validate_openwebui_sqlite(work):
    database = Path(work).resolve() / "webui.db"

    if not database.is_file():
        raise BackupError(
            "No existe webui.db en la copia temporal."
        )

    connection = None

    try:
        connection = sqlite3.connect(
            "file:{}?mode=ro".format(database),
            uri=True,
        )

        integrity = connection.execute(
            "PRAGMA integrity_check"
        ).fetchone()[0]

        tables = connection.execute(
            "SELECT count(*) FROM sqlite_master WHERE type=?",
            ("table",),
        ).fetchone()[0]

    except sqlite3.Error as exc:
        raise BackupError(
            "No se pudo validar webui.db: {}".format(exc)
        ) from exc

    finally:
        if connection is not None:
            connection.close()

    if integrity != "ok":
        raise BackupError(
            "webui.db no pasó PRAGMA integrity_check."
        )

    if tables <= 0:
        raise BackupError(
            "webui.db no contiene tablas."
        )

    return {
        "integrity": integrity,
        "tables": tables,
    }


def cleanup_openwebui_test_container(container):
    result = run(
        ["podman", "rm", "-f", container],
        timeout=60,
    )

    if result.returncode != 0:
        raise BackupError(
            result.stderr.strip()
            or "No se pudo eliminar el contenedor temporal de Open WebUI."
        )


def start_openwebui_test_container(work):
    work = Path(work).resolve()

    if not work.is_dir():
        raise BackupError(
            "No existe la copia temporal de Open WebUI."
        )

    production = inspect_container_state("sineos-open-webui")

    if production["status"] != "exited" or production["exit_code"] != 0:
        raise BackupError(
            "sineos-open-webui debe estar detenido limpiamente."
        )

    container = "sineos-td023-openwebui-" + str(time.time_ns())

    started = run([
        "podman", "run", "-d",
        "--name", container,
        "--network", "none",
        "-v", str(work) + ":/app/backend/data",
        production["image"],
    ], timeout=120)

    if started.returncode != 0:
        cleanup_openwebui_test_container(container)
        raise BackupError(
            started.stderr.strip()
            or "No se pudo iniciar Open WebUI temporal."
        )

    return {
        "container": container,
        "image": production["image"],
    }


def wait_openwebui_test_http(container, attempts=90):
    script = (
        "import urllib.request,sys; "
        "r=urllib.request.urlopen(sys.argv[1],timeout=5); "
        "print(r.status)"
    )

    for _ in range(attempts):
        probe = run([
            "podman", "exec", container,
            "python", "-c", script,
            "http://127.0.0.1:8080/",
        ], timeout=10)

        if probe.returncode == 0:
            lines = probe.stdout.strip().splitlines()

            try:
                status = int(lines[-1]) if lines else 0
            except ValueError:
                status = 0

            if 200 <= status < 400:
                return status

        state = run([
            "podman", "inspect", container,
            "--format", "{{.State.Running}}",
        ])

        if state.returncode != 0 or state.stdout.strip() != "true":
            logs = run([
                "podman", "logs", "--tail", "80", container,
            ], timeout=30)

            raise BackupError(
                "Open WebUI temporal terminó durante el arranque. "
                + (logs.stdout.strip() or logs.stderr.strip())
            )

        time.sleep(1)

    raise BackupError(
        "Open WebUI temporal no respondió por HTTP a tiempo."
    )


def stop_openwebui_test_container(container):
    stopped = run(
        ["podman", "stop", "-t", "30", container],
        timeout=60,
    )

    if stopped.returncode != 0:
        raise BackupError(
            stopped.stderr.strip()
            or "Open WebUI temporal no pudo detenerse limpiamente."
        )

    state = run([
        "podman", "inspect", container,
        "--format", "{{.State.ExitCode}}",
    ])

    if state.returncode != 0 or state.stdout.strip() != "0":
        raise BackupError(
            "Open WebUI temporal terminó con ExitCode distinto de 0."
        )

    return 0


def validate_openwebui_restore_functional(restored_repo):
    before = inspect_container_state("sineos-open-webui")

    if before["status"] != "exited" or before["exit_code"] != 0:
        raise BackupError(
            "sineos-open-webui debe estar detenido limpiamente."
        )

    copy = None
    container = None

    try:
        copy = prepare_openwebui_test_copy(restored_repo)

        source_before = run([
            "podman", "unshare", "find",
            copy["source"], "-type", "f",
        ]).stdout.splitlines()

        sqlite_before = validate_openwebui_sqlite(copy["work"])

        started = start_openwebui_test_container(copy["work"])
        container = started["container"]

        http_initial = wait_openwebui_test_http(container, attempts=90)

        time.sleep(15)

        http_stable = wait_openwebui_test_http(container, attempts=1)

        exit_code = stop_openwebui_test_container(container)

        sqlite_after = validate_openwebui_sqlite(copy["work"])

        if sqlite_before["integrity"] != "ok":
            raise BackupError("SQLite inicial de Open WebUI no es íntegro.")

        if sqlite_after["integrity"] != "ok":
            raise BackupError("SQLite final de Open WebUI no es íntegro.")

        if sqlite_before["tables"] != sqlite_after["tables"]:
            raise BackupError(
                "Cambió el número de tablas de Open WebUI durante la prueba."
            )

    finally:
        if container:
            cleanup_openwebui_test_container(container)

        if copy:
            cleanup_openwebui_test_copy(copy["work"])

    source_after = run([
        "podman", "unshare", "find",
        copy["source"], "-type", "f",
    ]).stdout.splitlines()

    if len(source_before) != len(source_after):
        raise BackupError(
            "Cambió el restore original de Open WebUI."
        )

    after = inspect_container_state("sineos-open-webui")

    if (
        after["status"] != before["status"]
        or after["exit_code"] != before["exit_code"]
    ):
        raise BackupError(
            "Cambió el estado de Open WebUI de producción."
        )

    return {
        "sqlite_integrity": sqlite_after["integrity"],
        "sqlite_tables": sqlite_after["tables"],
        "http_initial": http_initial,
        "http_stable": http_stable,
        "temporary_exit_code": exit_code,
        "restored_files": len(source_after),
        "production_before": before["status"],
        "production_after": after["status"],
    }


def cleanup_stirling_test_copy(work):
    result = run(
        ["podman", "unshare", "rm", "-rf", str(Path(work).resolve())],
        timeout=120,
    )

    if result.returncode != 0:
        raise BackupError(
            result.stderr.strip()
            or "No se pudo eliminar la copia temporal de Stirling PDF."
        )


def prepare_stirling_test_copy(restored_repo):
    repo = Path(restored_repo).resolve()
    source = repo / "Containers/volumes/stirling-pdf"

    if not source.is_dir():
        raise BackupError(
            "No existen los datos restaurados de Stirling PDF."
        )

    database = source / "configs/stirling-pdf-DB-2.3.232.mv.db"

    if not database.is_file():
        raise BackupError(
            "No existe la base H2 restaurada de Stirling PDF."
        )

    root = (
        Path.home()
        / ".local/state/sineos/backup/functional-tests"
    )
    root.mkdir(parents=True, exist_ok=True)
    root.chmod(0o700)

    work = root / ("stirling-pdf-" + str(time.time_ns()))
    work.mkdir(mode=0o700)

    copied = run([
        "podman", "unshare",
        "cp", "-a",
        str(source) + "/.",
        str(work) + "/",
    ], timeout=120)

    if copied.returncode != 0:
        cleanup_stirling_test_copy(work)
        raise BackupError(
            copied.stderr.strip()
            or "No se pudieron copiar los datos de Stirling PDF."
        )

    created = run([
        "podman", "unshare", "mkdir", "-p",
        str(work / "configs/cache"),
        str(work / "logs"),
        str(work / "tessdata"),
    ], timeout=60)

    if created.returncode != 0:
        cleanup_stirling_test_copy(work)
        raise BackupError(
            created.stderr.strip()
            or "No se pudieron recrear los directorios excluidos de Stirling."
        )

    return {
        "source": str(source),
        "work": str(work),
        "database": str(database),
    }


def cleanup_stirling_test_container(container):
    result = run(
        ["podman", "rm", "-f", container],
        timeout=60,
    )

    if result.returncode != 0:
        raise BackupError(
            result.stderr.strip()
            or "No se pudo eliminar el contenedor temporal de Stirling PDF."
        )


def start_stirling_test_container(work):
    work = Path(work).resolve()

    if not work.is_dir():
        raise BackupError(
            "No existe la copia temporal de Stirling PDF."
        )

    production = inspect_container_state("sineos-stirling-pdf")

    if production["status"] != "exited" or production["exit_code"] != 0:
        raise BackupError(
            "sineos-stirling-pdf debe estar detenido limpiamente."
        )

    container = "sineos-td023-stirling-" + str(time.time_ns())

    started = run([
        "podman", "run", "-d",
        "--name", container,
        "--network", "none",
        "-e", "FAT_DOCKER=true",
        "-e", "UMASK=022",
        "-e", "STIRLING_TEMPFILES_DIRECTORY=/tmp/stirling-pdf",
        "-e", "STIRLING_AOT_ENABLE=false",
        "-e", "PUID=1000",
        "-e", "PGID=1000",
        "-e", "SECURITY_ENABLELOGIN=false",
        "-e", "TESS_BASE_PATH=/usr/share/tesseract-ocr/5/tessdata",
        "-e", "STIRLING_JVM_PROFILE=balanced",
        "-e", "INSTALL_BOOK_AND_ADVANCED_HTML_OPS=false",
        "-e", "DISABLE_ADDITIONAL_FEATURES=false",
        "-e", "SYSTEM_DEFAULTLOCALE=es-ES",
        "-v", str(work / "customFiles") + ":/customFiles",
        "-v", str(work / "pipeline") + ":/pipeline",
        "-v", str(work / "tessdata") + ":/usr/share/tessdata",
        "-v", str(work / "configs") + ":/configs",
        "-v", str(work / "logs") + ":/logs",
        production["image"],
    ], timeout=120)

    if started.returncode != 0:
        cleanup_stirling_test_container(container)
        raise BackupError(
            started.stderr.strip()
            or "No se pudo iniciar Stirling PDF temporal."
        )

    return {
        "container": container,
        "image": production["image"],
    }


def wait_stirling_test_http(container, attempts=120):
    script = (
        "import socket,sys;"
        "s=socket.create_connection((sys.argv[1],int(sys.argv[2])),3);"
        "s.settimeout(3);"
        "s.sendall(sys.argv[3].encode());"
        "data=s.recv(256).decode();"
        "s.close();"
        "lines=data.splitlines();"
        "print(lines[0] if lines else sys.argv[4])"
    )

    request = (
        "GET / HTTP/1.0\r\n"
        "Host: localhost\r\n"
        "Connection: close\r\n\r\n"
    )

    for _ in range(attempts):
        probe = run([
            "podman", "exec", container,
            "python3", "-c", script,
            "127.0.0.1",
            "8080",
            request,
            "",
        ], timeout=10)

        if probe.returncode == 0:
            lines = probe.stdout.strip().splitlines()

            if lines:
                status = lines[-1]
                parts = status.split()

                if (
                    len(parts) >= 2
                    and parts[0].startswith("HTTP/")
                    and parts[1] in (
                        "200", "301", "302",
                        "303", "307", "308",
                    )
                ):
                    return status

        state = run([
            "podman", "inspect", container,
            "--format", "{{.State.Running}}",
        ])

        if state.returncode != 0 or state.stdout.strip() != "true":
            logs = run([
                "podman", "logs", "--tail", "100", container,
            ], timeout=30)

            raise BackupError(
                "Stirling PDF temporal terminó durante el arranque. "
                + (logs.stdout.strip() or logs.stderr.strip())
            )

        time.sleep(1)

    raise BackupError(
        "Stirling PDF temporal no respondió por HTTP a tiempo."
    )


def validate_stirling_test_database(container):
    result = run([
        "podman", "exec", container,
        "test", "-s",
        "/configs/stirling-pdf-DB-2.3.232.mv.db",
    ], timeout=30)

    if result.returncode != 0:
        raise BackupError(
            "La base H2 restaurada de Stirling PDF no está disponible."
        )

    return True


def stop_stirling_test_container(container):
    stopped = run(
        ["podman", "stop", "-t", "30", container],
        timeout=60,
    )

    if stopped.returncode != 0:
        raise BackupError(
            stopped.stderr.strip()
            or "Stirling PDF temporal no pudo detenerse limpiamente."
        )

    state = run([
        "podman", "inspect", container,
        "--format", "{{.State.ExitCode}}",
    ])

    if state.returncode != 0 or state.stdout.strip() != "0":
        raise BackupError(
            "Stirling PDF temporal terminó con ExitCode distinto de 0."
        )

    return 0


def validate_stirling_restore_functional(restored_repo):
    before = inspect_container_state("sineos-stirling-pdf")

    if before["status"] != "exited" or before["exit_code"] != 0:
        raise BackupError(
            "sineos-stirling-pdf debe estar detenido limpiamente."
        )

    copy = None
    container = None

    try:
        copy = prepare_stirling_test_copy(restored_repo)

        source = Path(copy["source"]).resolve()
        source_database = (
            source / "configs/stirling-pdf-DB-2.3.232.mv.db"
        )

        files_before = run([
            "podman", "unshare", "find",
            str(source), "-type", "f",
        ])

        if files_before.returncode != 0:
            raise BackupError(
                "No se pudo inspeccionar el restore de Stirling PDF."
            )

        source_files_before = files_before.stdout.splitlines()

        hash_before = run([
            "podman", "unshare", "sha256sum",
            str(source_database),
        ])

        if hash_before.returncode != 0:
            raise BackupError(
                "No se pudo calcular el hash de la base H2."
            )

        database_hash_before = hash_before.stdout.split()[0]

        started = start_stirling_test_container(copy["work"])
        container = started["container"]

        http_initial = wait_stirling_test_http(
            container,
            attempts=120,
        )

        validate_stirling_test_database(container)

        time.sleep(15)

        http_stable = wait_stirling_test_http(
            container,
            attempts=1,
        )

        exit_code = stop_stirling_test_container(container)

    finally:
        if container:
            cleanup_stirling_test_container(container)

        if copy:
            cleanup_stirling_test_copy(copy["work"])

    files_after = run([
        "podman", "unshare", "find",
        str(source), "-type", "f",
    ])

    if files_after.returncode != 0:
        raise BackupError(
            "No se pudo verificar el restore original de Stirling PDF."
        )

    source_files_after = files_after.stdout.splitlines()

    hash_after = run([
        "podman", "unshare", "sha256sum",
        str(source_database),
    ])

    if hash_after.returncode != 0:
        raise BackupError(
            "No se pudo verificar la base H2 original."
        )

    database_hash_after = hash_after.stdout.split()[0]

    if len(source_files_before) != len(source_files_after):
        raise BackupError(
            "Cambió el número de archivos del restore original de Stirling."
        )

    if database_hash_before != database_hash_after:
        raise BackupError(
            "Cambió la base H2 del restore original de Stirling."
        )

    after = inspect_container_state("sineos-stirling-pdf")

    if (
        after["status"] != before["status"]
        or after["exit_code"] != before["exit_code"]
    ):
        raise BackupError(
            "Cambió el estado de Stirling PDF de producción."
        )

    return {
        "http_initial": http_initial,
        "http_stable": http_stable,
        "h2_database": True,
        "temporary_exit_code": exit_code,
        "restored_files": len(source_files_after),
        "production_before": before["status"],
        "production_after": after["status"],
    }


def validate_functional_restore_suite(restored_repo, restored_staging):
    validate_stateful_containers_stopped()

    postgres = validate_postgres_restore_functional(
        restored_staging
    )

    uptime = validate_uptime_restore_functional(
        restored_repo
    )

    openwebui = validate_openwebui_restore_functional(
        restored_repo
    )

    stirling = validate_stirling_restore_functional(
        restored_repo
    )

    validate_stateful_containers_stopped()

    return {
        "postgres": postgres,
        "uptime_kuma": uptime,
        "open_webui": openwebui,
        "stirling_pdf": stirling,
    }


def validate_restored_git_head(restored_repo, expected_head):
    repo = Path(restored_repo).resolve()

    if not repo.is_dir():
        raise BackupError(
            "No existe el repositorio SineOS restaurado."
        )

    result = run([
        "git", "-C", str(repo),
        "rev-parse", "HEAD",
    ])

    if result.returncode != 0:
        raise BackupError(
            result.stderr.strip()
            or "No se pudo obtener el HEAD del repositorio restaurado."
        )

    actual = result.stdout.strip()

    if actual != expected_head:
        raise BackupError(
            "El HEAD restaurado no coincide con el esperado: "
            + actual
        )

    return {
        "expected": expected_head,
        "actual": actual,
        "match": True,
    }


def certify_restic_snapshot(
    *,
    root,
    password_file,
    snapshot_id,
    postgres_staging,
    expected_head,
):
    validate_stateful_containers_stopped()

    check = restic_check(
        root,
        password_file,
    )

    restored = restore_snapshot(
        root=root,
        password_file=password_file,
        snapshot_id=snapshot_id,
    )

    layout = validate_restored_layout(
        restored["target"],
        postgres_staging,
    )

    git_head = validate_restored_git_head(
        layout["repository"],
        expected_head,
    )

    postgres = validate_postgres_staging(
        layout["postgres_staging"]
    )

    postgres_match = validate_postgres_restore_matches_source(
        postgres_staging,
        layout["postgres_staging"],
    )

    functional = validate_functional_restore_suite(
        layout["repository"],
        layout["postgres_staging"],
    )

    validate_stateful_containers_stopped()

    return {
        "snapshot_id": snapshot_id,
        "restic_check": check["ok"],
        "restore_target": restored["target"],
        "layout": layout,
        "git_head": git_head,
        "postgres_staging": postgres,
        "postgres_match": postgres_match,
        "functional": functional,
        "certified": True,
    }


def validate_postgres_restore_matches_source(
    source_staging,
    restored_staging,
):
    source = Path(source_staging).resolve()
    restored = Path(restored_staging).resolve()

    files = (
        "database.dump",
        "globals.sql",
        "SHA256SUMS",
    )

    for name in files:
        original = source / name
        recovered = restored / name

        if not original.is_file():
            raise BackupError(
                f"Falta {name} en el staging PostgreSQL original."
            )

        if not recovered.is_file():
            raise BackupError(
                f"Falta {name} en el staging PostgreSQL restaurado."
            )

        original_hash = run([
            "sha256sum", str(original)
        ])

        recovered_hash = run([
            "sha256sum", str(recovered)
        ])

        if original_hash.returncode != 0:
            raise BackupError(
                f"No se pudo calcular SHA256 original de {name}."
            )

        if recovered_hash.returncode != 0:
            raise BackupError(
                f"No se pudo calcular SHA256 restaurado de {name}."
            )

        if (
            original_hash.stdout.split()[0]
            != recovered_hash.stdout.split()[0]
        ):
            raise BackupError(
                f"{name} restaurado no coincide con el original."
            )

    return {
        "match": True,
        "files": list(files),
    }


STATEFUL_CONTAINERS = (
    "sineos-postgres",
    "sineos-open-webui",
    "sineos-uptime-kuma",
    "sineos-stirling-pdf",
)


def inspect_container_state(container):
    result = run([
        "podman",
        "inspect",
        container,
        "--format",
        "{{.State.Status}}|{{.State.ExitCode}}|{{.ImageName}}",
    ])

    if result.returncode != 0:
        raise BackupError(
            result.stderr.strip()
            or f"No se pudo inspeccionar el contenedor {container}."
        )

    parts = result.stdout.strip().split("|", 2)

    if len(parts) != 3:
        raise BackupError(
            f"Estado inesperado para el contenedor {container}."
        )

    status, exit_code, image = parts

    try:
        exit_code = int(exit_code)
    except ValueError as exc:
        raise BackupError(
            f"ExitCode inválido para el contenedor {container}."
        ) from exc

    return {
        "container": container,
        "status": status,
        "exit_code": exit_code,
        "image": image,
    }


def validate_stateful_containers_stopped():
    states = {}

    for container in STATEFUL_CONTAINERS:
        state = inspect_container_state(container)
        states[container] = state

        if state["status"] != "exited" or state["exit_code"] != 0:
            raise BackupError(
                f"{container} debe estar detenido limpiamente "
                f"antes del backup; estado={state.get("status")} "
                f"ExitCode={state.get("exit_code")}."
            )

    return states


def validate_git_state(repo_root):
    repo = Path(repo_root)

    branch = run(["git", "branch", "--show-current"], cwd=repo)
    if branch.returncode != 0 or branch.stdout.strip() != "main":
        raise BackupError("La rama activa debe ser main.")

    status = run(["git", "status", "--porcelain"], cwd=repo)
    if status.returncode != 0:
        raise BackupError("No se pudo consultar el estado Git.")
    if status.stdout.strip():
        raise BackupError("Git contiene cambios locales; el backup no comenzará.")

    local = run(["git", "rev-parse", "HEAD"], cwd=repo)
    if local.returncode != 0 or not local.stdout.strip():
        raise BackupError("No se pudo identificar HEAD local.")

    remote = run(
        ["git", "ls-remote", "origin", "refs/heads/main"],
        timeout=30,
        cwd=repo,
        env=git_remote_env(),
    )
    if remote.returncode != 0 or not remote.stdout.strip():
        raise BackupError(
            remote.stderr.strip()
            or "No se pudo consultar origin/main."
        )

    local_head = local.stdout.strip()
    remote_head = remote.stdout.split()[0]

    if local_head != remote_head:
        raise BackupError("HEAD local no coincide con origin/main.")

    return {
        "branch": "main",
        "clean": True,
        "local_head": local_head,
        "remote_head": remote_head,
        "synced": True,
    }


def execute_backup(*, root, expected_uuid=None, expected_serial=None, expected_repository_id=None):
    validate_git_state(REPO_ROOT)
    validate_stateful_containers_stopped()
    preflight(
        root=root,
        expected_uuid=expected_uuid,
        expected_serial=expected_serial,
        expected_repository_id=expected_repository_id,
        require_writable=True,
    )
    raise BackupError("TD-023: ejecución de backup todavía no implementada.")
