# 09 — Knowledge Vault y Miyo

**Estado:** VALIDADO / REINSTALACIÓN COMPLETA DE MIYO PENDIENTE

## Separación fundamental

```text
Repositorio SineOS
    código, infraestructura y documentación

Knowledge Vault
    conocimiento permanente en Obsidian
```

El Vault no es el repositorio Git.

## Obsidian

Obsidian actúa como fuente de verdad del conocimiento. El mecanismo exacto de instalación de Obsidian no está todavía documentado como bootstrap reproducible y debe añadirse cuando se revalide.

## Miyo

Versión validada:

```text
Miyo 0.2.27
```

Ubicación utilizada para la AppImage:

```text
~/.local/opt/miyo/Miyo.AppImage
```

Preparación genérica del archivo descargado:

```bash
mkdir -p ~/.local/opt/miyo
chmod 755 ~/.local/opt/miyo/Miyo.AppImage
~/.local/opt/miyo/Miyo.AppImage
```

La URL/origen exacto de descarga y el procedimiento limpio completo siguen pendientes de documentar.

## CLI

Miyo Desktop administra:

```text
~/.miyo/bin/miyo
```

Validación:

```bash
~/.miyo/bin/miyo --help
~/.miyo/bin/miyo files
~/.miyo/bin/miyo search "consulta"
```

## Servicio

El servicio local validado escucha en:

```text
127.0.0.1:8742
```

Comprobar:

```bash
ss -ltn | grep ':8742'
```

## Scope

Miyo debe indexar el Vault, no `~/Workspace/SineOS`.

## Arquitectura validada

```text
Obsidian
  ↓
Miyo
  ↓
Copilot / OpenCode
  ↓
LLM
```

Se validó recuperación semántica, watcher de cambios, eliminación del índice y flujos con DeepSeek/Gemini.

## Regla de recuperación

El índice de Miyo es reconstruible. El dato importante es el Knowledge Vault.

## Pendiente

- reinstalación reproducible completa;
- backup independiente del Vault;
- benchmark semántico multinota;
- pruebas de recuperación.

## Documentación

- `Documentation/Architecture/Knowledge-Vault.md`
- `Documentation/Operations/Miyo.md`