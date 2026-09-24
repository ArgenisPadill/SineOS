# SineOS — Rotación de secretos

**Estado:** Adoptado  
**Fecha:** 23-09-2026

## Propósito

Definir cómo rotar secretos de SineOS sin exponer valores, romper consumidores ni introducir credenciales en Git.

## Principio

> Primero se identifica el secreto y todos sus consumidores; después se rota; al final se valida servicio por servicio.

La rotación no debe hacerse únicamente por rutina si no existe una razón concreta y un procedimiento probado para actualizar todos los consumidores.

## Cuándo rotar

Rotar cuando:

- exista exposición confirmada;
- una credencial haya sido compartida accidentalmente;
- exista sospecha de compromiso;
- un proveedor lo exija;
- cambie el propietario o alcance del servicio;
- un procedimiento de recuperación requiera reemplazar material criptográfico.

No rotar por defecto cuando:

- el secreto es válido y no existe evidencia de exposición;
- la aplicación genera y administra internamente su material criptográfico;
- no se conoce todavía cómo actualizar todos los consumidores.

## Reglas generales

1. Nunca imprimir el valor en terminal si no es necesario.
2. Nunca copiar el valor a documentación, issues, commits o capturas.
3. Mantener archivos secretos en modo 600 o más restrictivo.
4. Preparar rollback antes de sustituir una credencial funcional.
5. Actualizar todos los consumidores antes de invalidar el valor anterior cuando el proveedor permita convivencia temporal.
6. Validar el servicio después de la rotación.
7. Ejecutar el auditor de secretos al terminar.

## Open WebUI — WEBUI_SECRET_KEY

Ubicación local:

```text
Containers/stacks/open-webui/.env
```

Permisos requeridos:

```text
600
```

El Compose consume el archivo mediante `env_file`.

### Riesgo de rotación

`WEBUI_SECRET_KEY` participa en sesiones y funciones criptográficas de Open WebUI.

Cambiarlo puede invalidar sesiones y puede afectar datos cifrados por la aplicación.

Por tanto:

> No rotar este secreto de forma rutinaria ni a ciegas.

### Procedimiento ante compromiso

1. Crear backup del volumen persistente de Open WebUI.
2. Detener el contenedor.
3. Guardar una copia privada del `.env` actual como rollback.
4. Generar un nuevo valor criptográficamente aleatorio fuera de Git.
5. Sustituir únicamente `WEBUI_SECRET_KEY` en el `.env`.
6. Mantener permisos 600.
7. Recrear Open WebUI desde el Compose.
8. Validar:
   - HTTP local;
   - inicio de sesión;
   - acceso a conversaciones/datos persistentes;
   - integración con Ollama;
   - ausencia de errores criptográficos en logs.
9. Si falla una función dependiente del secreto, restaurar el `.env` anterior y recrear el contenedor.
10. Ejecutar `Scripts/Security/sineos-secrets-audit.sh`.

La rotación real de este secreto no se ha ejecutado porque no existe evidencia de compromiso.

## PostgreSQL — credenciales del stack

Ubicación:

```text
Containers/stacks/postgres/.env
```

Permisos:

```text
600
```

### Regla

La contraseña no debe cambiarse únicamente en el archivo `.env`.

Una rotación correcta requiere actualizar primero la credencial dentro de PostgreSQL y después sincronizar el secreto utilizado por los consumidores.

### Procedimiento

1. Crear backup lógico validado de PostgreSQL.
2. Identificar todos los consumidores de la cuenta.
3. Generar un nuevo valor fuera de Git.
4. Cambiar la contraseña dentro de PostgreSQL para el rol correspondiente.
5. Actualizar el `.env` local y cualquier consumidor autorizado.
6. Mantener permisos 600.
7. Reiniciar o recrear únicamente los consumidores que lo necesiten.
8. Validar:
   - `pg_isready`;
   - conexión autenticada;
   - aplicaciones consumidoras;
   - logs.
9. Ejecutar el auditor de secretos.

Mientras TD-003 siga abierto, una rotación de credenciales PostgreSQL debe considerarse operación sensible y no hacerse sin backup/restauración previamente validados.

## Uptime Kuma — Push URLs

Ubicaciones actuales:

```text
~/.config/sineos/monitoring/open-webui.env
~/.config/sineos/monitoring/postgresql.env
```

Permisos:

```text
600
```

Las Push URLs se tratan como secretos porque incorporan identificadores/token de monitor.

### Procedimiento

1. Crear o regenerar la URL Push en Uptime Kuma.
2. Actualizar el archivo local correspondiente sin mostrar el valor.
3. Mantener permisos 600.
4. Ejecutar el check de monitoreo.
5. Confirmar recepción del heartbeat.
6. Retirar el valor anterior si sigue activo.
7. Ejecutar el auditor de secretos.

## Stirling PDF — JWT keys generadas por la aplicación

Stirling PDF administra su propio material JWT bajo el volumen persistente.

No se rota manualmente mientras no exista:

- incidente que lo requiera;
- procedimiento soportado por la aplicación;
- backup validado;
- evidencia de que la rotación no rompe datos o autenticación.

En la versión 2.14.3 existe además la limitación documentada de permisos bajo `/configs`.

## Git / SSH

Las claves SSH no forman parte de los secretos gestionados por los stacks de contenedores.

Ante compromiso de una clave SSH:

1. generar una nueva clave dedicada;
2. registrar la clave pública en el proveedor;
3. validar autenticación;
4. retirar la clave pública anterior;
5. eliminar o archivar de forma segura la clave privada comprometida;
6. comprobar que ninguna clave privada esté rastreada por Git.

## Evidencia y documentación

La documentación registra:

- nombre/tipo del secreto;
- fecha de rotación;
- componente afectado;
- resultado de validación;
- motivo.

Nunca registra el valor.

## Validación posterior

Después de cualquier rotación:

```bash
bash Scripts/Security/sineos-secrets-audit.sh
```

El resultado esperado es:

```text
Advertencias: 0
Errores: 0
RESULTADO: OK
```

Si la rotación afecta un servicio, también debe ejecutarse su validación funcional específica.

## Rollback

Toda rotación que pueda interrumpir servicio debe tener un rollback definido antes del cambio.

Un rollback puede consistir en:

- restaurar el archivo secreto anterior desde una copia privada;
- revertir temporalmente una contraseña del servicio;
- restaurar un backup de configuración;
- recrear el consumidor con el secreto anterior.

El rollback nunca debe publicarse en Git si contiene el valor real.

## Estado actual

A 23-09-2026:

- no existe evidencia de secretos publicados en Git;
- Gitleaks reporta 0 hallazgos en historial;
- el snapshot versionable reporta 0 hallazgos;
- Open WebUI conserva un secret persistente validado;
- PostgreSQL y Push URLs están protegidos localmente;
- no se requiere rotación inmediata de ningún secreto conocido.
