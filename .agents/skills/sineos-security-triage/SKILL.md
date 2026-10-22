---
name: sineos-security-triage
description: Auditar en solo lectura el estado de seguridad de SineOS Debian 13, AppArmor, nftables, Podman, SSH, servicios y recuperación; usar para inventarios o preparación del gate de Seguridad, nunca para aplicar hardening sin autorización.
---

# SineOS — Triage defensivo de Seguridad

**Disparador:** usuario solicita auditar, inventariar, diagnosticar, priorizar o revisar el estado de seguridad de SineOS.

**No activar:** cambios directos de firewall, eliminación de paquetes, reconfiguración de servicios, pruebas intrusivas o instalación; requieren tarea separada y autorización explícita.

Lee primero `AGENTS.md`, `Documentation/Architecture/Engineering-Delivery-Standard.md`, `Documentation/Security/Security-Baseline.md`, `Documentation/Operations/Technical-Debt.md` y el [issue #2](https://github.com/ArgenisPadill/SineOS/issues/2).

## Método

1. Identifica qué evidencia está en archivos y qué datos del host faltan. **Nunca confundas documentación histórica con estado actual observado.**
2. Planea solo consultas no modificadoras apropiadas para Debian 13: versión, `systemctl status`/`is-enabled`, `ss -tulpn`, estado de perfiles AppArmor, `nft list ruleset`, inventarios Podman, estado de Btrfs/Restic/rollback, registros saneados. Evita mostrar contraseñas, tokens, rutas sensibles o secretos en el informe.
3. Ejecuta consultas locales **solo** si el usuario autorizó esta inspección y existe acceso apropiado. La lectura de configuraciones privadas requiere permiso específico; no presupongas `sudo`.
4. Separa **OBSERVADO / DOCUMENTADO / NO VERIFICADO / RIESGO / BLOQUEADO**. No recomiendes desactivar defensas, alterar producción o reiniciar servicios como 'primera solución'.
5. Clasifica hallazgos por exposición, impacto, urgencia, dependencia y mitigación; relaciona los TD/issue existentes. Describe una verificación y un rollback futuro para cada intervención propuesta, sin aplicarla.
6. Informa en español, con evidencia, límites y propuesta de próximos pasos. No cierres un gate ni marques PASS por revisar Markdown.

**Salida requerida:** estado, evidencia (archivo/comando sin secretos), riesgo, propuesta no ejecutada, autorización necesaria y relación con #2. La prioridad absoluta sigue siendo Seguridad; SineOS Office permanece congelado.

**Fuentes de inspiración:** [GitHub Debian Linux Triage](https://github.com/github/awesome-copilot/blob/main/skills/debian-linux-triage/SKILL.md), [Trail of Bits Differential Review](https://github.com/trailofbits/skills/blob/main/plugins/differential-review/skills/differential-review/SKILL.md). Implementación original, sin scripts importados.
