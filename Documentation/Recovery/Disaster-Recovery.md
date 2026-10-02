# SineOS — Disaster Recovery

## Estado

```text
Estado: VALIDADO
Fecha de validación: 02-10-2026
Deuda cerrada: TD-016
Plataforma de prueba: Debian GNU/Linux 13.7 limpio
Entorno: QEMU/KVM
```

Este procedimiento fue validado mediante una reconstrucción real de SineOS en un sistema Debian limpio, asumiendo que el equipo principal no puede utilizarse, los snapshots locales no están disponibles y el almacenamiento original puede haberse perdido.

La recuperación combina Git para infraestructura y documentación, Restic para datos privados y estado persistente, credenciales independientes para secretos y Podman rootless para reconstruir los servicios.

No se almacenan contraseñas, tokens ni valores de secretos en este documento.

## Fuentes de recuperación

La recuperación validada utiliza:

- GitHub para infraestructura, configuración versionada y documentación.
- Restic para datos privados y estado persistente.
- Un gestor de credenciales independiente para secretos de recuperación.
- Podman rootless para reconstruir los servicios.

Snapshot utilizado durante TD-016:

```text
Tag: SineOsBackups-011026-0101
Snapshot Restic: 9ec723e9d67e188ae5d37af07993b14a6d43139e472bf8ce40e8afc20259d638
Repositorio Restic: a1f88f2abd60836da247816e8c2e6eff1139cad54663e02d836b163773d3b406
```

## Requisitos del sistema limpio

La prueba certificada utilizó:

```text
Debian: 13.7
Restic: 0.18.0
Podman: 5.4.2
podman-compose: 1.3.0
Git: 2.47.3
```

También deben estar disponibles uidmap, pasta, slirp4netns, fuse-overlayfs, netavark y aardvark-dns.

## Orden de recuperación

```text
Debian limpio
→ Git
→ credencial Restic
→ repositorio Restic
→ restore completo
→ secretos y estado privado
→ redes Podman
→ PostgreSQL
→ Uptime Kuma
→ Stirling PDF
→ Open WebUI
→ XFCE + LightDM
→ primer login y configuración visual
→ validación integrada
```

## Git

Clonar el repositorio en `${SINEOS_REPO}` y comprobar:

```bash
git status -sb
git rev-parse HEAD
git rev-parse origin/main
```

Durante TD-016 se validó:

```text
HEAD local:  ba166be940f1c1c9f2073b14212fb4569b77f08e
origin/main: ba166be940f1c1c9f2073b14212fb4569b77f08e
Estado Git: limpio
```

## Restic

La credencial de Restic debe recuperarse desde almacenamiento independiente y nunca desde Git.

Antes del restore deben comprobarse los snapshots y la integridad del repositorio:

```bash
restic snapshots
restic check
```

En TD-016 se validaron el repositorio, el snapshot requerido y un restore completo sin errores.

## Estado privado restaurado

El restore utilizado incluyó:

- Knowledge Vault.
- configuración privada de SineOS.
- estados de health, security y maintenance.
- datos persistentes de Open WebUI.
- datos persistentes de Uptime Kuma.
- datos persistentes de Stirling PDF.
- staging lógico de PostgreSQL.

Los secretos restaurados deben conservar permisos restrictivos y no deben imprimirse durante la recuperación.

## Podman rootless

La recuperación certificada utiliza Podman rootless.

Antes de iniciar los servicios que dependen de ella debe existir la red compartida:

```bash
podman network create sineos-monitoring
```

Si la red ya existe, no debe recrearse innecesariamente.

## PostgreSQL

PostgreSQL se recupera desde el backup lógico certificado. El volumen vivo de PostgreSQL está excluido del backup Restic y no debe utilizarse como mecanismo de recuperación.

En un host rootless limpio, el directorio persistente debe prepararse para el UID/GID utilizado por la imagen PostgreSQL:

```bash
podman unshare chown 999:999 "${SINEOS_REPO}/Containers/volumes/postgres/data"
chmod 700 "${SINEOS_REPO}/Containers/volumes/postgres/data"
```

Sin este ajuste, el bootstrap realizado durante TD-016 falló por falta de permisos sobre `/var/lib/postgresql`.

La recuperación lógica utiliza los archivos certificados del staging PostgreSQL: `globals.sql`, `database.dump` y sus hashes SHA-256.

Durante TD-016 se validó:

```text
PostgreSQL: 18.6
pg_isready: OK
Base recuperada: sineos
Usuario recuperado: sineos
Restore de roles: OK
Restore de base: OK
Contraseña incorrecta: rechazada
Contraseña recuperada: aceptada
```

La autenticación final debe comprobarse desde fuera del contenedor a través del puerto publicado. Una conexión interna por loopback puede coincidir con reglas `trust` y no demuestra por sí sola que la contraseña haya sido validada.

## Uptime Kuma

Uptime Kuma recupera su estado persistente junto con Embedded MariaDB.

En un host Debian limpio, los archivos restaurados conservaron ownership incompatible con el usuario utilizado por MariaDB dentro del contenedor.

Fue necesario normalizar el volumen restaurado:

```bash
podman unshare chown -R 1000:1000 "${SINEOS_REPO}/Containers/volumes/uptime-kuma/data"
```

Antes de este ajuste, MariaDB no pudo escribir archivos como `aria_log_control` e `ibdata1`.

Después de corregir ownership se validó:

```text
Embedded MariaDB: OK
HTTP: 302
Estabilidad: OK
Monitor Stirling PDF: recuperado
```

Este hallazgo debe incorporarse al flujo automatizado de recuperación para que un restore sobre host limpio no dependa de una corrección manual.

## Stirling PDF

Stirling PDF no requirió una corrección manual de ownership durante TD-016.

La imagen ejecutó su propia fase de ajuste de permisos durante el arranque y pudo utilizar directamente los datos restaurados.

Se validó:

```text
Imagen: docker.stirlingpdf.com/stirlingtools/stirling-pdf:2.14.3-fat
HTTP: 200
Base H2: presente
JWT existente: recuperado
Red sineos-monitoring: OK
```

TD-019 permanece abierto porque la versión actual modifica permisos dentro de `/configs` durante el arranque y ese comportamiento debe revisarse al actualizar.

## Open WebUI

Open WebUI recupera su estado desde el volumen persistente y su `.env` privado.

Durante TD-016 se validó:

```text
HTTP: 200
RestartCount: 0
SQLite integrity_check: ok
Tablas: 43
Revisión Alembic: d4c1a8e37b62
WEBUI_SECRET_KEY: recuperado y cargado
```

El directorio `cache/` está excluido del backup.

En el host limpio Open WebUI reconstruyó aproximadamente 889 MiB de caché descargando el modelo de embeddings desde Internet.

Por ello, el estado persistente se recupera sin depender del caché, pero algunas funciones RAG pueden tardar en quedar disponibles después de un Disaster Recovery.

## Entorno gráfico XFCE

La recuperación completa de SineOS también incluye la reconstrucción del entorno gráfico definido por el proyecto.

La validación complementaria de TD-016 se realizó sobre la misma máquina Debian 13 limpia utilizando el script versionado:

```text
Scripts/Desktop/sineos-xfce-macos.sh
Versión validada: 4.0.0
```

Desde una instalación sin XFCE, el script instaló y configuró correctamente:

- XFCE.
- LightDM.
- arranque mediante `graphical.target`.
- Arc-Dark para GTK y XFWM.
- Papirus-Dark.
- fuentes Noto Sans y JetBrains Mono.
- Docklike.
- barra superior y Dock inferior.
- wallpaper generado por SineOS.
- aplicación automática del layout durante el primer inicio de sesión.

Después del reinicio y primer login se validó:

```text
XFCE instalado: sí
LightDM: active / enabled
Sesión: X11 / XFCE
Layout SineOS: aplicado
xfce4-panel: activo
xfdesktop: activo
Tema GTK: Arc-Dark
Iconos: Papirus-Dark
Tema XFWM: Arc-Dark
Panel superior: p=6;x=0;y=0
Panel inferior: p=10;x=0;y=0
Auto-ocultación Dock: 2
Autostart de primer login: consumido correctamente
```

El wallpaper utilizado es generado localmente por el instalador y tiene una apariencia deliberadamente genérica. SineOS no define actualmente un tema gráfico propio; reproduce una configuración visual basada en componentes estándar de XFCE.

La validación demuestra que una instalación Debian limpia puede reconstruir automáticamente la experiencia de escritorio definida por SineOS a partir del repositorio Git.

## Validación integrada

Al finalizar la recuperación deben comprobarse como mínimo:

```text
PostgreSQL: accepting connections
Open WebUI: HTTP 200
Uptime Kuma: HTTP 2xx/3xx
Stirling PDF: HTTP 200
Uptime → Stirling: HTTP 200
XFCE: sesión X11 activa
LightDM: active / enabled
Layout SineOS: aplicado
Tema GTK/XFWM: Arc-Dark
Iconos: Papirus-Dark
Wallpaper SineOS: configurado
Git working tree: limpio
HEAD local = origin/main
```

La prueba TD-016 cumplió todos estos controles.

## Imágenes utilizadas durante TD-016

```text
PostgreSQL
docker.io/library/postgres:18
662db3da228c2ea2649b3ae04db4b4479e85fea5979f6a917a7f6d5cb1e7ec39

Uptime Kuma
docker.io/louislam/uptime-kuma:2
836213aba0d589c3a4977c218a25b27ef3f5a6f7c2cac6883636afca1afcda46

Stirling PDF
docker.stirlingpdf.com/stirlingtools/stirling-pdf:2.14.3-fat
4e38392ba07e6c2704f2f756589ef37f91e84eb7388687536f1e71b7a9015d02

Open WebUI
ghcr.io/open-webui/open-webui:main
2c9064266cedccc600a6c6f85a3d19b5869407588dae2ef08ecde8a93842a2ea
```

Las etiquetas móviles no garantizan reproducibilidad futura. Los IDs anteriores registran exactamente las imágenes utilizadas durante esta certificación.

## Límites de la prueba

TD-016 valida recuperación de infraestructura, datos persistentes, secretos necesarios, servicios principales y entorno gráfico reproducible de SineOS.

No cierra automáticamente las deudas de hardening, red, Ollama, AppArmor, permisos de Stirling PDF ni reproducibilidad de imágenes.

El hallazgo de ownership de Uptime Kuma debe mantenerse como deuda separada hasta que el flujo automatizado lo resuelva.

## Resultado

La reconstrucción completa desde Debian 13 limpio fue satisfactoria.

SineOS puede recuperarse desde Git, Restic y credenciales independientes sin depender del SSD original ni de snapshots Btrfs locales. La reconstrucción validada incluye también XFCE, LightDM y la configuración visual reproducible definida por el proyecto.
