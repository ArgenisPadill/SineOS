#!/usr/bin/env bash
# SineOS
# Nombre: install-sineos-maintenance.sh
# Propósito: instalar la aplicación nativa y el recordatorio trimestral de mantenimiento.
# Categoría: pilar / instalación
# Estado: pendiente de validación
# Plataforma: Debian 13 / XFCE
# Reejecutable: sí
# Privilegios: usuario normal
# Documentación: Documentation/Operations/Maintenance.md

set -euo pipefail

APP_NAME="SineOS Mantenimiento"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
APP="$REPO_ROOT/Apps/Maintenance/sineos-maintenance.py"
CORE="$REPO_ROOT/Apps/Maintenance/maintenance_core.py"
RUNNER="$REPO_ROOT/Scripts/Maintenance/run-health-audit-interactive.sh"
LOCAL_BIN="$HOME/.local/bin"
APP_LINK="$LOCAL_BIN/sineos-maintenance"
DESKTOP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$DESKTOP_DIR/sineos-maintenance.desktop"
SYSTEMD_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="$SYSTEMD_DIR/sineos-maintenance-reminder.service"
TIMER_FILE="$SYSTEMD_DIR/sineos-maintenance-reminder.timer"
STATE_DIR="$HOME/.local/state/sineos-maintenance"
CONFIG_DIR="$HOME/.config/sineos"
CONFIG_FILE="$CONFIG_DIR/maintenance.env"

fail(){ printf 'ERROR: %s\n' "$*" >&2; exit 1; }
ok(){ printf 'OK: %s\n' "$*"; }
have(){ command -v "$1" >/dev/null 2>&1; }

check_dependencies(){
    [[ -f "$APP" ]] || fail "No existe $APP"
    [[ -f "$CORE" ]] || fail "No existe $CORE"
    [[ -f "$RUNNER" ]] || fail "No existe $RUNNER"
    have python3 || fail "Falta python3"
    have git || fail "Falta git"
    have notify-send || fail "Falta notify-send (libnotify-bin)"
    have exo-open || fail "Falta exo-open (libexo)"
    python3 -c 'import gi; gi.require_version("Gtk","3.0"); from gi.repository import Gtk' >/dev/null 2>&1 \
        || fail "Falta GTK3/PyGObject (python3-gi, gir1.2-gtk-3.0)"
}

install_all(){
    check_dependencies
    mkdir -p "$LOCAL_BIN" "$DESKTOP_DIR" "$SYSTEMD_DIR" "$STATE_DIR" "$CONFIG_DIR"
    chmod 700 "$STATE_DIR" "$CONFIG_DIR"
    chmod 755 "$APP" "$CORE" "$RUNNER"
    ln -sfn "$APP" "$APP_LINK"

    if [[ ! -e "$CONFIG_FILE" ]]; then
        cat > "$CONFIG_FILE" <<'EOF'
# SineOS · Mantenimiento
# El backup permanece deshabilitado hasta completar TD-021.
SINEOS_BACKUP_ENABLED=0
# SINEOS_BACKUP_ROOT=/ruta/del/disco/SineOsBackups
EOF
        chmod 600 "$CONFIG_FILE"
    fi

    cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=$APP_NAME
Comment=Salud trimestral, respaldo externo y validación con GitHub
Exec=$APP_LINK
Icon=utilities-system-monitor
Terminal=false
Categories=System;Utility;
StartupNotify=true
EOF
    chmod 644 "$DESKTOP_FILE"

    cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=SineOS - Recordatorio de mantenimiento trimestral

[Service]
Type=oneshot
ExecStart=$APP_LINK --notify
EOF

    cat > "$TIMER_FILE" <<'EOF'
[Unit]
Description=SineOS - Evaluar recordatorio de mantenimiento

[Timer]
OnCalendar=daily
Persistent=true
RandomizedDelaySec=15m
Unit=sineos-maintenance-reminder.service

[Install]
WantedBy=timers.target
EOF

    chmod 644 "$SERVICE_FILE" "$TIMER_FILE"
    if have update-desktop-database; then
        update-desktop-database "$DESKTOP_DIR" >/dev/null 2>&1 || true
    fi

    systemctl --user daemon-reload
    systemctl --user enable --now sineos-maintenance-reminder.timer

    ok "Aplicación instalada: $APP_LINK"
    ok "Lanzador: $DESKTOP_FILE"
    ok "Timer: sineos-maintenance-reminder.timer"
    ok "Estado local: $STATE_DIR"
    ok "Configuración: $CONFIG_FILE"
}

show_status(){
    check_dependencies
    printf '%s\n' "$APP_NAME"
    printf 'Aplicación : %s\n' "$([[ -L "$APP_LINK" ]] && echo instalada || echo no-installada)"
    printf 'Timer habilitado : %s\n' "$(systemctl --user is-enabled sineos-maintenance-reminder.timer 2>/dev/null || true)"
    printf 'Timer activo     : %s\n' "$(systemctl --user is-active sineos-maintenance-reminder.timer 2>/dev/null || true)"
    echo
    python3 "$APP" --status || true
}

adopt_current(){
    check_dependencies
    python3 "$APP" --adopt-current
}

uninstall_all(){
    systemctl --user disable --now sineos-maintenance-reminder.timer >/dev/null 2>&1 || true
    rm -f "$TIMER_FILE" "$SERVICE_FILE" "$DESKTOP_FILE" "$APP_LINK"
    systemctl --user daemon-reload
    if have update-desktop-database; then
        update-desktop-database "$DESKTOP_DIR" >/dev/null 2>&1 || true
    fi
    ok "Integración retirada. El estado local y maintenance.env se conservaron."
}

case "${1:-install}" in
    install) install_all ;;
    status) show_status ;;
    adopt-current) adopt_current ;;
    uninstall) uninstall_all ;;
    *) echo "Uso: $0 {install|status|adopt-current|uninstall}"; exit 2 ;;
esac
