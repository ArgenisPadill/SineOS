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


## Permisos de datos sensibles

Durante la revisión de seguridad del 23-09-2026 se detectó que Stirling PDF 2.14.3 restablece recursivamente a modo `755` el contenido de `/configs` durante cada arranque.

Esto afecta también artefactos generados por la propia aplicación bajo:

```text
/configs/backup/keys/
/configs/backup/db/
```

Se comprobó que:

- la clave JWT privada, la clave pública y el backup SQL pertenecen a UID/GID `1000:1000` dentro del namespace rootless;
- Stirling PDF ejecuta la aplicación principal con UID `1000`;
- aplicar manualmente `600/644` funciona mientras el contenedor está detenido;
- al siguiente arranque, la imagen 2.14.3 vuelve a establecer `755`;
- el servicio continúa operativo y carga correctamente la clave JWT.

La causa está en el script upstream `scripts/init-without-ocr.sh` de la versión `v2.14.3`, que ejecuta un `chmod -R 755` sobre `/configs`.

No se implementa un parche local permanente porque supondría mantener una imagen derivada o alterar el entrypoint de un componente externo.

La rama actual upstream ya cambió esta lógica para aplicar `755` únicamente a directorios, pero la versión estable más reciente revisada sigue siendo `2.14.3`.

### Mitigaciones actuales

- la interfaz permanece limitada a `127.0.0.1:8080`;
- Podman se ejecuta rootless;
- el repositorio y los volúmenes se encuentran bajo el HOME del usuario, cuyo acceso está restringido;
- `Containers/volumes/*` está excluido de Git;
- no se exponen las claves ni los backups en documentación pública.

### Acción futura

Cuando exista una versión estable posterior a `2.14.3`, revisar específicamente el comportamiento de permisos de `/configs` antes de actualizar y comprobar que los archivos sensibles pueden conservar modos restrictivos como `600`.


## Seguridad

El servicio está diseñado actualmente para uso local.

No debe cambiarse el binding de `127.0.0.1:8080` a `0.0.0.0:8080` sin revisar previamente autenticación, firewall y política de exposición de SineOS.
