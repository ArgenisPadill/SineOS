# 10 — Servicios locales y monitoreo

**Estado:** VALIDADO CON HUECOS DE REPRODUCIBILIDAD

## Componentes

```text
Stirling PDF  -> 127.0.0.1:8080
Uptime Kuma   -> 127.0.0.1:3001
Open WebUI    -> 127.0.0.1:3000
PostgreSQL    -> 127.0.0.1:5432
```

Los stacks se ejecutan con Podman rootless y, salvo deuda específica de Open WebUI, la intención operativa actual es arranque manual.

## Crear red interna de monitoreo

```bash
podman network exists sineos-monitoring || podman network create sineos-monitoring
podman network inspect sineos-monitoring
```

## Uptime Kuma

```bash
cd "$HOME/Workspace/SineOS/Containers/stacks/uptime-kuma"
podman-compose -f compose.yaml config
podman-compose -f compose.yaml pull
podman-compose -f compose.yaml up -d
curl -I http://127.0.0.1:3001
```

Interfaz:

```text
http://127.0.0.1:3001
```

## Stirling PDF

```bash
cd "$HOME/Workspace/SineOS/Containers/stacks/stirling-pdf"
podman-compose -f compose.yaml config
podman-compose -f compose.yaml pull
podman-compose -f compose.yaml up -d
curl -I http://127.0.0.1:8080
```

Stirling PDF usa la imagen validada `2.14.3-fat`, idioma `es-ES` y login deshabilitado para uso local.

## Monitor directo de Stirling PDF

Desde Uptime Kuma se utiliza la red interna:

```text
http://sineos-stirling-pdf:8080
```

## Open WebUI y PostgreSQL

Estos servicios usan scripts Push desde el host:

```text
Scripts/Monitoring/check-open-webui.sh
Scripts/Monitoring/check-postgresql.sh
```

Los Push URLs se guardan fuera de Git:

```bash
mkdir -p ~/.config/sineos/monitoring
chmod 700 ~/.config/sineos/monitoring
```

Ejemplo de archivo local:

```bash
printf '%s\n' 'PUSH_URL="PEGAR_URL_PUSH_AQUI"' > ~/.config/sineos/monitoring/open-webui.env
chmod 600 ~/.config/sineos/monitoring/open-webui.env
```

Para PostgreSQL:

```bash
printf '%s\n' 'PUSH_URL="PEGAR_URL_PUSH_AQUI"' > ~/.config/sineos/monitoring/postgresql.env
chmod 600 ~/.config/sineos/monitoring/postgresql.env
```

## Validar scripts

```bash
cd "$HOME/Workspace/SineOS"
./Scripts/Monitoring/check-open-webui.sh
./Scripts/Monitoring/check-postgresql.sh
```

## Timers existentes

Durante la construcción se utilizaron timers de usuario con frecuencia de 30 segundos:

```text
sineos-monitor-open-webui.timer
sineos-monitor-postgresql.timer
```

Comprobar el equipo actual:

```bash
systemctl --user status sineos-monitor-open-webui.timer --no-pager
systemctl --user status sineos-monitor-postgresql.timer --no-pager
systemctl --user list-timers --all | grep sineos
```

## Hueco importante

Las unidades `.service`/`.timer` todavía no están versionadas en Git. Por tanto, **no debe considerarse reproducible todavía la instalación del monitoreo recurrente**.

Una siguiente iteración debe recuperar las unidades reales del sistema, sanearlas, versionarlas e incluir un instalador.

## Documentación

- `Containers/stacks/uptime-kuma/README.md`
- `Containers/stacks/stirling-pdf/README.md`
- `Scripts/README.md`