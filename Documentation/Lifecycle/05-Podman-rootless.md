# 05 — Podman rootless

**Estado:** VALIDADO

## Plataforma comprobada

```text
Podman 5.4.2
rootless=true
cgroup v2
netavark
pasta
```

Debian 13 incluye Podman 5.4.2 y `podman-compose` en sus repositorios. La instalación utilizada por SineOS se apoya en paquetes Debian.

## Instalar

```bash
sudo apt update
sudo apt install -y \
  podman podman-compose buildah skopeo \
  uidmap passt slirp4netns
```

## Validar rootless

Ejecutar como usuario normal:

```bash
podman --version
podman-compose version
podman info
podman ps -a
podman network ls
podman volume ls
```

Comprobación específica:

```bash
podman info --format '{{.Host.Security.Rootless}}'
```

El resultado esperado es `true`.

## Regla SineOS

- contenedores de usuario mediante Podman rootless;
- no usar `sudo podman` como flujo normal;
- datos persistentes fuera de la capa efímera del contenedor;
- servicios locales publicados en loopback siempre que sea posible;
- arranque manual para los stacks actuales salvo decisión explícita distinta.

## Podman Desktop

Se utilizó para iniciar/detener manualmente servicios. Su procedimiento exacto de instalación todavía no está documentado de forma reproducible y debe revalidarse antes de convertirlo en parte del bootstrap automático.