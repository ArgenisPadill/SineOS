#!/usr/bin/env bash
# SineOS
# Nombre: sineos-secrets-audit.sh
# Propósito: auditar secretos y permisos sin mostrar valores.
# Categoría: operativo recurrente / seguridad
# Estado: validado 23-09-2026
# Plataforma: Debian 13
# Reejecutable: sí
# Privilegios: usuario normal, sin sudo
# Documentación: Documentation/Security/Secrets-Management.md

set -u
set -o pipefail

NAME="sineos-secrets-audit"
VERSION="1.1.0"
TS="$(date '+%Y-%m-%d_%H-%M-%S')"
OK=0
WARN=0
ERR=0

ok(){ echo "[ OK ] $1"; ((OK+=1)); }
warn(){ echo "[WARN] $1"; ((WARN+=1)); }
err(){ echo "[ERROR] $1"; ((ERR+=1)); }
section(){ printf '\n============================================================\n %s\n============================================================\n' "$1"; }
has(){ command -v "$1" >/dev/null 2>&1; }

has git || { echo "ERROR: Git no disponible."; exit 2; }
has python3 || { echo "ERROR: Python 3 no disponible."; exit 2; }

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
[[ -n "$ROOT" ]] || { echo "ERROR: ejecuta dentro del repositorio SineOS."; exit 2; }

STATE="${HOME}/.local/state/sineos/security"
REPORT_DIR="$STATE/secrets-audit"
GITLEAKS_DIR="$STATE/gitleaks"
mkdir -p "$REPORT_DIR" "$GITLEAKS_DIR"
chmod 700 "$STATE" "$REPORT_DIR" "$GITLEAKS_DIR" 2>/dev/null || true
umask 077

REPORT="$REPORT_DIR/$NAME-$TS.txt"
WORK_JSON="$GITLEAKS_DIR/working-tree-$TS.json"
HISTORY_JSON="$GITLEAKS_DIR/git-history-$TS.json"
: > "$REPORT"
chmod 600 "$REPORT"
exec > >(tee -a "$REPORT") 2>&1

cd "$ROOT" || exit 2

section "SineOS — AUDITORÍA DE SECRETOS"
echo "Versión: $VERSION"
echo "Fecha: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "Repositorio: $ROOT"
echo "No se muestran valores de secretos."

section "1. HERRAMIENTAS"
if has gitleaks; then
  ok "Gitleaks disponible."
  gitleaks version 2>&1 | head -n 1
else
  err "Gitleaks no está instalado."
fi

section "2. ARCHIVOS .env"
FOUND=0
while IFS= read -r -d '' f; do
  FOUND=1
  mode="$(stat -c '%a' "$f" 2>/dev/null || echo '?')"
  owner="$(stat -c '%U:%G' "$f" 2>/dev/null || echo '?')"
  size="$(stat -c '%s' "$f" 2>/dev/null || echo '?')"
  rel="${f#"$ROOT"/}"
  echo "$rel | permiso=$mode | propietario=$owner | tamaño=${size}B"
  [[ "$mode" == 600 || "$mode" == 400 ]] && ok "$rel tiene permisos privados." || warn "$rel usa permiso $mode."
  git check-ignore -q "$f" 2>/dev/null && ok "$rel está ignorado por Git." || err "$rel NO está ignorado por Git."
done < <(find "$ROOT/Containers/stacks" -type f -name '.env' -print0 2>/dev/null)
[[ "$FOUND" -eq 1 ]] || warn "No se encontraron .env locales."

section "3. ~/.config/sineos"
CFG="${HOME}/.config/sineos"
if [[ -d "$CFG" ]]; then
  mode="$(stat -c '%a' "$CFG")"
  [[ "$mode" == 700 ]] && ok "~/.config/sineos está en 700." || warn "~/.config/sineos usa permiso $mode."
  while IFS= read -r -d '' f; do
    mode="$(stat -c '%a' "$f" 2>/dev/null || echo '?')"
    echo "$mode $f"
    [[ "$mode" == 600 || "$mode" == 400 ]] && ok "$(basename "$f") privado." || warn "$f usa permiso $mode."
  done < <(find "$CFG" -maxdepth 3 -type f -print0 2>/dev/null)
else
  warn "No existe ~/.config/sineos."
fi

section "4. NOMBRES SENSIBLES RASTREADOS"
TRACKED="$(git ls-files | grep -Ei '(^|/)(\.env$|[^/]+\.(key|pem|p12|pfx)$|id_rsa$|id_ed25519$|credentials\.json$)' || true)"
if [[ -z "$TRACKED" ]]; then
  ok "No hay nombres sensibles conocidos rastreados por Git."
else
  err "Hay nombres potencialmente sensibles rastreados:"
  echo "$TRACKED"
fi

count_json(){
  python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))))' "$1" 2>/dev/null || echo -1
}

section "5. GITLEAKS — SNAPSHOT VERSIONABLE"
if has gitleaks; then
  rm -f "$WORK_JSON"

  SNAPSHOT_DIR="$(mktemp -d)"
  chmod 700 "$SNAPSHOT_DIR"

  COPIED=0
  while IFS= read -r -d '' rel; do
    [[ -f "$ROOT/$rel" ]] || continue
    mkdir -p "$SNAPSHOT_DIR/$(dirname "$rel")"
    cp -- "$ROOT/$rel" "$SNAPSHOT_DIR/$rel"
    ((COPIED+=1))
  done < <(git ls-files -co --exclude-standard -z)

  echo "Archivos versionados/versionables analizados: $COPIED"
  echo "Los archivos ignorados por Git no se incluyen en este snapshot."

  gitleaks detect --source "$SNAPSHOT_DIR" --no-git --redact --report-format json --report-path "$WORK_JSON" --exit-code 0 >/dev/null 2>&1
  chmod 600 "$WORK_JSON" 2>/dev/null || true

  rm -rf "$SNAPSHOT_DIR"

  n="$(count_json "$WORK_JSON")"
  [[ "$n" == 0 ]] && ok "Snapshot versionable: 0 hallazgos." || err "Snapshot versionable: $n hallazgo(s). Revisa el JSON privado."
fi

section "6. GITLEAKS — HISTORIAL"
if has gitleaks; then
  rm -f "$HISTORY_JSON"
  gitleaks detect --source "$ROOT" --redact --report-format json --report-path "$HISTORY_JSON" --exit-code 0 >/dev/null 2>&1
  chmod 600 "$HISTORY_JSON" 2>/dev/null || true
  n="$(count_json "$HISTORY_JSON")"
  [[ "$n" == 0 ]] && ok "Historial Git: 0 hallazgos." || err "Historial Git: $n hallazgo(s). Revisa el JSON privado."
fi

section "7. GIT"
[[ -z "$(git status --porcelain)" ]] && ok "Working tree limpio." || { warn "Working tree con cambios locales."; git status --short; }

section "8. REPORTES"
stat -c '%a %U:%G %s bytes %n' "$REPORT" 2>/dev/null || true
[[ -f "$WORK_JSON" ]] && stat -c '%a %U:%G %s bytes %n' "$WORK_JSON" || true
[[ -f "$HISTORY_JSON" ]] && stat -c '%a %U:%G %s bytes %n' "$HISTORY_JSON" || true

section "9. RESUMEN"
echo "OK: $OK"
echo "Advertencias: $WARN"
echo "Errores: $ERR"
echo "Reporte: $REPORT"

if [[ "$ERR" -gt 0 ]]; then
  echo "RESULTADO: REVISAR"
  exit 1
fi

echo "RESULTADO: OK"
exit 0
