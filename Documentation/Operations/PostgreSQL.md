# SineOS — PostgreSQL 18

## Estado operativo

PostgreSQL es el servicio de base de datos persistente principal de SineOS. Se ejecuta con Podman rootless, almacenamiento persistente y arranque manual desde Podman Desktop.

## Estructura

La definición versionada reside en `Containers/stacks/postgres/`. La documentación usa `${SINEOS_REPO}` para representar la raíz local del repositorio y nunca publica su ruta absoluta real.

Los datos persistentes se montan dentro del contenedor en el directorio estándar de PostgreSQL. Los datos reales permanecen excluidos de Git.

## Configuración y secretos

La configuración local utiliza `.env`, excluido del repositorio. `.env.example` documenta únicamente la estructura necesaria para reconstruir el servicio.

No se publican:

- contraseñas o tokens;
- URLs de monitoreo;
- rutas personales;
- direcciones de redes privadas;
- identificadores de dispositivos o cuentas.

## Red

PostgreSQL solo se expone a la interfaz local del equipo. La documentación representa el acceso como:

```text
localhost:<POSTGRES_PORT>
```

Los detalles concretos de enlace permanecen en la configuración operativa y no se duplican en documentación pública.

## Política de arranque

El servicio se inicia y detiene manualmente. La antigua intención de usar systemd/Quadlet para autostart fue descartada mientras esta política siga vigente.

## Validación

El Compose vigente no define healthcheck. La disponibilidad se comprueba explícitamente con `pg_isready` dentro del contenedor.

Se validaron:

- persistencia tras recreación controlada;
- conexión mediante clientes locales de administración;
- disponibilidad del servidor;
- funcionamiento del monitoreo.

Los parámetros concretos de conexión no se publican.

## Monitoreo

`Scripts/Monitoring/check-postgresql.sh` comprueba disponibilidad y utiliza una URL Push almacenada fuera del repositorio.

## Pendientes

- formalizar gestión de secretos;
- definir frecuencia y retención de backups;
- definir destino cifrado;
- probar restauración completa;
- documentar Disaster Recovery.

Un snapshot no sustituye un backup y un backup no se considera validado hasta probar su restauración.

## Estado

| Elemento | Estado |
|---|---|
| PostgreSQL 18 | Operativo |
| Podman rootless | Operativo |
| Persistencia | Validada |
| Exposición | Solo local |
| Arranque | Manual |
| Monitoreo | Operativo |
| Backup/restauración | Pendiente |
