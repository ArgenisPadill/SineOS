# 13 — Programas, scripts y automatización

**Estado:** ADOPTADO COMO ESTÁNDAR

## Programas propios

El catálogo oficial está en:

```text
Apps/README.md
```

Actualmente incluye NetworkPrivacy.

Comprobar:

```bash
find "$HOME/Workspace/SineOS/Apps" -maxdepth 3 -type f -print
```

## Scripts

El catálogo oficial está en:

```text
Scripts/README.md
```

Inventario:

```bash
find "$HOME/Workspace/SineOS/Scripts" -maxdepth 3 -type f -print | sort
```

## Categorías

```text
pilar
operativo recurrente
instalación/integración
migración
one-shot
experimental
```

## Regla

Un comando que se repite es candidato a script. Un script que sostiene una función de SineOS es infraestructura.

Un programa propio debe documentarse e instalarse como componente, no quedar escondido como archivo Python suelto.

## Automatización junto al componente

No toda automatización vive en `Scripts/`.

Ejemplo:

```text
Containers/stacks/postgres/Makefile
```

Validar interfaz:

```bash
cd "$HOME/Workspace/SineOS/Containers/stacks/postgres"
make help
```

## Buscar artefactos locales aún no versionados

Esta comprobación no modifica nada:

```bash
find "$HOME" -maxdepth 4 -type f \
  \( -name '*.sh' -o -name '*.py' -o -name '*.service' -o -name '*.timer' \) \
  2>/dev/null | sort
```

Cada hallazgo debe revisarse antes de publicarlo para eliminar secretos, rutas privadas y scripts reemplazados.

## Documentación

- `Documentation/Architecture/Script-Standard.md`
- `Documentation/Architecture/Native-Applications.md`
- `Scripts/README.md`
- `Apps/README.md`