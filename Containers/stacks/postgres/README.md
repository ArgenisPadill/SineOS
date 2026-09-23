# SineOS — PostgreSQL

Stack de PostgreSQL 18 para SineOS.

## Plataforma
- Runtime: Podman rootless
- Imagen: `docker.io/library/postgres:18`
- Contenedor: `sineos-postgres`
- Host: `127.0.0.1:5432`
- Persistencia: `Containers/volumes/postgres/data`
- Arranque: manual desde Podman Desktop

## Configuración
`.env` contiene la configuración local y credenciales; no se versiona. `.env.example` conserva solo la estructura reproducible.

## Persistencia
`Containers/volumes/postgres/data -> /var/lib/postgresql`. Los datos sobrevivieron a la recreación controlada del contenedor.

## Seguridad
El Compose publica únicamente loopback. Las credenciales permanecen fuera de Git.

## Validación
```bash
podman exec sineos-postgres pg_isready -U sineos -d sineos
```

También se validaron DBeaver, pgAdmin y persistencia. El Compose actual no define healthcheck; que `podman ps` no muestre `healthy` no implica una falla.

## Autostart
La antigua intención de Quadlet fue reemplazada por arranque manual. No debe restaurarse autostart salvo una decisión explícita posterior.
