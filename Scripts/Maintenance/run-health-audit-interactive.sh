#!/usr/bin/env bash
# SineOS
# Nombre: run-health-audit-interactive.sh
# Propósito: ejecutar la auditoría trimestral desde la aplicación nativa.
# Categoría: operativo recurrente / mantenimiento
# Estado: pendiente de validación
# Plataforma: Debian 13 / XFCE
# Reejecutable: sí
# Privilegios: solicita sudo únicamente para habilitar lecturas administrativas.
# Documentación: Documentation/Operations/Maintenance.md

set -u
set -o pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
AUDITOR="$REPO_ROOT/Scripts/Audit/sineos-health-audit.sh"

cd "$REPO_ROOT" || exit 1

printf '%s\n' "SineOS — Auditoría trimestral"
printf '%s\n\n' "Se solicitará autenticación para las comprobaciones de solo lectura que la requieren."

if ! sudo -v; then
    echo "ERROR: no se obtuvo autorización administrativa."
    read -r -p "Presiona Enter para cerrar..." _
    exit 1
fi

bash "$AUDITOR"
rc=$?

echo
if [[ "$rc" -eq 0 ]]; then
    echo "Auditoría terminada. Regresa a SineOS · Mantenimiento y pulsa Actualizar."
else
    echo "La auditoría requiere atención. Revisa el resultado antes de validarla."
fi

echo
read -r -p "Presiona Enter para cerrar..." _
exit "$rc"
