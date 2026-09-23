#!/usr/bin/env bash
# ==============================================================================
# SineOS XFCE macOS-like
# Instalador reproducible para Debian + XFCE
#
# Objetivo:
#   - Partir de una instalación limpia de Debian.
#   - Instalar XFCE y dependencias visuales desde repositorios oficiales.
#   - Crear una barra superior translúcida tipo macOS.
#   - Crear un Dock inferior auto-ocultable.
#   - Aplicar tema, iconos, tipografías, cursor, compositor y wallpaper.
#   - NO modificar audio, VPN, TLP, suspensión, kernel ni firmware.
#
# Uso recomendado:
#   bash sineos-xfce-macos.sh install
#
# Si se ejecuta desde una Debian mínima sin sesión gráfica:
#   1. Instala XFCE y los paquetes.
#   2. Programa la personalización para el primer inicio de sesión XFCE.
#   3. Reinicia e inicia sesión.
#
# Comandos:
#   install        Instala XFCE/dependencias y aplica o programa el diseño.
#   apply          Aplica el diseño en una sesión XFCE activa.
#   status         Muestra el estado.
#   restore        Restaura el último respaldo.
#   packages       Solo instala dependencias.
#   help           Ayuda.
#
# Licencia sugerida para GitHub: MIT
# ==============================================================================

set -Eeuo pipefail

APP_NAME="SineOS XFCE macOS-like"
VERSION="4.0.0"

THEME="Arc-Dark"
ICON_THEME="Papirus-Dark"
UI_FONT="Noto Sans 10"
TITLE_FONT="Noto Sans SemiBold 10"
MONO_FONT="JetBrains Mono 10"
CURSOR_SIZE="24"

STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/sineos-xfce-macos"
BACKUP_DIR="$STATE_DIR/backups"
LAST_BACKUP="$STATE_DIR/last-backup"
MARKER="$STATE_DIR/layout-applied"

GTK_DIR="$HOME/.config/gtk-3.0"
GTK_CSS="$GTK_DIR/gtk.css"
AUTOSTART_DIR="$HOME/.config/autostart"
FIRST_LOGIN_DESKTOP="$AUTOSTART_DIR/sineos-xfce-first-login.desktop"
LOCAL_BIN="$HOME/.local/bin"
INSTALLED_SCRIPT="$LOCAL_BIN/sineos-xfce-macos"

CSS_START='/* --- SINEOS-XFCE-MACOS START --- */'
CSS_END='/* --- SINEOS-XFCE-MACOS END --- */'

TOP_PANEL=1
BOTTOM_PANEL=2

TOP_PLUGINS=(101 102 103 104 105 106 107 108)
BOTTOM_PLUGIN=201

SELF_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
FIRST_LOGIN_MODE=0

# ------------------------------------------------------------------------------
# Utilidades
# ------------------------------------------------------------------------------

log()  { printf '\n\033[1;36m>>> %s\033[0m\n' "$*"; }
ok()   { printf '\033[1;32mOK:\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33mAVISO:\033[0m %s\n' "$*"; }
fail() { printf '\033[1;31mERROR:\033[0m %s\n' "$*" >&2; }

die() {
    fail "$*"
    exit 1
}

have() { command -v "$1" >/dev/null 2>&1; }

is_debian() {
    [[ -r /etc/os-release ]] || return 1
    # shellcheck disable=SC1091
    . /etc/os-release
    [[ "${ID:-}" == "debian" ]]
}

debian_major() {
    # shellcheck disable=SC1091
    . /etc/os-release
    printf '%s\n' "${VERSION_ID%%.*}"
}

is_xfce_session() {
    [[ "${XDG_CURRENT_DESKTOP:-}" == *XFCE* ]] &&
    [[ -n "${DISPLAY:-}" ]] &&
    [[ -n "${DBUS_SESSION_BUS_ADDRESS:-}" ]]
}

as_root() {
    if [[ "$EUID" -eq 0 ]]; then
        "$@"
    elif have sudo; then
        sudo "$@"
    else
        die "Necesito privilegios administrativos. Instala sudo o ejecuta como root."
    fi
}

pkg_available() {
    apt-cache show "$1" >/dev/null 2>&1
}

pkg_installed() {
    dpkg-query -W -f='${Status}' "$1" 2>/dev/null |
        grep -q '^install ok installed$'
}

ensure_user_mode() {
    [[ "$EUID" -ne 0 ]] ||
        die "Los comandos apply/status/restore deben ejecutarse como el usuario del escritorio, sin sudo."
}

ensure_xfce_session() {
    ensure_user_mode
    is_xfce_session ||
        die "Este comando debe ejecutarse dentro de una sesión XFCE activa."
}

# ------------------------------------------------------------------------------
# Paquetes
# ------------------------------------------------------------------------------

install_packages() {
    is_debian || die "Este instalador está diseñado para Debian."

    local major
    major="$(debian_major)"

    log "Debian detectado: versión principal $major"
    log "Actualizando índices APT"
    as_root apt-get update

    # Paquetes base. Todos proceden de repositorios oficiales de Debian.
    local requested=(
        task-xfce-desktop
        lightdm
        xfce4-goodies
        xfce4-whiskermenu-plugin
        xfce4-notifyd
        xfce4-power-manager
        xfce4-pulseaudio-plugin
        network-manager-applet
        nm-connection-editor
        blueman
        bluez
        pavucontrol
        mate-polkit
        light-locker
        arc-theme
        papirus-icon-theme
        fonts-jetbrains-mono
        breeze-cursor-theme
        xdg-user-dirs
        dbus-x11
        libnotify-bin
    )

    # Noto cambia de metapaquete según instalación/version.
    if pkg_available fonts-noto-core; then
        requested+=(fonts-noto-core)
    elif pkg_available fonts-noto; then
        requested+=(fonts-noto)
    fi

    # Menú global.
    local optional=(
        xfce4-appmenu-plugin
        appmenu-registrar
        appmenu-gtk3-module
        appmenu-gtk2-module
    )

    # Docklike está disponible en Debian 13+; si no existe usaremos tasklist
    # del propio XFCE como fallback, sin descargar binarios externos.
    if pkg_available xfce4-docklike-plugin; then
        optional+=(xfce4-docklike-plugin)
    fi

    local installable=()
    local missing=()
    local p

    for p in "${requested[@]}"; do
        if pkg_available "$p"; then
            installable+=("$p")
        else
            missing+=("$p")
        fi
    done

    for p in "${optional[@]}"; do
        if pkg_available "$p"; then
            installable+=("$p")
        else
            warn "Paquete opcional no disponible en esta versión: $p"
        fi
    done

    if ((${#missing[@]})); then
        warn "Algunos paquetes base no aparecen en los repositorios configurados:"
        printf '  - %s\n' "${missing[@]}"
        echo
        warn "Continuaré con los disponibles; APT no será modificado con repositorios externos."
    fi

    log "Instalando entorno y dependencias"
    as_root apt-get install -y "${installable[@]}"

    # Una instalación mínima necesita arrancar en modo gráfico.
    if have systemctl && [[ "$(ps -p 1 -o comm= 2>/dev/null)" == "systemd" ]]; then
        log "Preparando arranque gráfico"
        as_root systemctl set-default graphical.target >/dev/null 2>&1 || true

        # No sustituimos un display manager existente.
        if ! systemctl status display-manager.service >/dev/null 2>&1; then
            as_root systemctl enable lightdm.service >/dev/null 2>&1 || true
        fi
    fi

    ok "Paquetes instalados."

    if pkg_installed xfce4-docklike-plugin; then
        ok "Dock: xfce4-docklike-plugin"
    else
        warn "Docklike no está disponible; se usará la lista de ventanas de XFCE como fallback."
    fi

    if pkg_installed xfce4-appmenu-plugin; then
        ok "Menú global: xfce4-appmenu-plugin"
    else
        warn "AppMenu no está disponible; la barra superior funcionará sin menú global."
    fi
}

# ------------------------------------------------------------------------------
# Instalación local y primer inicio
# ------------------------------------------------------------------------------

install_local_copy() {
    mkdir -p "$LOCAL_BIN" "$AUTOSTART_DIR" "$STATE_DIR"
    cp -f "$SELF_PATH" "$INSTALLED_SCRIPT"
    chmod +x "$INSTALLED_SCRIPT"
    ok "Copia local: $INSTALLED_SCRIPT"
}

schedule_first_login() {
    install_local_copy

    cat > "$FIRST_LOGIN_DESKTOP" <<EOF
[Desktop Entry]
Type=Application
Version=1.0
Name=SineOS XFCE - configuración inicial
Comment=Aplica una sola vez el diseño SineOS al iniciar XFCE
Exec=sh -lc 'sleep 8; "$INSTALLED_SCRIPT" apply --first-login'
OnlyShowIn=XFCE;
X-GNOME-Autostart-enabled=true
Terminal=false
NoDisplay=true
EOF

    ok "Personalización programada para el primer inicio de sesión XFCE."
}

# ------------------------------------------------------------------------------
# Respaldo
# ------------------------------------------------------------------------------

make_backup() {
    mkdir -p "$BACKUP_DIR"

    local stamp backup
    stamp="$(date '+%Y%m%d-%H%M%S')"
    backup="$BACKUP_DIR/$stamp"
    mkdir -p "$backup"

    log "Creando respaldo"

    if [[ -d "$HOME/.config/xfce4" ]]; then
        cp -a "$HOME/.config/xfce4" "$backup/xfce4"
    fi

    if [[ -f "$GTK_CSS" ]]; then
        mkdir -p "$backup/gtk-3.0"
        cp -a "$GTK_CSS" "$backup/gtk-3.0/gtk.css"
        printf 'present\n' > "$backup/gtk-css-state"
    else
        printf 'absent\n' > "$backup/gtk-css-state"
    fi

    if [[ -f "$FIRST_LOGIN_DESKTOP" ]]; then
        cp -a "$FIRST_LOGIN_DESKTOP" "$backup/first-login.desktop"
    fi

    printf '%s\n' "$backup" > "$LAST_BACKUP"
    ok "Respaldo: $backup"
}

# ------------------------------------------------------------------------------
# XFConf
# ------------------------------------------------------------------------------

set_prop() {
    local channel="$1" prop="$2" type="$3" value="$4"

    if xfconf-query -c "$channel" -p "$prop" >/dev/null 2>&1; then
        xfconf-query -c "$channel" -p "$prop" -s "$value" >/dev/null
    else
        xfconf-query -c "$channel" -p "$prop" -n -t "$type" -s "$value" >/dev/null
    fi
}

set_rgba() {
    local prop="$1" r="$2" g="$3" b="$4" a="$5"

    xfconf-query -c xfce4-panel -p "$prop" -r >/dev/null 2>&1 || true
    xfconf-query -c xfce4-panel -p "$prop" -n -a \
        -t double -s "$r" \
        -t double -s "$g" \
        -t double -s "$b" \
        -t double -s "$a" >/dev/null
}

set_int_array() {
    local prop="$1"
    shift
    local args=()
    local n

    for n in "$@"; do
        args+=( -t int -s "$n" )
    done

    xfconf-query -c xfce4-panel -p "$prop" -r >/dev/null 2>&1 || true
    xfconf-query -c xfce4-panel -p "$prop" -n -a "${args[@]}" >/dev/null
}

create_plugin() {
    local id="$1" name="$2"
    local prop="/plugins/plugin-$id"

    xfconf-query -c xfce4-panel -p "$prop" -r -R >/dev/null 2>&1 || true
    xfconf-query -c xfce4-panel -p "$prop" -n -t string -s "$name" >/dev/null
}

# ------------------------------------------------------------------------------
# Tema visual
# ------------------------------------------------------------------------------

find_theme() {
    local theme="$1" d
    for d in \
        "$HOME/.themes/$theme" \
        "$HOME/.local/share/themes/$theme" \
        "/usr/share/themes/$theme"
    do
        [[ -d "$d" ]] && return 0
    done
    return 1
}

find_icon_theme() {
    local theme="$1" d
    for d in \
        "$HOME/.icons/$theme" \
        "$HOME/.local/share/icons/$theme" \
        "/usr/share/icons/$theme"
    do
        [[ -d "$d" ]] && return 0
    done
    return 1
}

pick_cursor() {
    local c
    for c in Breeze_Snow breeze_cursors Breeze; do
        if find_icon_theme "$c"; then
            printf '%s\n' "$c"
            return 0
        fi
    done
    return 1
}

apply_theme() {
    log "Aplicando tema, iconos y tipografía"

    if find_theme "$THEME"; then
        set_prop xsettings /Net/ThemeName string "$THEME"
        set_prop xfwm4 /general/theme string "$THEME"
    else
        warn "No encontré $THEME; mantengo el tema GTK actual."
    fi

    if find_icon_theme "$ICON_THEME"; then
        set_prop xsettings /Net/IconThemeName string "$ICON_THEME"
    fi

    set_prop xsettings /Gtk/FontName string "$UI_FONT"
    set_prop xsettings /Gtk/MonospaceFontName string "$MONO_FONT"
    set_prop xfwm4 /general/title_font string "$TITLE_FONT"

    set_prop xsettings /Xft/Antialias int 1
    set_prop xsettings /Xft/Hinting int 1
    set_prop xsettings /Xft/HintStyle string hintslight
    set_prop xsettings /Xft/RGBA string rgb

    local cursor=""
    cursor="$(pick_cursor 2>/dev/null || true)"
    if [[ -n "$cursor" ]]; then
        set_prop xsettings /Gtk/CursorThemeName string "$cursor"
        set_prop xsettings /Gtk/CursorThemeSize int "$CURSOR_SIZE"
    fi

    # Solo compositor visual. No tocamos energía, vídeo, kernel ni drivers.
    set_prop xfwm4 /general/use_compositing bool true
    set_prop xfwm4 /general/show_frame_shadow bool true
    set_prop xfwm4 /general/show_popup_shadow bool true
    set_prop xfwm4 /general/show_dock_shadow bool true
    set_prop xfwm4 /general/frame_opacity int 100
    set_prop xfwm4 /general/inactive_opacity int 100

    ok "Apariencia base aplicada."
}

# ------------------------------------------------------------------------------
# Paneles
# ------------------------------------------------------------------------------

configure_top_panel() {
    log "Configurando barra superior"

    set_prop xfce4-panel "/panels/panel-$TOP_PANEL/position" string 'p=6;x=0;y=0'
    set_prop xfce4-panel "/panels/panel-$TOP_PANEL/length" uint 100
    set_prop xfce4-panel "/panels/panel-$TOP_PANEL/length-adjust" bool false
    set_prop xfce4-panel "/panels/panel-$TOP_PANEL/size" uint 30
    set_prop xfce4-panel "/panels/panel-$TOP_PANEL/icon-size" uint 18
    set_prop xfce4-panel "/panels/panel-$TOP_PANEL/nrows" uint 1
    set_prop xfce4-panel "/panels/panel-$TOP_PANEL/position-locked" bool true
    set_prop xfce4-panel "/panels/panel-$TOP_PANEL/autohide-behavior" uint 0
    set_prop xfce4-panel "/panels/panel-$TOP_PANEL/background-style" uint 1
    set_rgba "/panels/panel-$TOP_PANEL/background-rgba" 0.035 0.045 0.065 0.72
    set_prop xfce4-panel "/panels/panel-$TOP_PANEL/enter-opacity" uint 100
    set_prop xfce4-panel "/panels/panel-$TOP_PANEL/leave-opacity" uint 100

    # Menú de inicio.
    create_plugin 101 whiskermenu

    # Menú global de la aplicación activa, si existe.
    local ids=(101)
    if pkg_installed xfce4-appmenu-plugin; then
        create_plugin 102 appmenu
        ids+=(102)
    fi

    # Separador expansible: izquierda dinámica / derecha fija.
    create_plugin 103 separator
    set_prop xfce4-panel /plugins/plugin-103/expand bool true
    set_prop xfce4-panel /plugins/plugin-103/style uint 0
    ids+=(103)

    # Estado del sistema.
    create_plugin 104 systray
    create_plugin 105 pulseaudio
    create_plugin 106 power-manager-plugin
    create_plugin 107 clock
    create_plugin 108 actions

    ids+=(104 105 106 107 108)
    set_int_array "/panels/panel-$TOP_PANEL/plugin-ids" "${ids[@]}"

    # Reloj simple y legible.
    set_prop xfce4-panel /plugins/plugin-107/digital-format string '%a %d %b  %H:%M'

    ok "Barra superior lista."
}

configure_bottom_panel() {
    log "Configurando Dock inferior"

    set_prop xfce4-panel "/panels/panel-$BOTTOM_PANEL/position" string 'p=10;x=0;y=0'
    set_prop xfce4-panel "/panels/panel-$BOTTOM_PANEL/length-adjust" bool true
    set_prop xfce4-panel "/panels/panel-$BOTTOM_PANEL/length" uint 1
    set_prop xfce4-panel "/panels/panel-$BOTTOM_PANEL/size" uint 56
    set_prop xfce4-panel "/panels/panel-$BOTTOM_PANEL/icon-size" uint 42
    set_prop xfce4-panel "/panels/panel-$BOTTOM_PANEL/nrows" uint 1
    set_prop xfce4-panel "/panels/panel-$BOTTOM_PANEL/position-locked" bool true

    # 2 = siempre auto-ocultable.
    # No reiniciamos xfce4-panel: XFConf aplica el cambio en vivo.
    set_prop xfce4-panel "/panels/panel-$BOTTOM_PANEL/autohide-behavior" uint 2

    set_prop xfce4-panel "/panels/panel-$BOTTOM_PANEL/background-style" uint 1
    set_rgba "/panels/panel-$BOTTOM_PANEL/background-rgba" 0.045 0.055 0.075 0.84
    set_prop xfce4-panel "/panels/panel-$BOTTOM_PANEL/enter-opacity" uint 100
    set_prop xfce4-panel "/panels/panel-$BOTTOM_PANEL/leave-opacity" uint 100

    if pkg_installed xfce4-docklike-plugin; then
        create_plugin "$BOTTOM_PLUGIN" docklike
        set_int_array "/panels/panel-$BOTTOM_PANEL/plugin-ids" "$BOTTOM_PLUGIN"
        ok "Docklike activado."
    else
        # Fallback para versiones de Debian donde Docklike no está empaquetado.
        # Sigue siendo auto-ocultable, pero no ofrece fijado de apps equivalente.
        create_plugin "$BOTTOM_PLUGIN" tasklist
        set_prop xfce4-panel "/plugins/plugin-$BOTTOM_PLUGIN/show-labels" bool false
        set_int_array "/panels/panel-$BOTTOM_PANEL/plugin-ids" "$BOTTOM_PLUGIN"
        warn "Usando tasklist como Dock de compatibilidad."
    fi
}

configure_panel_layout() {
    log "Construyendo diseño de dos paneles"

    # Declaramos exactamente dos paneles.
    set_int_array /panels "$TOP_PANEL" "$BOTTOM_PANEL"

    configure_top_panel
    configure_bottom_panel

    ok "Estructura de paneles aplicada."
}

# ------------------------------------------------------------------------------
# CSS
# ------------------------------------------------------------------------------

write_css() {
    log "Aplicando acabado visual"

    mkdir -p "$GTK_DIR"

    local tmp
    tmp="$(mktemp)"

    if [[ -f "$GTK_CSS" ]]; then
        awk -v start="$CSS_START" -v end="$CSS_END" '
            $0==start {skip=1; next}
            $0==end   {skip=0; next}
            !skip     {print}
        ' "$GTK_CSS" > "$tmp"
    else
        : > "$tmp"
    fi

    cat >> "$tmp" <<'CSS'

/* --- SINEOS-XFCE-MACOS START --- */

/*
 * El panel inferior se muestra rápido al tocar el borde y tarda un poco
 * en ocultarse para evitar parpadeos accidentales.
 */
#XfcePanelWindow {
    -XfcePanelWindow-popup-delay: 120;
    -XfcePanelWindow-popdown-delay: 1800;
    -XfcePanelWindow-autohide-size: 2;
}

#XfcePanelWindow,
.xfce4-panel .background {
    color: #f6f7fb;
    font-family: "Noto Sans";
    font-size: 10pt;
}

#xfce-panel-button,
#xfce-panel-toggle-button,
#whiskermenu-button,
#applicationmenu-button,
#actions-button,
#clock-button,
#pulseaudio-button,
#showdesktop-button,
#windowmenu-button,
#sn-button {
    background-image: none;
    background-color: transparent;
    border: 0;
    border-radius: 9px;
    box-shadow: none;
    margin: 2px;
    padding: 2px 7px;
    color: #f6f7fb;
}

#xfce-panel-button:hover,
#xfce-panel-toggle-button:hover,
#whiskermenu-button:hover,
#applicationmenu-button:hover,
#actions-button:hover,
#clock-button:hover,
#pulseaudio-button:hover,
#sn-button:hover {
    background-color: rgba(255,255,255,0.10);
}

#xfce-panel-toggle-button:checked,
#xfce-panel-toggle-button:active,
#whiskermenu-button:checked {
    background-color: rgba(255,255,255,0.14);
}

/* Menú global superior. */
.xfce4-panel menubar,
.xfce4-panel menubar > menuitem {
    background: transparent;
    color: #f6f7fb;
    border-radius: 7px;
    padding: 2px 5px;
}

.xfce4-panel menubar > menuitem:hover {
    background-color: rgba(255,255,255,0.10);
}

/* Botones del Dock / tasklist. */
.xfce4-panel .tasklist .toggle,
.xfce4-panel button {
    box-shadow: none;
}

.xfce4-panel .tasklist .toggle:hover {
    background-color: rgba(255,255,255,0.09);
    border-radius: 10px;
}

menu,
.context-menu {
    border-radius: 10px;
}

/* --- SINEOS-XFCE-MACOS END --- */
CSS

    mv "$tmp" "$GTK_CSS"
    ok "CSS aplicado."
}

# ------------------------------------------------------------------------------
# Wallpaper
# ------------------------------------------------------------------------------

create_wallpaper() {
    log "Creando fondo de pantalla"

    local pics wallpaper prop count=0
    pics="$(xdg-user-dir PICTURES 2>/dev/null || true)"
    [[ -n "$pics" ]] || pics="$HOME/Pictures"

    mkdir -p "$pics/Wallpapers"
    wallpaper="$pics/Wallpapers/sineos-macos-dark.svg"

    cat > "$wallpaper" <<'SVG'
<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
  <defs>
    <linearGradient id="base" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0e1420"/>
      <stop offset="0.50" stop-color="#18273a"/>
      <stop offset="1" stop-color="#090e17"/>
    </linearGradient>
    <radialGradient id="blue">
      <stop offset="0" stop-color="#4f8cff" stop-opacity=".32"/>
      <stop offset="1" stop-color="#4f8cff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="violet">
      <stop offset="0" stop-color="#9c6bff" stop-opacity=".20"/>
      <stop offset="1" stop-color="#9c6bff" stop-opacity="0"/>
    </radialGradient>
    <filter id="blur">
      <feGaussianBlur stdDeviation="55"/>
    </filter>
  </defs>
  <rect width="1920" height="1080" fill="url(#base)"/>
  <ellipse cx="1510" cy="170" rx="620" ry="470" fill="url(#blue)" filter="url(#blur)"/>
  <ellipse cx="300" cy="900" rx="560" ry="430" fill="url(#violet)" filter="url(#blur)"/>
</svg>
SVG

    while IFS= read -r prop; do
        [[ -n "$prop" ]] || continue
        if xfconf-query -c xfce4-desktop -p "$prop" -s "$wallpaper" >/dev/null 2>&1; then
            ((count++)) || true
        fi
    done < <(
        xfconf-query -c xfce4-desktop -lv 2>/dev/null |
            awk '$1 ~ /\/last-image$/ {print $1}'
    )

    xfdesktop --reload >/dev/null 2>&1 || true

    if ((count > 0)); then
        ok "Wallpaper aplicado."
    else
        warn "Wallpaper creado, pero XFCE no expuso una propiedad last-image todavía."
    fi
}

# ------------------------------------------------------------------------------
# Aplicar
# ------------------------------------------------------------------------------

apply_layout() {
    ensure_xfce_session

    for cmd in xfconf-query xfce4-panel xfdesktop; do
        have "$cmd" || die "Falta $cmd. Ejecuta primero: $0 packages"
    done

    make_backup

    # Aplicamos la estructura una sola vez. Las ejecuciones posteriores
    # refrescan apariencia y comportamiento sin reconstruir el panel.
    if [[ ! -f "$MARKER" ]]; then
        configure_panel_layout
    else
        log "El layout ya estaba aplicado; no reconstruyo plugins."
        # Garantizamos que el Dock siga auto-ocultable.
        set_prop xfce4-panel "/panels/panel-$BOTTOM_PANEL/autohide-behavior" uint 2
    fi

    apply_theme
    write_css
    create_wallpaper

    mkdir -p "$STATE_DIR"
    printf '%s\n' "$VERSION" > "$MARKER"

    # El primer inicio ya cumplió su función.
    rm -f "$FIRST_LOGIN_DESKTOP"

    # IMPORTANTE:
    # No usamos 'xfce4-panel --restart'. XFConf actualiza los paneles en vivo.
    # Esto evita el problema observado en algunos equipos donde --restart
    # cierra el panel pero no vuelve a iniciarlo.

    echo
    echo "================================================================"
    echo " $APP_NAME v$VERSION"
    echo "================================================================"
    echo " Barra superior : fija, translúcida, menú global + estado"
    echo " Dock inferior  : auto-ocultable; aparece al tocar el borde"
    echo " Tema           : $THEME"
    echo " Iconos         : $ICON_THEME"
    echo " Tipografía     : $UI_FONT"
    echo
    if pkg_installed xfce4-docklike-plugin; then
        echo " Dock           : Docklike Taskbar"
    else
        echo " Dock           : tasklist de compatibilidad"
    fi
    echo
    echo "No se modificaron audio, Bluetooth, red, energía, kernel ni firmware."
    echo
    echo "Si algún detalle GTK no cambia inmediatamente, cierra sesión y vuelve"
    echo "a entrar una vez. NO es necesario reiniciar el sistema."
    echo "================================================================"
}

# ------------------------------------------------------------------------------
# Restore
# ------------------------------------------------------------------------------

restore_latest() {
    ensure_xfce_session

    [[ -f "$LAST_BACKUP" ]] || die "No existe un respaldo previo."
    local backup
    backup="$(cat "$LAST_BACKUP")"
    [[ -d "$backup" ]] || die "El respaldo ya no existe: $backup"

    log "Restaurando último respaldo"

    # Restauración de emergencia conocida y fiable:
    # detenemos panel, restauramos archivos, reiniciamos xfconfd y arrancamos
    # explícitamente el panel; NO usamos 'xfce4-panel --restart'.
    xfce4-panel --quit >/dev/null 2>&1 || true
    sleep 1

    if [[ -d "$backup/xfce4" ]]; then
        rm -rf "$HOME/.config/xfce4"
        cp -a "$backup/xfce4" "$HOME/.config/xfce4"
    fi

    local css_state="absent"
    [[ -f "$backup/gtk-css-state" ]] && css_state="$(cat "$backup/gtk-css-state")"

    mkdir -p "$GTK_DIR"
    if [[ "$css_state" == "present" && -f "$backup/gtk-3.0/gtk.css" ]]; then
        cp -a "$backup/gtk-3.0/gtk.css" "$GTK_CSS"
    else
        rm -f "$GTK_CSS"
    fi

    rm -f "$MARKER"

    pkill -x xfconfd >/dev/null 2>&1 || true
    sleep 2

    nohup xfce4-panel >/tmp/sineos-xfce-panel-restore.log 2>&1 &
    nohup xfdesktop >/tmp/sineos-xfdesktop-restore.log 2>&1 &
    sleep 3

    if pgrep -x xfce4-panel >/dev/null 2>&1; then
        ok "Paneles restaurados."
    else
        fail "El panel no arrancó automáticamente."
        echo "Registro: /tmp/sineos-xfce-panel-restore.log"
        echo "Puedes iniciarlo manualmente con: xfce4-panel"
        return 1
    fi
}

# ------------------------------------------------------------------------------
# Status
# ------------------------------------------------------------------------------

show_status() {
    echo "$APP_NAME v$VERSION"
    echo

    if [[ -r /etc/os-release ]]; then
        # shellcheck disable=SC1091
        . /etc/os-release
        echo "Sistema        : ${PRETTY_NAME:-desconocido}"
    fi

    echo "XFCE instalado : $(pkg_installed xfce4-panel && echo sí || echo no)"
    echo "Arc-Dark       : $(pkg_installed arc-theme && echo sí || echo no)"
    echo "Papirus        : $(pkg_installed papirus-icon-theme && echo sí || echo no)"
    echo "AppMenu        : $(pkg_installed xfce4-appmenu-plugin && echo sí || echo no)"
    echo "Docklike       : $(pkg_installed xfce4-docklike-plugin && echo sí || echo no)"
    echo "Aplicado       : $([[ -f "$MARKER" ]] && echo sí || echo no)"

    if is_xfce_session && have xfconf-query; then
        echo
        echo "Panel superior :"
        xfconf-query -c xfce4-panel -p "/panels/panel-$TOP_PANEL/position" 2>/dev/null || true
        echo "Panel inferior :"
        xfconf-query -c xfce4-panel -p "/panels/panel-$BOTTOM_PANEL/position" 2>/dev/null || true
        printf 'Auto-ocultación: '
        xfconf-query -c xfce4-panel -p "/panels/panel-$BOTTOM_PANEL/autohide-behavior" 2>/dev/null || true
    fi
}

# ------------------------------------------------------------------------------
# Flujo completo
# ------------------------------------------------------------------------------

install_all() {
    install_packages

    # Si se ejecuta como root directamente no podemos aplicar la configuración
    # del usuario de manera segura porque no tenemos su DBus de sesión.
    if [[ "$EUID" -eq 0 ]]; then
        warn "Los paquetes quedaron instalados."
        warn "Inicia sesión con el usuario normal en XFCE y ejecuta:"
        echo "  $SELF_PATH apply"
        return 0
    fi

    install_local_copy

    if is_xfce_session; then
        apply_layout
    else
        schedule_first_login

        echo
        echo "================================================================"
        echo " INSTALACIÓN DEL SISTEMA COMPLETADA"
        echo "================================================================"
        echo " XFCE y las dependencias ya están instaladas."
        echo
        echo " Como todavía no hay una sesión XFCE activa, el diseño se aplicará"
        echo " automáticamente la primera vez que inicies sesión en XFCE."
        echo
        echo " Si vienes de una instalación mínima, puedes reiniciar ahora:"
        echo "   sudo reboot"
        echo "================================================================"
    fi
}

show_help() {
    cat <<EOF
$APP_NAME v$VERSION

Uso:
  $0 install
      Instala XFCE y todos los paquetes disponibles y después aplica el diseño
      o lo programa para el primer inicio de sesión.

  $0 packages
      Solo instala los paquetes necesarios.

  $0 apply
      Aplica el diseño. Debe ejecutarse SIN sudo dentro de XFCE.

  $0 status
      Muestra estado de instalación y configuración.

  $0 restore
      Restaura el último respaldo de XFCE.

  $0 help
      Muestra esta ayuda.

Compatibilidad:
  - Debian 13+ : perfil completo con Docklike si el paquete está disponible.
  - Debian 12  : AppMenu está disponible; el Dock usa fallback si Docklike
                 no existe en los repositorios configurados.
  - No agrega PPAs, repositorios de Ubuntu ni binarios descargados de terceros.

Seguridad:
  - No toca kernel, firmware, Secure Boot, audio, NetworkManager, VPN, TLP
    ni configuración de suspensión.
  - No ejecuta 'xfce4-panel --restart'.
  - Crea un respaldo antes de modificar la configuración del usuario.
EOF
}

# ------------------------------------------------------------------------------
# Entrada
# ------------------------------------------------------------------------------

COMMAND="${1:-help}"
shift || true

for arg in "$@"; do
    case "$arg" in
        --first-login) FIRST_LOGIN_MODE=1 ;;
        *) die "Opción desconocida: $arg" ;;
    esac
done

case "$COMMAND" in
    install)  install_all ;;
    packages) install_packages ;;
    apply)    apply_layout ;;
    status)   show_status ;;
    restore)  restore_latest ;;
    help|-h|--help) show_help ;;
    *) show_help; exit 2 ;;
esac