#!/usr/bin/env bash
# SineOS
# Nombre: sineos-health-audit.sh
# Propósito: auditoría profunda trimestral de salud de SineOS.
# Categoría: operativo recurrente / auditoría
# Estado: pendiente de revalidación final v1.2.2
# Plataforma: Debian 13 Trixie
# Reejecutable: sí
# Privilegios: usuario normal; sudo -n solo para lecturas cuando esté disponible.
# Documentación: Documentation/Operations/Quarterly-Health.md

set -u
set -o pipefail

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH"

NAME="sineos-health-audit"
VERSION="1.2.2"
TS="$(date '+%Y-%m-%d_%H-%M-%S')"
OK=0
WARN=0
ERR=0
INFO=0

ok(){ echo "[ OK ] $1"; ((OK+=1)); }
warn(){ echo "[WARN] $1"; ((WARN+=1)); }
err(){ echo "[ERROR] $1"; ((ERR+=1)); }
info(){ echo "[INFO] $1"; ((INFO+=1)); }
section(){ printf '\n============================================================\n %s\n============================================================\n' "$1"; }
has(){ command -v "$1" >/dev/null 2>&1; }

has git || { echo "ERROR: Git no disponible."; exit 2; }
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
[[ -n "$ROOT" ]] || { echo "ERROR: ejecuta dentro del repositorio SineOS."; exit 2; }
cd "$ROOT" || exit 2

STATE="${HOME}/.local/state/sineos/health"
mkdir -p "$STATE"
chmod 700 "$STATE" 2>/dev/null || true
umask 077
REPORT="$STATE/$NAME-$TS.txt"
: > "$REPORT"
chmod 600 "$REPORT"
exec > >(tee -a "$REPORT") 2>&1

section "SineOS — AUDITORÍA PROFUNDA DE SALUD"
echo "Versión: $VERSION"
echo "Fecha: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "Repositorio: $ROOT"
echo "Reporte: $REPORT"

section "1. SISTEMA"
grep -q '^VERSION_ID="13"' /etc/os-release 2>/dev/null && ok "Debian 13 detectado." || warn "Sistema distinto de Debian 13."
echo "Kernel: $(uname -r)"
echo "Uptime: $(uptime -p 2>/dev/null || true)"
if has timedatectl; then
  synced="$(timedatectl show -p NTPSynchronized --value 2>/dev/null || true)"
  [[ "$synced" == yes ]] && ok "Reloj sincronizado." || warn "NTP no aparece sincronizado."
fi

section "2. GIT Y GITHUB"
branch="$(git branch --show-current 2>/dev/null || true)"
[[ "$branch" == main ]] && ok "Rama main activa." || warn "Rama activa: ${branch:-desconocida}."
[[ -z "$(git status --porcelain)" ]] && ok "Working tree limpio." || { warn "Working tree con cambios."; git status --short; }

local_head="$(git rev-parse HEAD 2>/dev/null || true)"
remote_head="$(timeout 20 git ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}' || true)"
if [[ -n "$remote_head" && "$local_head" == "$remote_head" ]]; then
  ok "HEAD local coincide con main remoto."
elif [[ -z "$remote_head" ]]; then
  warn "No se pudo comprobar main remoto."
else
  err "HEAD local y main remoto no coinciden."
fi

section "3. SYSTEMD Y JOURNAL"
failed="$(systemctl --failed --no-legend 2>/dev/null || true)"
[[ -z "$failed" ]] && ok "Sin unidades systemd fallidas." || { err "Hay unidades systemd fallidas:"; echo "$failed"; }

journal_all="$(journalctl -p err..alert -b --no-pager 2>/dev/null | grep -v '^-- No entries --$' || true)"
host_errors="$(
  printf '%s\n' "$journal_all" |
  grep -Ev 'sineos-(open-webui|stirling-pdf|uptime-kuma|postgres)\[' |
  grep -Ev 'sudo\[[0-9]+\].*password is required' ||
  true
)"

resolved_monitor=0
monitor_result="$(systemctl --user show sineos-monitor-open-webui.service -p Result --value 2>/dev/null || true)"
monitor_status="$(systemctl --user show sineos-monitor-open-webui.service -p ExecMainStatus --value 2>/dev/null || true)"
if [[ "$monitor_result" == "success" && "$monitor_status" == "0" ]]; then
  before="$(printf '%s\n' "$host_errors" | sed '/^$/d' | wc -l)"
  host_errors="$(printf '%s\n' "$host_errors" | grep -v 'Failed to start sineos-monitor-open-webui.service' || true)"
  after="$(printf '%s\n' "$host_errors" | sed '/^$/d' | wc -l)"
  resolved_monitor="$(( before - after ))"
fi

resolved_obex=0
obex_active="$(systemctl --user is-active obex.service 2>/dev/null || true)"
obex_result="$(systemctl --user show obex.service -p Result --value 2>/dev/null || true)"
if [[ "$obex_active" == "active" && "$obex_result" == "success" ]]; then
  before="$(printf '%s\n' "$host_errors" | sed '/^$/d' | wc -l)"
  host_errors="$(printf '%s\n' "$host_errors" | grep -v 'Unable to acquire registry: Error calling StartServiceByName for org.gnome.evolution.dataserver.Sources5: Unit evolution-source-registry.service not found' || true)"
  after="$(printf '%s\n' "$host_errors" | sed '/^$/d' | wc -l)"
  resolved_obex="$(( before - after ))"
fi

if [[ "$resolved_monitor" -gt 0 ]]; then
  info "$resolved_monitor fallo(s) histórico(s) del monitor Open WebUI quedaron recuperados; el servicio actual termina con Result=success y ExecMainStatus=0."
fi

if [[ "$resolved_obex" -gt 0 ]]; then
  info "$resolved_obex evento(s) histórico(s) de obexd/Evolution fueron clasificados como no activos; obex.service está active con Result=success."
fi

if [[ -z "$(printf '%s' "$host_errors" | tr -d '[:space:]')" ]]; then
  ok "Sin errores actuales de prioridad alta del host."
else
  warn "El journal del host contiene eventos err..alert que siguen requiriendo revisión."
  printf '%s\n' "$host_errors" | tail -n 40
fi

container_err_n="$(
  printf '%s\n' "$journal_all" |
  grep -Ec 'sineos-(open-webui|stirling-pdf|uptime-kuma|postgres)\[' ||
  true
)"
if [[ "$container_err_n" -gt 0 ]]; then
  info "$container_err_n entrada(s) de contenedores aparecen con prioridad err; son contexto, no fallo automático del host."
fi

section "4. APT Y PAQUETES"
latest="$(find /var/lib/apt/lists -maxdepth 1 -type f -name '*InRelease' -printf '%T@\n' 2>/dev/null | sort -nr | head -n1 | cut -d. -f1)"
if [[ -n "$latest" ]]; then
  age="$(( ($(date +%s) - latest) / 86400 ))"
  echo "Edad metadatos APT: $age día(s)"
  (( age <= 7 )) && ok "Metadatos APT recientes." || warn "Metadatos APT > 7 días."
else
  warn "No se pudo medir antigüedad de APT."
fi

up="$(apt list --upgradable 2>/dev/null | sed '1d' || true)"
up_n="$(printf '%s\n' "$up" | sed '/^$/d' | wc -l)"
[[ "$up_n" -eq 0 ]] && ok "Sin paquetes actualizables según cache." || { warn "$up_n paquete(s) actualizable(s)."; printf '%s\n' "$up" | head -n 60; }

audit="$(dpkg --audit 2>/dev/null || true)"
[[ -z "$audit" ]] && ok "dpkg consistente." || { err "dpkg reporta problemas:"; echo "$audit"; }

local_pkgs="$(apt list '~o' 2>/dev/null | sed '1d' || true)"
local_n="$(printf '%s\n' "$local_pkgs" | sed '/^$/d' | wc -l)"
if [[ "$local_n" -eq 0 ]]; then
  ok "No hay paquetes instalados fuera de las fuentes APT actuales."
else
  info "$local_n paquete(s) aparecen instalados localmente o sin versión disponible en las fuentes actuales; se inventarían, no se eliminan automáticamente."
  printf '%s\n' "$local_pkgs" | head -n 60
fi

echo
echo "Fuentes APT:"
grep -RhsE '^[[:space:]]*(deb |Types:|URIs:|Suites:)' /etc/apt/sources.list /etc/apt/sources.list.d 2>/dev/null || true

section "5. KERNEL"
running="$(uname -r)"
if dpkg-query -W "linux-image-$running" >/dev/null 2>&1; then
  ok "Kernel en ejecución gestionado por dpkg."
else
  warn "No se relacionó el kernel actual con linux-image-$running."
fi
[[ -e /run/reboot-required || -e /var/run/reboot-required ]] && warn "Reinicio pendiente." || ok "Sin marcador de reinicio pendiente."

section "6. VULNERABILIDADES"
if has debsecan; then
  fixed="$(debsecan --suite trixie --format packages --only-fixed 2>/dev/null | sort -u || true)"
  fixed_n="$(printf '%s\n' "$fixed" | sed '/^$/d' | wc -l)"
  [[ "$fixed_n" -eq 0 ]] && ok "Sin correcciones de seguridad pendientes según debsecan." || { err "$fixed_n paquete(s) con corrección de seguridad disponible."; printf '%s\n' "$fixed" | head -n 80; }

  vuln="$(debsecan --suite trixie --format simple 2>/dev/null || true)"
  vuln_n="$(printf '%s\n' "$vuln" | sed '/^$/d' | wc -l)"
  info "Inventario general debsecan: $vuln_n entrada(s). El control accionable es --only-fixed."
else
  err "debsecan no instalado: revisión de vulnerabilidades no certificable."
fi

section "7. ALMACENAMIENTO Y BTRFS"
df -hT -x tmpfs -x devtmpfs
root_use="$(df -P / | awk 'NR==2 {gsub("%","",$5); print $5}')"
[[ -n "$root_use" && "$root_use" -lt 85 ]] && ok "Uso de / < 85%." || warn "Uso de / >= 85%."

if has btrfs && findmnt -n -o FSTYPE / | grep -qx btrfs; then
  btrfs filesystem usage / 2>&1 || true
  if sudo -n true >/dev/null 2>&1; then
    stats="$(sudo -n btrfs device stats / 2>/dev/null || true)"
    echo "$stats"
    if echo "$stats" | awk '{if ($2+0 > 0) bad=1} END {exit bad?0:1}'; then
      err "Btrfs reporta contadores de error."
    else
      ok "Btrfs sin contadores de error."
    fi
  else
    warn "Sin sudo no interactivo: btrfs device stats no certificado."
  fi
fi

section "8. SMART"
lsblk -d -o NAME,TYPE,SIZE,TRAN,MODEL 2>/dev/null || true
if has smartctl; then
  if sudo -n true >/dev/null 2>&1; then
    while read -r dev rest; do
      [[ -n "$dev" ]] || continue
      health="$(sudo -n smartctl -H "$dev" 2>&1 || true)"
      echo "$health"
      if echo "$health" | grep -Eqi 'PASSED|OK'; then
        ok "SMART saludable: $dev"
      elif echo "$health" | grep -qi 'SMART support is: Unavailable'; then
        info "$dev no expone capacidad SMART; no se interpreta como fallo del dispositivo."
      else
        warn "SMART no concluyente: $dev"
      fi
    done < <(sudo -n smartctl --scan-open 2>/dev/null || true)
  else
    warn "smartctl disponible pero sin sudo no interactivo."
  fi
else
  warn "smartmontools no instalado."
fi

section "9. SEGURIDAD DEL HOST"
has aa-status && { aa-status 2>/dev/null | head -n 30 || true; ok "AppArmor disponible."; } || warn "aa-status no disponible."

if has nft; then
  if sudo -n true >/dev/null 2>&1; then
    sudo -n nft list ruleset 2>/dev/null | grep -q 'policy drop' && ok "nftables contiene policy drop." || warn "No se confirmó policy drop."
  else
    warn "nftables no legible sin sudo no interactivo."
  fi
else
  err "nft no disponible."
fi

section "10. PODMAN"
if has podman; then
  podman ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Image}}'
  bad="$(podman ps -a --format '{{.Names}}|{{.Status}}' | grep -Ei 'unhealthy|dead|created' || true)"
  [[ -z "$bad" ]] && ok "Sin contenedores unhealthy/dead/created." || { warn "Contenedores a revisar:"; echo "$bad"; }

  moving="$(podman ps -a --format '{{.Names}}|{{.Image}}' | grep -E ':(main|latest)$' || true)"
  known_moving="$(printf '%s\n' "$moving" | grep -F 'sineos-open-webui|ghcr.io/open-webui/open-webui:main' || true)"
  other_moving="$(printf '%s\n' "$moving" | grep -v -F 'sineos-open-webui|ghcr.io/open-webui/open-webui:main' | sed '/^$/d' || true)"

  [[ -n "$known_moving" ]] && info "Open WebUI usa :main; riesgo conocido y registrado como TD-006."
  if [[ -n "$other_moving" ]]; then
    warn "Se detectaron otros tags móviles no clasificados:"
    printf '%s\n' "$other_moving"
  elif [[ -z "$moving" ]]; then
    ok "Sin tags móviles main/latest."
  fi
else
  err "Podman no disponible."
fi

section "11. SECRETOS"
if [[ -f "$ROOT/Scripts/Security/sineos-secrets-audit.sh" ]] && bash "$ROOT/Scripts/Security/sineos-secrets-audit.sh" >/dev/null 2>&1; then
  ok "Auditor de secretos: OK."
else
  err "Auditor de secretos requiere revisión."
fi

section "12. RESPALDO"
if [[ -f "$ROOT/Documentation/Recovery/Backup-Status.md" ]]; then
  grep -A6 'Último respaldo validado' "$ROOT/Documentation/Recovery/Backup-Status.md" || true
  ok "Estado de respaldo versionado disponible."
else
  warn "Backup-Status.md no existe."
fi

section "13. RESUMEN"
echo "OK: $OK"
echo "Advertencias: $WARN"
echo "Errores: $ERR"
echo "Información: $INFO"
echo "Reporte: $REPORT"

if [[ "$ERR" -gt 0 ]]; then
  echo "RESULTADO: REQUIERE_ATENCION"
  exit 1
elif [[ "$WARN" -gt 0 ]]; then
  echo "RESULTADO: CON_ADVERTENCIAS"
  exit 0
else
  echo "RESULTADO: OK"
  exit 0
fi
