# SineOS — Guía de construcción y ciclo de vida

Esta carpeta reconstruye, en orden, el camino seguido para construir SineOS desde Debian hasta el estado operativo actual.

Está pensada como un **runbook vivo**: los bloques de terminal pueden copiarse y pegarse, y esta guía debe actualizarse conforme SineOS avance.

## Estados

- **VALIDADO:** el estado o procedimiento fue comprobado en SineOS.
- **VALIDADO HISTÓRICAMENTE:** funcionó durante la construcción, aunque puede requerir una nueva prueba en una instalación limpia.
- **PENDIENTE DE REVALIDAR:** conocemos el estado final, pero no existe evidencia suficiente para afirmar que el procedimiento completo fue reproducido desde cero.
- **PENDIENTE:** todavía no está implementado.

## Regla principal

> Esta guía no inventa pasos para rellenar huecos. Si un procedimiento no fue validado, se marca como pendiente y se completa cuando se pruebe.

## Orden de construcción

```text
00 Preparación de imagen
01 Instalación de Debian
02 Configuración base de Debian
03 XFCE y escritorio reproducible
04 Git, GitHub y SSH
05 Podman rootless
06 PostgreSQL
07 Ollama e IA local
08 Open WebUI
09 Knowledge Vault y Miyo
10 Servicios locales y monitoreo
11 Seguridad, red y privacidad
12 NetworkPrivacy
13 Programas, scripts y automatización
14 Auditoría y mantenimiento
15 Estado actual y siguientes pasos
16 Validación final de seguridad asistida por agente
```

## Alcance

Esta guía describe el sistema construido y validado en Debian 13 Trixie sobre la plataforma SineOS.

Para detalles profundos de cada componente se enlazan los documentos de `Documentation/Architecture/`, `Documentation/Operations/` y `Documentation/Security/`.

## Convención de rutas

En ejemplos se usa:

```bash
export SINEOS_REPO="$HOME/Workspace/SineOS"
```

Las rutas personales reales no deben publicarse en Git.

## Actualización

Cada vez que se incorpore o cambie un componente estable debe revisarse:

1. el archivo correspondiente de esta guía;
2. la documentación operativa del componente;
3. `Scripts/README.md` si hay automatización;
4. `Apps/README.md` si hay un programa propio;
5. `CHANGELOG.md`;
6. deuda técnica si queda algo pendiente.