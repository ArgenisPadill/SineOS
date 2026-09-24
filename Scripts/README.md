# Scripts de SineOS

Este directorio contiene automatizaciones versionadas que forman parte de la operación, diagnóstico, instalación o reproducibilidad de SineOS.

La política completa se encuentra en `Documentation/Architecture/Script-Standard.md`.

## Catálogo actual

| Componente | Archivo | Clasificación | Estado | Uso |
|---|---|---|---|---|
| Auditoría | `Audit/sineos-audit.sh` | Operativo recurrente | Activo | Diagnóstico de solo lectura de la plataforma SineOS |\n| Salud trimestral | `Audit/sineos-health-audit.sh` | Operativo recurrente | Pendiente de validar | Auditoría profunda de sistema, seguridad, actualizaciones, Git y contenedores |
| Escritorio XFCE | `Desktop/sineos-xfce-macos.sh` | Pilar / instalación | Activo | Instala, aplica, valida y restaura la configuración visual reproducible de XFCE |
| Open WebUI | `Monitoring/check-open-webui.sh` | Operativo recurrente | Activo | Comprueba el endpoint local y envía heartbeat Push a Uptime Kuma |
| PostgreSQL | `Monitoring/check-postgresql.sh` | Operativo recurrente | Activo | Comprueba PostgreSQL mediante `pg_isready` y envía heartbeat Push |
| NetworkPrivacy | `NetworkPrivacy/install-network-privacy.sh` | Pilar / instalación | Activo | Valida dependencias e integra SineOS Privacidad de red con XFCE |
| Seguridad | `Security/sineos-secrets-audit.sh` | Operativo recurrente | Validado | Audita permisos, Git y Gitleaks sin mostrar secretos |

## Audit — sineos-audit.sh

### Propósito

Crear una fotografía diagnóstica del estado de SineOS sin modificar deliberadamente su configuración.

### Características

- solo lectura por diseño;
- revisa sistema operativo, hardware, Btrfs, APT, systemd, journal, red y seguridad;
- inspecciona Git, SSH y GitHub;
- inspecciona Podman y los contenedores SineOS;
- revisa PostgreSQL;
- revisa XFCE, audio, entrada, SMART y recursos;
- genera un reporte local.

### Observación actual

El script contiene rutas históricas basadas en `$HOME/Workspace/SineOS`. Antes de considerarlo totalmente portable debe migrarse a detección dinámica de la raíz del repositorio o a una variable configurada.

Los reportes están excluidos de Git.

### Frecuencia

Bajo demanda, antes y después de cambios importantes o durante diagnóstico.

## Desktop — sineos-xfce-macos.sh

### Propósito

Reproducir la configuración visual y funcional definida para XFCE en SineOS.

### Clasificación

Script pilar.

### Operaciones conocidas

```text
install
packages
apply
status
restore
help
```

### Características importantes

- instala dependencias soportadas;
- crea respaldo antes de modificar configuración;
- evita reconstruir innecesariamente el layout;
- puede restaurar el último respaldo;
- no modifica red, audio, Bluetooth, energía, kernel ni firmware;
- no utiliza `xfce4-panel --restart` por una incompatibilidad observada y documentada.

### Documentación

`Documentation/Operations/XFCE-Visual-Configuration.md`

## Monitoring — check-open-webui.sh

### Propósito

Validar localmente Open WebUI y notificar a un monitor Push de Uptime Kuma solamente cuando el servicio responde.

### Dependencias

- `curl`;
- archivo local `~/.config/sineos/monitoring/open-webui.env`.

### Secretos

La URL Push permanece fuera de Git.

### Frecuencia

Recurrente mediante el mecanismo local de ejecución que se defina y documente.

### Deuda documental

Debe formalizarse el mecanismo exacto que programa su ejecución y el procedimiento para crear el monitor Push.

## Monitoring — check-postgresql.sh

### Propósito

Comprobar la disponibilidad real de PostgreSQL mediante `podman exec sineos-postgres pg_isready` y enviar heartbeat a Uptime Kuma si la comprobación es satisfactoria.

### Dependencias

- Podman rootless;
- contenedor `sineos-postgres`;
- `pg_isready` dentro del contenedor;
- archivo local `~/.config/sineos/monitoring/postgresql.env`.

### Secretos

La URL Push permanece fuera de Git.

### Deuda documental

Debe formalizarse el mecanismo de ejecución recurrente y la creación/configuración del monitor correspondiente.

## NetworkPrivacy — install-network-privacy.sh

### Propósito

Integrar la aplicación SineOS Privacidad de red en el escritorio.

### Operaciones

```text
install
status
uninstall
```

### Qué realiza

- comprueba los archivos de la aplicación;
- valida Python 3;
- valida NetworkManager/`nmcli`;
- valida `dig` y `getent`;
- valida GTK3/PyGObject;
- prepara el directorio de estado;
- establece permisos;
- crea el archivo `.desktop`;
- actualiza la base de datos local de aplicaciones cuando está disponible.

### Limitación actual

Comprueba dependencias pero no instala automáticamente las que faltan.

### Documentación

- `Documentation/Operations/NetworkPrivacy.md`
- `Documentation/Architecture/Native-Applications.md`

## Security — sineos-secrets-audit.sh

### Propósito

Comprobar de forma recurrente la higiene de secretos de SineOS sin mostrar valores ni modificar configuración.

### Controles

- permisos de archivos `.env`;
- `.env` ignorados por Git;
- permisos de `~/.config/sineos`;
- nombres sensibles rastreados por Git;
- Gitleaks sobre snapshot versionado/versionable excluyendo archivos ignorados;
- Gitleaks sobre historial Git;
- estado del working tree.

### Reportes

Se guardan fuera del repositorio bajo `~/.local/state/sineos/security/` con permisos privados.

### Estado

Validado el 23-09-2026: 12 controles OK, 0 advertencias, 0 errores; snapshot versionable e historial Git sin hallazgos.

## Automatización fuera de Scripts/

No toda automatización debe vivir literalmente bajo `Scripts/`.

Por ejemplo, `Containers/stacks/postgres/Makefile` es una interfaz operativa del stack PostgreSQL y ofrece comandos para validar configuración, descargar imagen, iniciar, detener, reiniciar, consultar estado, logs y health.

Se conserva junto al stack porque su contexto natural es PostgreSQL.

## Scripts de una sola vez

Los scripts usados durante construcción, reparación o migraciones anteriores no deben copiarse al repositorio sin revisión.

Si se recuperan desde el equipo local, historial de shell, backups u otras fuentes, cada uno debe clasificarse.

Resultado posible:

```text
seguir usando        -> Scripts/<función>/
migración relevante  -> Scripts/Migrations/
reemplazado          -> no reincorporar
diagnóstico útil     -> integrar y documentar
experimental         -> no presentar como estable
contiene secretos    -> sanear antes de considerar publicación
```

Los directorios nuevos solo se crean cuando exista un archivo real que los justifique.

## Próximas acciones

- crear documentación específica del auditor;
- crear documentación específica del sistema de monitoreo;
- eliminar rutas locales rígidas del auditor;
- formalizar cómo se programan los checks de monitoreo;
- inventariar scripts históricos existentes en el equipo y decidir cuáles merecen incorporarse;
- incorporar futuros scripts de backup y recovery cuando sean implementados y validados.