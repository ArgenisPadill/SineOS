# 03 — XFCE y escritorio reproducible

**Estado:** VALIDADO

## Objetivo

Instalar/configurar XFCE y aplicar la experiencia visual reproducible de SineOS.

El script oficial es:

```text
Scripts/Desktop/sineos-xfce-macos.sh
```

## Desde el repositorio

```bash
cd "$HOME/Workspace/SineOS"
chmod +x Scripts/Desktop/sineos-xfce-macos.sh
./Scripts/Desktop/sineos-xfce-macos.sh install
```

El instalador puede instalar XFCE/LightDM y dependencias visuales. Si todavía no existe una sesión XFCE activa, programa la aplicación del diseño para el primer inicio.

## Solo paquetes

```bash
./Scripts/Desktop/sineos-xfce-macos.sh packages
```

## Aplicar o actualizar diseño

Ejecutar como usuario normal dentro de XFCE:

```bash
./Scripts/Desktop/sineos-xfce-macos.sh apply
```

## Estado

```bash
./Scripts/Desktop/sineos-xfce-macos.sh status
```

## Restaurar último respaldo

```bash
./Scripts/Desktop/sineos-xfce-macos.sh restore
```

## Validación

El script fue diseñado para crear respaldo, evitar reconstrucciones innecesarias y no tocar red, audio, Bluetooth, energía, kernel o firmware.

No debe sustituirse su lógica por `xfce4-panel --restart`; durante las pruebas ese flujo podía cerrar el panel sin volver a levantarlo.

## Documento completo

`Documentation/Operations/XFCE-Visual-Configuration.md`