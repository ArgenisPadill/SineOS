# Uptime Kuma — SineOS

Sistema de monitoreo local de servicios de SineOS.

## Arquitectura

- Imagen: `docker.io/louislam/uptime-kuma:2`
- Contenedor: `sineos-uptime-kuma`
- Interfaz: `http://127.0.0.1:3001`
- Base de datos: Embedded MariaDB
- Datos persistentes: `Containers/volumes/uptime-kuma/data`
- Red compartida de monitoreo: `sineos-monitoring`
- Ejecución: rootless Podman

## Política de arranque

Uptime Kuma NO se inicia automáticamente.

El contenedor se inicia y detiene manualmente desde Podman Desktop.

Los timers de monitoreo de SineOS no arrancan contenedores.

## Servicios monitorizados

### Stirling PDF

Monitor HTTP directo a través de la red interna de Podman:

`http://sineos-stirling-pdf:8080`

No requiere exponer Stirling PDF a la LAN.

### Open WebUI

Open WebUI utiliza `network_mode: pasta` y publica únicamente:

`127.0.0.1:3000`

Por esta razón no se conecta a la red bridge `sineos-monitoring`.

El host comprueba:

`http://127.0.0.1:3000/health`

Script:

`Scripts/Monitoring/check-open-webui.sh`

Si el servicio responde correctamente, el host envía un heartbeat mediante un monitor Push de Uptime Kuma.

Timer:

`sineos-monitor-open-webui.timer`

Frecuencia: 30 segundos.

### PostgreSQL

PostgreSQL se comprueba desde el host mediante:

`pg_isready -U sineos -d sineos`

ejecutado dentro del contenedor `sineos-postgres`.

Script:

`Scripts/Monitoring/check-postgresql.sh`

Si PostgreSQL acepta conexiones, se envía un heartbeat al monitor Push correspondiente.

Timer:

`sineos-monitor-postgresql.timer`

Frecuencia: 30 segundos.

## Secretos

Las URLs Push NO se almacenan en este repositorio.

Se encuentran únicamente en:

`~/.config/sineos/monitoring/open-webui.env`

`~/.config/sineos/monitoring/postgresql.env`

Permisos requeridos:

`600`

Estos archivos nunca deben añadirse a Git.

## Red de monitoreo

Red externa de Podman:

`sineos-monitoring`

Driver:

`bridge`

La utilizan Uptime Kuma y los servicios compatibles con networking bridge, como Stirling PDF.

## Seguridad

La interfaz web de Uptime Kuma está publicada únicamente en:

`127.0.0.1:3001`

No debe exponerse a la LAN salvo que exista una necesidad explícita y se revise previamente la política de seguridad de SineOS.
