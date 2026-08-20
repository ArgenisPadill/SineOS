# SineOS — PostgreSQL

Stack de PostgreSQL 18 para el ecosistema SineOS.

## Plataforma

- Runtime: Podman rootless
- Orquestación: podman-compose
- Imagen: docker.io/library/postgres:18
- Arquitectura: amd64
- Puerto: 5432
- Persistencia: Containers/volumes/postgres/

## Configuración

La configuración local se encuentra en `.env`.
El archivo `.env` contiene credenciales y no debe versionarse.
La plantilla `.env.example` sirve como referencia para reconstruir la configuración.

## Operación

```bash
make config
make pull
make up
make ps
make logs
make health
make restart
make down
```

## Persistencia

Los datos PostgreSQL se almacenan fuera del contenedor mediante un bind mount.
PostgreSQL 18 utiliza `/var/lib/postgresql` como punto de montaje recomendado.

## Seguridad

El contenedor funciona mediante Podman rootless.
Las credenciales se mantienen fuera del repositorio Git.

## Estado

Stack funcional y validado.

Se verificó:

- creación y arranque del contenedor;
- healthcheck de PostgreSQL;
- conexión local mediante PostgreSQL;
- exposición del puerto 5432;
- persistencia mediante bind mount;
- persistencia de datos después de reiniciar;
- persistencia de datos después de eliminar y recrear el contenedor.
