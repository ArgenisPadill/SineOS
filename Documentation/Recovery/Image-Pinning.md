# SineOS — Fijación de imágenes de contenedores

**Estado:** preparación documental; cambio efectivo a digests **PENDING** (requiere consultar y probar imágenes del host). Fecha: 02-11-2026.

## Hallazgo en main

| Stack | Imagen en Compose / ejemplo actual | Situación |
| --- | --- | --- |
| postgres | `docker.io/library/postgres:18` vía `POSTGRES_IMAGE` | **Móvil**: cambia dentro de la rama mayor. |
| open-webui | `ghcr.io/open-webui/open-webui:main` | **Móvil**, advertido en README. |
| uptime-kuma | `docker.io/louislam/uptime-kuma:2` | **Móvil**, cambia dentro de v2. |
| stirling-pdf | `docker.stirlingpdf.com/stirlingtools/stirling-pdf:2.14.3-fat` | Etiqueta de versión concreta; aún puede ser retagueada. No es pin por digest. |

**Importante:** los identificadores SHA256 de imágenes documentados en el DR TD-016 son IDs locales de imagen; **no** se pueden suponer equivalentes a digests de manifest remoto para sintaxis `image@sha256:...`.

## Captura de referencias en la máquina origen (solo lectura)

```bash
podman images --digests
podman image inspect docker.io/library/postgres:18 --format '{{json .RepoDigests}}'
podman image inspect ghcr.io/open-webui/open-webui:main --format '{{json .RepoDigests}}'
podman image inspect docker.io/louislam/uptime-kuma:2 --format '{{json .RepoDigests}}'
podman image inspect docker.stirlingpdf.com/stirlingtools/stirling-pdf:2.14.3-fat --format '{{json .RepoDigests}}'
```

Si no hay `RepoDigests`, no inventarlos ni sustituirlos por `Image ID`. Comprobar para cada contenedor ejecutado la imagen efectiva y su versión de aplicación, especialmente el esquema de SQLite de Open WebUI, MariaDB embebida de Uptime Kuma y el dump de PostgreSQL.

## Promoción segura

1. Guardar evidencia del contenedor e imagen efectiva **sin secretos** y verificar el digest real compatible con la arquitectura amd64.
2. Conservar recuperación Restic y dump lógico certificados; comprobar que su contenido restaura con la versión seleccionada.
3. Sustituir la referencia en Compose o `.env` local por `repositorio@sha256:<manifest-digest-verificado>`; **no** usar el ID de imagen local.
4. Ejecutar validación estática y pull controlado de la imagen en entorno de prueba, sin recrear todavía el servicio productivo.
5. Probar salud, persistencia, datos y reversión de **un stack a la vez**. No activar autostart ni alterar los volúmenes.
6. Solo después de PASS explícito promover la referencia al Compose versionado y documentar su plataforma y origen.

**Nota:** este Pull Request no cambia imágenes operativas ni marca el pinning como resuelto. Los otros cuatro incrementos son independientes y seguros de revisar primero.
