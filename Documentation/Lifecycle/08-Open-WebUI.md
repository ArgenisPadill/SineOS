# 08 — Open WebUI

**Estado:** VALIDADO CON DEUDA TÉCNICA

## Arquitectura

```text
Navegador
   ↓
127.0.0.1:3000
   ↓
Open WebUI / Podman rootless
   ↓
host.containers.internal:11434
   ↓
Ollama
```

## Definición versionada

```text
Containers/stacks/open-webui/compose.yaml
```

## Crear/iniciar

```bash
cd "$HOME/Workspace/SineOS/Containers/stacks/open-webui"
podman-compose -f compose.yaml config
podman-compose -f compose.yaml pull
podman-compose -f compose.yaml up -d
```

## Validar

```bash
podman ps --filter name=sineos-open-webui
curl -f http://127.0.0.1:3000/health
```

Abrir en navegador:

```text
http://127.0.0.1:3000
```

## Persistencia

```text
Containers/volumes/open-webui/data
```

Este directorio queda fuera de Git.

## Red

La configuración actual utiliza `network_mode: pasta` y:

```text
OLLAMA_BASE_URL=http://host.containers.internal:11434
```

## Política de arranque

El uso cotidiano se realiza manualmente desde Podman Desktop.

El Compose todavía contiene `restart: unless-stopped`; esta divergencia está registrada como deuda y debe eliminarse mediante recreación controlada, no editando a ciegas un contenedor en uso.

## Deuda pendiente

- fijar versión o digest en lugar de `:main`;
- secret persistente fuera de Git;
- retirar `restart: unless-stopped` de forma controlada;
- definir backup/restore necesario.

## Regla de seguridad

No cambiar `127.0.0.1:3000` por `0.0.0.0:3000` sin una revisión explícita.

## Documentación

`Documentation/Operations/Open-WebUI.md`