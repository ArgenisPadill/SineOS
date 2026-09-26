#!/usr/bin/env python3

import json
import os
import shutil
import stat
import subprocess
from datetime import datetime
from pathlib import Path


class BackupError(RuntimeError):
    pass


def run(command, timeout=30):
    try:
        return subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise BackupError(str(exc)) from exc


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


def execute_backup(*, root, expected_uuid=None, expected_serial=None, expected_repository_id=None):
    preflight(
        root=root,
        expected_uuid=expected_uuid,
        expected_serial=expected_serial,
        expected_repository_id=expected_repository_id,
        require_writable=True,
    )
    raise BackupError("TD-023: ejecución de backup todavía no implementada.")
