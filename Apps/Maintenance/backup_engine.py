#!/usr/bin/env python3

import json
import os
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
    preflight(
        root=root,
        expected_uuid=expected_uuid,
        expected_serial=expected_serial,
        expected_repository_id=expected_repository_id,
        require_writable=True,
    )
    raise BackupError("TD-023: ejecución de backup todavía no implementada.")
