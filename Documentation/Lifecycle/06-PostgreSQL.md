# 06 — PostgreSQL 18

**Estado:** VALIDADO

## Arquitectura

```text
PostgreSQL 18
Podman rootless
Contenedor: sineos-postgres
Host: 127.0.0.1:5432
Persistencia: Containers/volumes/postgres/data
Arranque: manual
```

## Preparar configuración

```bash
cd "$HOME/Workspace/SineOS/Containers/stacks/postgres"
cp .env.example .env
chmod 600 .env
```

Editar `.env` y cambiar obligatoriamente:

```text
POSTGRES_PASSWORD=CAMBIAR_ESTA_CONTRASENA
```

Las credenciales reales no pertenecen a Git.

## Validar Compose

```bash
cd "$HOME/Workspace/SineOS/Containers/stacks/postgres"
make config
```

## Descargar imagen

```bash
make pull
```

## Crear/iniciar inicialmente

```bash
make up
```

Después de creado, la política actual de SineOS es inicio y detención manual desde Podman Desktop. No restaurar autostart sin una decisión explícita.

## Validar

```bash
podman ps --filter name=sineos-postgres
podman exec sineos-postgres pg_isready -U sineos -d sineos
```

Comprobar publicación:

```bash
ss -ltn | grep ':5432'
```

Debe estar asociado a `127.0.0.1`, no a `0.0.0.0`.

## Persistencia

Los datos sobrevivieron una recreación controlada del contenedor. No borrar `Containers/volumes/postgres/data` como parte de una actualización normal.

## Interfaces operativas

```bash
cd "$HOME/Workspace/SineOS/Containers/stacks/postgres"
make ps
make logs
make health
```

## Pendiente

- backup automático;
- restore probado;
- rotación formal de credenciales;
- política de secretos;
- Disaster Recovery.

## Documentación

- `Documentation/Operations/PostgreSQL.md`
- `Containers/stacks/postgres/README.md`