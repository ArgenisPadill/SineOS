
cat > ~/Workspace/SineOS/Scripts/Audit/sineos-audit.sh <<'EOF'
#!/usr/bin/env bash

# ============================================================
# SineOS - Auditoría del sistema
# ============================================================
#
# Nombre:       sineos-audit.sh
# Versión:      1.0.0
# Propósito:    Diagnóstico de la plataforma SineOS
#
# IMPORTANTE:
#   Este script es de SOLO LECTURA.
#
#   NO:
#     - instala paquetes
#     - elimina paquetes
#     - modifica configuraciones
#     - reinicia servicios
#     - modifica Git
#     - modifica SSH
#     - modifica Podman
#     - modifica red
#
# Plataforma objetivo:
#   Debian GNU/Linux 13 (Trixie)
#   XFCE
#   Btrfs
#   Podman rootless
#
# ============================================================

set -u
set -o pipefail

# ------------------------------------------------------------
# Identidad del script
# ------------------------------------------------------------

SCRIPT_NAME="sineos-audit"
SCRIPT_VERSION="1.0.0"

TIMESTAMP="$(date '+%Y-%m-%d_%H-%M-%S')"

REPORT_DIR="${HOME}/Workspace/SineOS/Documentation/Audit"
REPORT_FILE="${REPORT_DIR}/${SCRIPT_NAME}-${TIMESTAMP}.txt"

mkdir -p "$REPORT_DIR"

# ------------------------------------------------------------
# Colores
# ------------------------------------------------------------

if [[ -t 1 ]]; then
    RED='\033[31m'
    GREEN='\033[32m'
    YELLOW='\033[33m'
    BLUE='\033[34m'
    CYAN='\033[36m'
    BOLD='\033[1m'
    RESET='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    CYAN=''
    BOLD=''
    RESET=''
fi

# ------------------------------------------------------------
# Contadores
# ------------------------------------------------------------

OK_COUNT=0
WARN_COUNT=0
ERROR_COUNT=0
INFO_COUNT=0

# ------------------------------------------------------------
# Funciones
# ------------------------------------------------------------

section() {
    echo
    echo "================================================================"
    echo " $1"
    echo "================================================================"
}

subsection() {
    echo
    echo "--- $1 ---"
}

ok() {
    echo -e "${GREEN}[ OK ]${RESET} $1"
    ((OK_COUNT+=1))
}

warn() {
    echo -e "${YELLOW}[WARN ]${RESET} $1"
    ((WARN_COUNT+=1))
}

error() {
    echo -e "${RED}[ERROR]${RESET} $1"
    ((ERROR_COUNT+=1))
}

info() {
    echo -e "${CYAN}[INFO ]${RESET} $1"
    ((INFO_COUNT+=1))
}

run_cmd() {
    echo
    echo "\$ $*"
    "$@" 2>&1 || true
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# ------------------------------------------------------------
# Encabezado
# ------------------------------------------------------------

{
    echo "================================================================"
    echo " SineOS - AUDITORÍA DEL SISTEMA"
    echo "================================================================"
    echo
    echo "Script:       ${SCRIPT_NAME}"
    echo "Versión:      ${SCRIPT_VERSION}"
    echo "Fecha:        $(date '+%Y-%m-%d %H:%M:%S %Z')"
    echo "Usuario:      ${USER}"
    echo "Host:         $(hostname)"
    echo "Reporte:      ${REPORT_FILE}"
    echo
    echo "IMPORTANTE:"
    echo "Este reporte es diagnóstico y no realiza modificaciones."
    echo
} | tee "$REPORT_FILE"

# ============================================================
# 01 - SISTEMA OPERATIVO
# ============================================================

{
section "01 - SISTEMA OPERATIVO"

subsection "Identificación"

run_cmd cat /etc/os-release

subsection "Kernel"

run_cmd uname -a

subsection "Arquitectura"

run_cmd uname -m

subsection "Hostname"

run_cmd hostnamectl

subsection "Uptime"

run_cmd uptime

if grep -qi "Debian GNU/Linux 13" /etc/os-release 2>/dev/null; then
    ok "Debian GNU/Linux 13 detectado."
else
    warn "La versión detectada no coincide con Debian GNU/Linux 13."
fi

} | tee -a "$REPORT_FILE"

# ============================================================
# 02 - HARDWARE
# ============================================================

{
section "02 - HARDWARE"

subsection "CPU"

run_cmd lscpu

subsection "Memoria"

run_cmd free -h

subsection "PCI"

if command_exists lspci; then
    run_cmd lspci
else
    warn "lspci no está disponible."
fi

subsection "USB"

if command_exists lsusb; then
    run_cmd lsusb
else
    warn "lsusb no está disponible."
fi

subsection "DMI / fabricante"

if command_exists dmidecode; then
    run_cmd sudo -n dmidecode -t system
else
    warn "dmidecode no está disponible."
fi

} | tee -a "$REPORT_FILE"

# ============================================================
# 03 - ALMACENAMIENTO / BTRFS
# ============================================================

{
section "03 - ALMACENAMIENTO Y BTRFS"

subsection "Dispositivos"

run_cmd lsblk -o NAME,SIZE,FSTYPE,FSVER,LABEL,UUID,MOUNTPOINTS

subsection "Uso de almacenamiento"

run_cmd df -hT

subsection "Montajes"

run_cmd findmnt

subsection "Btrfs"

if command_exists btrfs; then
    run_cmd btrfs filesystem show
    run_cmd btrfs filesystem usage /
else
    warn "Herramienta btrfs no disponible."
fi

subsection "Subvolúmenes"

if command_exists btrfs; then
    run_cmd btrfs subvolume list /
fi

} | tee -a "$REPORT_FILE"

# ============================================================
# 04 - MEMORIA / SWAP
# ============================================================

{
section "04 - MEMORIA Y SWAP"

run_cmd free -h

subsection "Swap"

run_cmd swapon --show

subsection "Memoria del kernel"

run_cmd cat /proc/meminfo

} | tee -a "$REPORT_FILE"

# ============================================================
# 05 - APT / DPkg
# ============================================================

{
section "05 - APT Y PAQUETES"

subsection "Versión de APT"

run_cmd apt --version

subsection "Repositorios"

run_cmd grep -RhsE '^[[:space:]]*deb ' /etc/apt/sources.list /etc/apt/sources.list.d 2>/dev/null

subsection "Paquetes pendientes"

run_cmd apt list --upgradable

subsection "Paquetes rotos"

run_cmd dpkg --audit

subsection "Paquetes configurados a medias"

run_cmd dpkg -C

subsection "Paquetes instalados"

info "Cantidad aproximada de paquetes instalados:"
dpkg-query -W -f='${binary:Package}\n' 2>/dev/null | wc -l

} | tee -a "$REPORT_FILE"

# ============================================================
# 06 - SERVICIOS SYSTEMD
# ============================================================

{
section "06 - SYSTEMD Y SERVICIOS"

subsection "Servicios fallidos"

FAILED="$(systemctl --failed --no-legend 2>/dev/null || true)"

if [[ -z "$FAILED" ]]; then
    ok "No se detectaron servicios systemd en estado failed."
else
    error "Se detectaron servicios systemd fallidos:"
    echo "$FAILED"
fi

subsection "Servicios activos"

run_cmd systemctl list-units --type=service --state=running --no-pager

subsection "Servicios habilitados"

run_cmd systemctl list-unit-files --state=enabled --no-pager

} | tee -a "$REPORT_FILE"

# ============================================================
# 07 - JOURNAL
# ============================================================

{
section "07 - JOURNAL / ERRORES DEL SISTEMA"

subsection "Errores del arranque actual"

run_cmd journalctl -p err -b --no-pager

subsection "Advertencias y errores recientes"

run_cmd journalctl -p warning..err -b --no-pager

subsection "Kernel"

run_cmd journalctl -k -b --no-pager

} | tee -a "$REPORT_FILE"

# ============================================================
# 08 - RED
# ============================================================

{
section "08 - RED"

subsection "Interfaces"

run_cmd ip -br address

subsection "Rutas"

run_cmd ip route

subsection "DNS"

if command_exists resolvectl; then
    run_cmd resolvectl status
else
    run_cmd cat /etc/resolv.conf
fi

subsection "Sockets escuchando"

run_cmd ss -tulpn

} | tee -a "$REPORT_FILE"

# ============================================================
# 09 - SEGURIDAD BÁSICA
# ============================================================

{
section "09 - SEGURIDAD BÁSICA"

subsection "Secure Boot"

if command_exists mokutil; then
    run_cmd mokutil --sb-state
else
    warn "mokutil no está instalado."
fi

subsection "EFI"

if [[ -d /sys/firmware/efi ]]; then
    ok "Sistema iniciado mediante UEFI."
else
    warn "No se detectó /sys/firmware/efi."
fi

subsection "Firewall"

if command_exists ufw; then
    run_cmd ufw status verbose
else
    info "ufw no está instalado."
fi

if command_exists nft; then
    run_cmd sudo -n nft list ruleset
else
    info "nft no está disponible."
fi

subsection "SSH"

if [[ -d "${HOME}/.ssh" ]]; then
    run_cmd ls -la "${HOME}/.ssh"
else
    info "No existe ~/.ssh."
fi

} | tee -a "$REPORT_FILE"

# ============================================================
# 10 - GIT
# ============================================================

{
section "10 - GIT"

subsection "Versión"

run_cmd git --version

subsection "Configuración global"

run_cmd git config --global --list

subsection "Repositorio SineOS"

cd "${HOME}/Workspace/SineOS" 2>/dev/null || true

run_cmd git status
run_cmd git remote -v
run_cmd git branch -vv
run_cmd git log --oneline --decorate --graph -5

subsection "Archivos potencialmente sensibles rastreados"

SENSITIVE_FILES="$(git ls-files | grep -Ei '(^|/)(\.env|.*\.pem|.*\.key|.*password.*|.*secret.*|.*token.*)$' || true)"

if [[ -z "$SENSITIVE_FILES" ]]; then
    ok "No se detectaron archivos sensibles conocidos rastreados por Git."
else
    warn "Se detectaron posibles archivos sensibles rastreados:"
    echo "$SENSITIVE_FILES"
fi

} | tee -a "$REPORT_FILE"

# ============================================================
# 11 - SSH / GITHUB
# ============================================================

{
section "11 - SSH Y GITHUB"

subsection "Archivos SSH"

if [[ -d "${HOME}/.ssh" ]]; then
    run_cmd find "${HOME}/.ssh" -maxdepth 1 -type f -printf '%f\n'
fi

subsection "Known Hosts"

if [[ -f "${HOME}/.ssh/known_hosts" ]]; then
    info "known_hosts existe."
else
    warn "No existe ~/.ssh/known_hosts."
fi

subsection "Prueba de GitHub"

if command_exists ssh; then
    run_cmd ssh -T -o BatchMode=yes -o ConnectTimeout=10 git@github.com
fi

} | tee -a "$REPORT_FILE"

# ============================================================
# 12 - PODMAN
# ============================================================

{
section "12 - PODMAN / CONTENEDORES"

if command_exists podman; then

    subsection "Versiones"

    run_cmd podman --version
    run_cmd buildah --version
    run_cmd skopeo --version
    run_cmd podman-compose version

    subsection "Podman info"

    run_cmd podman info

    subsection "Contenedores"

    run_cmd podman ps -a

    subsection "Imágenes"

    run_cmd podman images

    subsection "Volúmenes"

    run_cmd podman volume ls

    subsection "Redes"

    run_cmd podman network ls

else
    warn "Podman no está instalado."
fi

} | tee -a "$REPORT_FILE"

# ============================================================
# 13 - SINEOS CONTAINERS
# ============================================================

{
section "13 - ESTRUCTURA DE CONTENEDORES SINEOS"

CONTAINERS_DIR="${HOME}/Workspace/SineOS/Containers"

if [[ -d "$CONTAINERS_DIR" ]]; then

    subsection "Estructura"

    run_cmd tree -L 3 "$CONTAINERS_DIR"

    subsection "Archivos .env"

    ENV_FILES="$(find "$CONTAINERS_DIR" -type f -name '.env' -print 2>/dev/null || true)"

    if [[ -z "$ENV_FILES" ]]; then
        ok "No existen archivos .env."
    else
        warn "Se encontraron archivos .env. No se mostrará su contenido."
        echo "$ENV_FILES"
    fi

    subsection "Archivos potencialmente sensibles"

    run_cmd find "$CONTAINERS_DIR" -type f \
        \( \
        -name '*.key' \
        -o -name '*.pem' \
        -o -name '*.secret' \
        -o -iname '*password*' \
        -o -iname '*token*' \
        \) \
        -print

else
    warn "No existe ${CONTAINERS_DIR}"
fi

} | tee -a "$REPORT_FILE"

# ============================================================
# 14 - XFCE
# ============================================================

{
section "14 - XFCE"

subsection "Versión XFCE"

if command_exists xfce4-session; then
    run_cmd xfce4-session --version
fi

subsection "Panel"

if command_exists xfce4-panel; then
    run_cmd xfce4-panel --version
fi

subsection "Plugins PulseAudio"

if command_exists xfconf-query; then
    run_cmd xfconf-query -c xfce4-panel -lv
fi

subsection "Atajos multimedia"

if command_exists xfconf-query; then
    run_cmd xfconf-query -c xfce4-keyboard-shortcuts -lv
fi

} | tee -a "$REPORT_FILE"

# ============================================================
# 15 - AUDIO
# ============================================================

{
section "15 - AUDIO"

subsection "PulseAudio"

if command_exists pactl; then
    run_cmd pactl info
    run_cmd pactl list short sinks
    run_cmd pactl list short sources
else
    warn "pactl no está disponible."
fi

subsection "Dispositivos ALSA"

if command_exists aplay; then
    run_cmd aplay -l
fi

} | tee -a "$REPORT_FILE"

# ============================================================
# 16 - LIBINPUT
# ============================================================

{
section "16 - DISPOSITIVOS DE ENTRADA"

if command_exists libinput; then
    subsection "Dispositivos"

    run_cmd sudo -n libinput list-devices
else
    warn "libinput no está disponible."
fi

} | tee -a "$REPORT_FILE"

# ============================================================
# 17 - DISCO / SMART
# ============================================================

{
section "17 - SALUD DEL DISCO"

if command_exists smartctl; then

    subsection "Dispositivos SMART"

    run_cmd sudo -n smartctl --scan

else
    info "smartmontools no está instalado; no se puede realizar auditoría SMART."
fi

} | tee -a "$REPORT_FILE"

# ============================================================
# 18 - PROCESOS / RECURSOS
# ============================================================

{
section "18 - RECURSOS DEL SISTEMA"

subsection "Carga"

run_cmd uptime

subsection "Procesos principales"

run_cmd ps aux --sort=-%cpu | head -n 20

subsection "Memoria"

run_cmd ps aux --sort=-%mem | head -n 20

} | tee -a "$REPORT_FILE"

# ============================================================
# 19 - ENTORNO
# ============================================================

{
section "19 - ENTORNO DE USUARIO"

subsection "Shell"

run_cmd zsh --version

subsection "PATH"

echo "$PATH"

subsection "Herramientas"

for cmd in \
    code \
    git \
    zsh \
    eza \
    batcat \
    fzf \
    curl \
    wget \
    jq \
    tree \
    python3 \
    pip3 \
    node \
    npm
do
    if command_exists "$cmd"; then
        printf "%-15s : " "$cmd"
        "$cmd" --version 2>&1 | head -n 1 || true
    else
        printf "%-15s : no instalado\n" "$cmd"
    fi
done

} | tee -a "$REPORT_FILE"

# ============================================================
# 20 - RESUMEN
# ============================================================

{
section "20 - RESUMEN DE AUDITORÍA"

echo
echo "Versión del auditor: ${SCRIPT_VERSION}"
echo "Fecha: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo

echo "Resultados:"
echo "  OK          : ${OK_COUNT}"
echo "  Advertencias: ${WARN_COUNT}"
echo "  Errores     : ${ERROR_COUNT}"
echo "  Información  : ${INFO_COUNT}"

echo
echo "Reporte generado:"
echo "${REPORT_FILE}"

echo
echo "================================================================"
echo " FIN DE AUDITORÍA"
echo "================================================================"

} | tee -a "$REPORT_FILE"

# ------------------------------------------------------------
# Regresar al directorio original
# ------------------------------------------------------------

cd - >/dev/null 2>&1 || true

exit 0

EOF
