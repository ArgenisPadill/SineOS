# Stirling PDF — SineOS

Herramienta local para manipulación y procesamiento de documentos PDF.

## Arquitectura

- Imagen: `docker.stirlingpdf.com/stirlingtools/stirling-pdf:2.14.3-fat`
- Contenedor: `sineos-stirling-pdf`
- Interfaz: `http://127.0.0.1:8080`
- Ejecución: rootless Podman
- Idioma predeterminado: `es-ES`
- Login interno: deshabilitado para uso exclusivamente local

## Persistencia

Los datos persistentes se encuentran en:

`Containers/volumes/stirling-pdf/`

Incluyen:

- `configs`
- `logs`
- `customFiles`
- `pipeline`
- `tessdata`

Los volúmenes persistentes están excluidos de Git.

## Política de arranque

Stirling PDF NO se inicia automáticamente.

El contenedor se inicia y detiene manualmente desde Podman Desktop.

## Red

La interfaz para el usuario está publicada únicamente en:

`127.0.0.1:8080`

Además, el contenedor pertenece a la red interna:

`sineos-monitoring`

Esto permite que Uptime Kuma compruebe el servicio mediante DNS interno de Podman:

`http://sineos-stirling-pdf:8080`

sin exponer el servicio a la red local.

## Monitoreo

Uptime Kuma realiza una comprobación HTTP directa mediante la red `sineos-monitoring`.

No se requieren tokens Push ni credenciales adicionales para este monitor.

## Seguridad

El servicio está diseñado actualmente para uso local.

No debe cambiarse el binding de `127.0.0.1:8080` a `0.0.0.0:8080` sin revisar previamente autenticación, firewall y política de exposición de SineOS.
