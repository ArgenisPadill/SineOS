#!/usr/bin/env python3

import calendar
import json
import os
import re
import subprocess
from datetime import date, datetime
from pathlib import Path

import backup_engine

APP_FILE = Path(__file__).resolve()
REPO_ROOT = APP_FILE.parents[2]
STATE_DIR = Path.home() / ".local" / "state" / "sineos-maintenance"
STATE_FILE = STATE_DIR / "state.json"
CONFIG_FILE = Path.home() / ".config" / "sineos" / "maintenance.env"
HEALTH_REPORT_DIR = Path.home() / ".local" / "state" / "sineos" / "health"
HEALTH_STATUS_FILE = REPO_ROOT / "Documentation" / "Operations" / "Health-Status.md"
BACKUP_STATUS_FILE = REPO_ROOT / "Documentation" / "Recovery" / "Backup-Status.md"
AUDIT_SCRIPT = REPO_ROOT / "Scripts" / "Audit" / "sineos-health-audit.sh"
INTERACTIVE_AUDIT = REPO_ROOT / "Scripts" / "Maintenance" / "run-health-audit-interactive.sh"

DEFAULT_STATE = {
    "health": {
        "last_validated": None,
        "commit": None,
        "audit_version": None,
    },
    "backup": {
        "enabled": False,
        "last_validated": None,
        "event_commit": None,
        "sync_commit": None,
        "tag": None,
    },
}


class MaintenanceError(RuntimeError):
    pass


def run(command, timeout=30, cwd=None, env=None):
    try:
        return subprocess.run(
            command,
            cwd=str(cwd or REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            env=env,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise MaintenanceError(str(exc)) from exc


def git_remote_env():
    env = dict(os.environ)
    runtime_dir = Path(
        env.get("XDG_RUNTIME_DIR") or f"/run/user/{os.getuid()}"
    )
    gcr_socket = runtime_dir / "gcr" / "ssh"

    if gcr_socket.exists():
        env["SSH_AUTH_SOCK"] = str(gcr_socket)

    # Las operaciones remotas iniciadas desde la GUI nunca deben quedar
    # esperando una passphrase en una terminal inexistente.
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["SSH_ASKPASS_REQUIRE"] = "never"
    env["GIT_SSH_COMMAND"] = "ssh -o BatchMode=yes"

    return env


def ensure_state_dir():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(STATE_DIR, 0o700)


def load_state():
    ensure_state_dir()
    state = json.loads(json.dumps(DEFAULT_STATE))
    if not STATE_FILE.exists():
        return state

    try:
        loaded = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return state

    for section in ("health", "backup"):
        if isinstance(loaded.get(section), dict):
            state[section].update(loaded[section])
    return state


def save_state(state):
    ensure_state_dir()
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.chmod(tmp, 0o600)
    tmp.replace(STATE_FILE)
    os.chmod(STATE_FILE, 0o600)


def parse_env_file(path=CONFIG_FILE):
    values = {}
    if not path.exists():
        return values
    try:
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    except OSError:
        pass
    return values


def add_months(day, months):
    month_index = day.month - 1 + months
    year = day.year + month_index // 12
    month = month_index % 12 + 1
    final_day = min(day.day, calendar.monthrange(year, month)[1])
    return date(year, month, final_day)


def parse_iso_day(value):
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def health_schedule(state=None):
    state = state or load_state()
    last = parse_iso_day(state["health"].get("last_validated"))
    if last is None:
        return None, None, True
    due = add_months(last, 3)
    return last, due, date.today() >= due


def backup_schedule(state=None):
    state = state or load_state()
    enabled = bool(state["backup"].get("enabled"))
    last = parse_iso_day(state["backup"].get("last_validated"))
    if not enabled:
        return False, last, None, False
    if last is None:
        return True, None, None, True
    due = add_months(last, 3)
    return True, last, due, date.today() >= due


def git_sync_state():
    branch = run(["git", "branch", "--show-current"]).stdout.strip()
    porcelain = run(["git", "status", "--porcelain"]).stdout
    local_head = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    remote = run(
        ["git", "ls-remote", "origin", "refs/heads/main"],
        timeout=20,
        env=git_remote_env(),
    )
    remote_head = ""
    if remote.returncode == 0 and remote.stdout.strip():
        remote_head = remote.stdout.split()[0]
    return {
        "branch": branch,
        "clean": porcelain.strip() == "",
        "changes": porcelain.strip(),
        "local_head": local_head,
        "remote_head": remote_head,
        "synced": bool(local_head and remote_head and local_head == remote_head),
    }


def latest_health_report():
    if not HEALTH_REPORT_DIR.exists():
        return None
    reports = sorted(
        HEALTH_REPORT_DIR.glob("sineos-health-audit-*.txt"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not reports:
        return None

    path = reports[0]
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None

    def match(pattern, default=None):
        found = re.search(pattern, text, re.MULTILINE)
        return found.group(1).strip() if found else default

    timestamp = match(r"^Fecha:\s+(.+)$")
    report_day = None
    if timestamp:
        try:
            report_day = datetime.strptime(
                timestamp.split()[0], "%Y-%m-%d"
            ).date()
        except ValueError:
            pass

    def number(label):
        raw = match(rf"^{re.escape(label)}:\s+(\d+)$", "0")
        try:
            return int(raw)
        except ValueError:
            return 0

    return {
        "path": path,
        "name": path.name,
        "timestamp": timestamp,
        "date": report_day,
        "version": match(r"^Versión:\s+(.+)$"),
        "ok": number("OK"),
        "warnings": number("Advertencias"),
        "errors": number("Errores"),
        "info": number("Información"),
        "result": match(r"^RESULTADO:\s+(.+)$"),
    }


def latest_health_is_valid():
    report = latest_health_report()
    if not report:
        return False, "No existe una auditoría de salud local."
    if report["result"] != "OK":
        return False, f"La última auditoría terminó en {report['result'] or 'estado desconocido'}."
    if report["warnings"] != 0 or report["errors"] != 0:
        return False, "La última auditoría todavía contiene advertencias o errores."
    return True, "Auditoría local validada."


def write_health_status(report):
    if not report or not report.get("date"):
        raise MaintenanceError("La auditoría no tiene una fecha válida.")

    content = f"""# SineOS — Estado de salud trimestral

Este archivo es actualizado por SineOS · Mantenimiento.

## Última auditoría validada

```text
Fecha: {report['date'].strftime('%d-%m-%Y')}
Auditor: sineos-health-audit {report.get('version') or 'desconocido'}
OK: {report['ok']}
Advertencias: {report['warnings']}
Errores: {report['errors']}
Información: {report['info']}
Resultado: {report['result']}
```

## Gate GitHub

El hash del commit se conserva como evidencia Git y en el estado local privado de la aplicación.
No se escribe dentro de este archivo para evitar autorreferencia.

El recordatorio trimestral solo se cierra cuando este estado queda comprometido y sincronizado con `origin/main`.
"""
    HEALTH_STATUS_FILE.write_text(content, encoding="utf-8")


def adopt_current_validation():
    valid, reason = latest_health_is_valid()
    if not valid:
        raise MaintenanceError(reason)

    report = latest_health_report()
    git = git_sync_state()
    if git["branch"] != "main":
        raise MaintenanceError("La rama activa no es main.")
    if not git["clean"]:
        raise MaintenanceError("Git tiene cambios locales; no se adoptará la validación.")
    if not git["synced"]:
        raise MaintenanceError("HEAD local todavía no coincide con origin/main.")

    state = load_state()
    state["health"].update({
        "last_validated": report["date"].isoformat(),
        "commit": git["local_head"],
        "audit_version": report.get("version"),
    })
    save_state(state)
    return git["local_head"]


def sync_health_validation():
    valid, reason = latest_health_is_valid()
    if not valid:
        raise MaintenanceError(reason)
    report = latest_health_report()

    state = load_state()
    registered_day = parse_iso_day(state["health"].get("last_validated"))
    if registered_day and report.get("date") and registered_day >= report["date"]:
        raise MaintenanceError(
            "La última auditoría ya pertenece al ciclo validado. Ejecuta una auditoría nueva antes de registrar otro ciclo."
        )

    before = git_sync_state()
    if before["branch"] != "main":
        raise MaintenanceError("La rama activa no es main.")
    if not before["clean"]:
        raise MaintenanceError(
            "El repositorio tiene cambios locales. SineOS no mezclará otros cambios con el commit de salud."
        )
    if not before["synced"]:
        raise MaintenanceError(
            "Antes de registrar la salud, main local debe coincidir con origin/main."
        )

    write_health_status(report)

    add = run(["git", "add", "--", str(HEALTH_STATUS_FILE.relative_to(REPO_ROOT))])
    if add.returncode != 0:
        raise MaintenanceError(add.stderr.strip() or "No se pudo preparar Health-Status.md.")

    staged = run(["git", "diff", "--cached", "--name-only"]).stdout.splitlines()
    expected = str(HEALTH_STATUS_FILE.relative_to(REPO_ROOT))
    if staged != [expected]:
        run(["git", "reset", "--", expected])
        raise MaintenanceError("El área staged contiene cambios inesperados; se canceló el commit.")

    diff = run(["git", "diff", "--cached", "--quiet"])
    if diff.returncode == 0:
        raise MaintenanceError("Health-Status.md ya coincide con la última auditoría; no hay nada nuevo que comprometer.")

    message = f"maintenance: validate quarterly health {report['date'].isoformat()}"
    commit = run(["git", "commit", "-m", message], timeout=60)
    if commit.returncode != 0:
        raise MaintenanceError(commit.stderr.strip() or commit.stdout.strip() or "Falló git commit.")

    new_head = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    push = run(
        ["git", "push", "origin", "main"],
        timeout=90,
        env=git_remote_env(),
    )
    if push.returncode != 0:
        raise MaintenanceError(
            "El commit local se creó, pero el push falló. El recordatorio seguirá pendiente. "
            + (push.stderr.strip() or push.stdout.strip())
        )

    after = git_sync_state()
    if not after["synced"] or after["local_head"] != new_head:
        raise MaintenanceError("El push terminó, pero no se pudo certificar HEAD local = origin/main.")

    state = load_state()
    state["health"].update({
        "last_validated": report["date"].isoformat(),
        "commit": new_head,
        "audit_version": report.get("version"),
    })
    save_state(state)
    return new_head


def backup_configuration():
    values = dict(os.environ)
    values.update(parse_env_file())
    root = values.get("SINEOS_BACKUP_ROOT", "").strip()
    expected_uuid = values.get("SINEOS_BACKUP_UUID", "").strip()
    expected_serial = values.get("SINEOS_BACKUP_SERIAL", "").strip()
    expected_repository_id = values.get("SINEOS_BACKUP_REPOSITORY_ID", "").strip()
    enabled = values.get("SINEOS_BACKUP_ENABLED", "0").strip().lower() in {
        "1", "true", "yes", "si", "sí"
    }
    path = Path(root).expanduser() if root else None
    valid_name = bool(path and path.name == "SineOsBackups")
    return {
        "enabled": enabled,
        "root": str(path) if path else None,
        "uuid": expected_uuid or None,
        "serial": expected_serial or None,
        "repository_id": expected_repository_id or None,
        "valid_name": valid_name,
        "exists": bool(path and path.is_dir()),
    }


def update_backup_enabled_from_config():
    state = load_state()
    state["backup"]["enabled"] = backup_configuration()["enabled"]
    save_state(state)
    return state


def run_backup_engine():
    cfg = backup_configuration()

    if not cfg["enabled"]:
        raise MaintenanceError(
            "El respaldo externo no está habilitado."
        )

    if not cfg["root"] or not cfg["valid_name"]:
        raise MaintenanceError(
            "SINEOS_BACKUP_ROOT no es válido."
        )

    if not cfg["exists"]:
        raise MaintenanceError(
            "El destino de respaldo no está disponible."
        )

    try:
        return backup_engine.execute_backup(
            root=cfg["root"],
            expected_uuid=cfg["uuid"],
            expected_serial=cfg["serial"],
            expected_repository_id=cfg["repository_id"],
        )
    except backup_engine.BackupError as exc:
        raise MaintenanceError(str(exc)) from exc


def notification_message():
    state = update_backup_enabled_from_config()
    messages = []
    _, health_due, health_overdue = health_schedule(state)
    if health_overdue:
        messages.append("Auditoría trimestral pendiente")
    elif health_due:
        messages.append(f"Salud próxima: {health_due.strftime('%d-%m-%Y')}")

    backup_enabled, _, backup_due, backup_overdue = backup_schedule(state)
    if backup_enabled:
        if backup_overdue:
            messages.append("Respaldo externo pendiente")
        elif backup_due:
            messages.append(f"Respaldo próximo: {backup_due.strftime('%d-%m-%Y')}")

    return state, messages


def send_due_notification():
    state, messages = notification_message()
    if not messages:
        return False

    body = "\n".join(messages) + "\nAbre SineOS · Mantenimiento para completar y validar el ciclo con GitHub."
    try:
        subprocess.run(
            [
                "notify-send",
                "-u", "critical",
                "-a", "SineOS Mantenimiento",
                "SineOS requiere mantenimiento",
                body,
            ],
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return True


def summary():
    state = update_backup_enabled_from_config()
    last_health, health_due, health_overdue = health_schedule(state)
    backup_enabled, last_backup, backup_due, backup_overdue = backup_schedule(state)
    report = latest_health_report()
    git = git_sync_state()
    backup = backup_configuration()
    return {
        "state": state,
        "health": {
            "last": last_health,
            "due": health_due,
            "overdue": health_overdue,
            "report": report,
        },
        "backup": {
            "enabled": backup_enabled,
            "last": last_backup,
            "due": backup_due,
            "overdue": backup_overdue,
            "config": backup,
        },
        "git": git,
    }
