#!/usr/bin/env bash
# SineOS
# Nombre: bootstrap.sh
# Propósito: instalar dependencias base en Debian 13 limpio, sin desplegar servicios ni datos.
# Categoría: pilar / instalación
# Estado: PROPUESTO; validación en host Debian limpio PENDING
# Plataforma: Debian GNU/Linux 13 amd64
# Reejecutable: sí, para paquetes APT; Ollama instalado no se sobrescribe
# Privilegios: usuario ordinario con sudo SOLO en --apply
# Documentación: Documentation/Recovery/Migration-Checklist.md
set -Eeuo pipefail

MODE="dry-run"
SKIP_OLLAMA=0
OLLAMA_TARGET_VERSION="0.34.0"

info() { printf '[INFO] %s\n' "$*"; }
warn() { printf '[WARN] %s\n' "$*" >&2; }
die()  { printf '[ERROR] %s\n' "$*" >&2; exit 1; }

usage() {
  cat <<'HELP'
SineOS bootstrap para Debian 13 x86_64
Uso:
  bash Scripts/Bootstrap/bootstrap.sh --dry-run   # valor por defecto
  bash Scripts/Bootstrap/bootstrap.sh --apply
  bash Scripts/Bootstrap/bootstrap.sh --apply --skip-ollama
No instala aplicaciones ni restaura datos de contenedores. No modifica firewall,
servicios existentes, volumenes, credenciales, layout XFCE ni el repositorio Git.
El instalador oficial de Ollama se descarga por HTTPS, se comprueba con sh -n
y se ejecuta con OLLAMA_VERSION=0.34.0: su script remoto NO esta fijado por hash.
Revisar el script remoto antes de ejecutar --apply en entornos sensibles.
HELP
}

for arg in "$@"; do
  case "$arg" in
    --dry-run) MODE="dry-run" ;;
    --apply) MODE="apply" ;;
    --skip-ollama) SKIP_OLLAMA=1 ;;
    -h|--help) usage; exit 0 ;;
    *) die "Argumento desconocido: $arg" ;;
  esac
done

[[ "${EUID}" -ne 0 ]] || die "Ejecutar como usuario normal, no como root."
[[ -r /etc/os-release ]] || die "No se pudo identificar el sistema."
# shellcheck source=/etc/os-release
. /etc/os-release
[[ "${ID:-}" == "debian" && "${VERSION_ID:-}" == "13" ]] || die "Solo Debian 13 (Trixie)."
[[ "$(dpkg --print-architecture)" == "amd64" ]] || die "Esta versión inicial solo soporta amd64."
command -v apt-get >/dev/null || die "Falta apt-get."

PACKAGES=(
  ca-certificates curl git gnupg jq restic zstd
  podman podman-compose buildah skopeo uidmap passt slirp4netns
  fuse-overlayfs netavark aardvark-dns
  xfce4 xfce4-goodies lightdm arc-theme papirus-icon-theme
  fonts-noto fonts-jetbrains-mono
)

info "Plataforma validada para ejecución: Debian 13 amd64."
info "Modo: $MODE; version objetivo de Ollama: $OLLAMA_TARGET_VERSION."
if [[ "$MODE" == "dry-run" ]]; then
  printf '[DRY-RUN] sudo apt-get update\n[DRY-RUN] sudo apt-get install -y'
  printf ' %q' "${PACKAGES[@]}"
  printf '\n'
  if (( ! SKIP_OLLAMA )); then
    info "Ollama: instalar version fija $OLLAMA_TARGET_VERSION solo si no existe."
    warn "El script instalador remoto de Ollama no esta fijado por SHA256."
  fi
  info "No se instalan contenedores, modelos, stacks ni configuraciones de seguridad."
  exit 0
fi

command -v sudo >/dev/null || die "Se requiere sudo para instalar paquetes."
sudo -v || die "No se obtuvo autorización sudo."
info "Actualizando indice APT..."
sudo apt-get update
info "Instalando paquetes base y XFCE (sin aplicar layout personalizado)..."
sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y "${PACKAGES[@]}"

if (( ! SKIP_OLLAMA )); then
  if command -v ollama >/dev/null 2>&1; then
    warn "Ollama ya existe; no se reinstala ni cambia su version."
    ollama --version || true
  else
    command -v curl >/dev/null || die "Falta curl."
    tmp_installer="$(mktemp -t sineos-ollama-install.XXXXXX)"
    trap 'rm -f "$tmp_installer"' EXIT
    info "Descargando instalador oficial de Ollama por HTTPS."
    curl --fail --silent --show-error --location --retry 2 \
      https://ollama.com/install.sh -o "$tmp_installer"
    sh -n "$tmp_installer" || die "El instalador de Ollama no supera sh -n."
    warn "Integridad del script remoto NO verificada mediante SHA256 conocido."
    info "Instalando Ollama $OLLAMA_TARGET_VERSION mediante instalador oficial."
    OLLAMA_VERSION="$OLLAMA_TARGET_VERSION" sh "$tmp_installer"
    command -v ollama >/dev/null || die "Ollama no quedo en PATH."
    ollama --version
  fi
fi

info "Herramientas instaladas (consulta de version sin restaurar estado):"
git --version
podman --version
podman-compose --version
info "La validacion rootless funcional, los ajustes de red para Ollama,"
info "la configuracion visual XFCE y la restauracion de datos son pasos PENDING."
info "Continuar con Documentation/Recovery/Migration-Checklist.md."
