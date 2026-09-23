#!/usr/bin/env bash
set -euo pipefail

APP_NAME="SineOS Privacidad de red"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
APP="$REPO_ROOT/Apps/NetworkPrivacy/sineos-network-privacy.py"
POLICY="$REPO_ROOT/Apps/NetworkPrivacy/network_policy.py"
DESKTOP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$DESKTOP_DIR/sineos-network-privacy.desktop"
STATE_DIR="$HOME/.local/state/sineos-network-privacy"

fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
ok() { printf 'OK: %s\n' "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }

check_dependencies() {
    [[ -f "$APP" ]] || fail "No existe $APP"
    [[ -f "$POLICY" ]] || fail "No existe $POLICY"
    have python3 || fail "Falta python3"
    have nmcli || fail "Falta nmcli / NetworkManager"
    have dig || fail "Falta dig (dnsutils)"
    have getent || fail "Falta getent"
    python3 -c 'import gi; gi.require_version("Gtk","3.0"); from gi.repository import Gtk' \
        >/dev/null 2>&1 || fail "Falta GTK3/PyGObject (python3-gi, gir1.2-gtk-3.0)"
}

install_launcher() {
    check_dependencies
    mkdir -p "$DESKTOP_DIR" "$STATE_DIR"
    chmod 700 "$STATE_DIR"
    chmod 755 "$APP" "$POLICY"

    cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=$APP_NAME
Comment=Control de DNSCrypt y privacidad de la conexión
Exec=$APP
Icon=network-wireless
Terminal=false
Categories=Network;Internet;
StartupNotify=true
EOF
    chmod 644 "$DESKTOP_FILE"
    if have update-desktop-database; then
        update-desktop-database "$DESKTOP_DIR" >/dev/null 2>&1 || true
    fi
    ok "Lanzador instalado en $DESKTOP_FILE"
    ok "Busca '$APP_NAME' en Internet dentro del menú de XFCE."
}

show_status() {
    printf '%s\n' "$APP_NAME"
    printf 'Aplicación : %s\n' "$([[ -x "$APP" ]] && echo disponible || echo no-disponible)"
    printf 'Lanzador   : %s\n' "$([[ -f "$DESKTOP_FILE" ]] && echo instalado || echo no-instalado)"
    printf 'DNSCrypt   : %s\n' "$(systemctl is-active dnscrypt-proxy.service 2>/dev/null || true)"
    printf 'Estado     : %s\n' "$STATE_DIR"
}

uninstall_launcher() {
    rm -f "$DESKTOP_FILE"
    if have update-desktop-database; then
        update-desktop-database "$DESKTOP_DIR" >/dev/null 2>&1 || true
    fi
    ok "Lanzador retirado. No se modificó NetworkManager ni el estado de perfiles."
}

case "${1:-install}" in
    install) install_launcher ;;
    status) show_status ;;
    uninstall) uninstall_launcher ;;
    *) echo "Uso: $0 {install|status|uninstall}"; exit 2 ;;
esac
