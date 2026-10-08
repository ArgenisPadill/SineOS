# SDE — Manifiesto técnico Alpha 0.1

**Fecha:** 07-10-2026  
**Estado:** planeación técnica inicial / congelado como baseline de Alpha 0.1  
**Issue maestro:** https://github.com/ArgenisPadill/SineOS/issues/1  
**Plataforma:** Debian 13 (Trixie) + XFCE 4.20 + X11 + LightDM

## Objetivo de Alpha 0.1

Alpha 0.1 no intenta entregar todavía toda la experiencia visual final.

Su objetivo principal es demostrar que SDE puede:

1. detectar el estado actual del escritorio;
2. crear un respaldo pre-SDE;
3. registrar qué archivos y ajustes serán propiedad de SDE;
4. aplicar cambios de forma idempotente;
5. validar el resultado;
6. entrar en Modo seguro si algo falla;
7. restaurar el estado anterior;
8. desinstalar sin borrar configuración ajena.

> Antes de modificar el escritorio, SDE debe demostrar que puede volver atrás.

---

# Arquitectura de paquetes prevista

## sineos-desktop

Metapaquete de la experiencia soportada.

### Depends
- sineos-desktop-core
- sineos-desktop-visual
- sineos-desktop-assets
- sineos-desktop-recovery

### Recommends
- sineos-desktop-tools

### Suggests
- módulos opcionales futuros.

## sineos-desktop-core

Responsable de:
- CLI `sineos-desktop`;
- esquema de configuración;
- migraciones;
- integración XFCE;
- validación;
- displays;
- Safe Areas;
- estado operativo;
- hooks de sesión;
- integración con NetworkManager, Polkit y otras capas del sistema sin reemplazarlas.

## sineos-desktop-visual

Responsable de:
- Picom;
- panel/dock;
- GTK CSS;
- XFWM;
- Rofi;
- OSD;
- visual de notificaciones;
- integración Qt;
- materiales, movimiento y foco.

## sineos-desktop-assets

Responsable de:
- wallpaper;
- logotipo;
- cursor;
- iconos SineOS;
- SVG fuente;
- recursos visuales;
- tema Plymouth;
- recursos de login/bloqueo.

## sineos-desktop-tools

Metapaquete de herramientas bajo demanda.

## sineos-desktop-recovery

Debe ser el paquete con menor dependencia posible.

Responsable de:
- backup pre-SDE;
- Last Known Good;
- safe-mode;
- health;
- repair;
- rollback;
- restore pre-SDE;
- metadatos de recuperación;
- bootstrap local/offline.

---

# Paquetes Debian confirmados para la base

Los siguientes nombres existen en Debian 13/Trixie y son candidatos directos para SDE.

## Sesión y escritorio

- `lightdm`
- `slick-greeter`
- `xfce4-panel`
- `xfce4-panel-profiles`
- `xfce4-screensaver`
- `xfce4-notifyd`
- `xfce4-screenshooter`
- `xfce4-power-manager`
- `xfce4-pulseaudio-plugin`

## Panel y experiencia

- `xfce4-appmenu-plugin`
- `xfce4-docklike-plugin`

## Composición y launcher

- `picom`
- `rofi`

## Pantallas

- `x11-xserver-utils`
- `autorandr` como auxiliar opcional, no como backend autoritativo.

## Captura y anotación

- `flameshot`
- `gromit-mpx`
- `xfce4-screenshooter` como fallback.

## Energía y hardware

- `tlp`
- `smartmontools` como candidato para salud SMART;
- herramientas que TLP ya utiliza o recomienda como `pciutils`, `usbutils`, `rfkill`, `iw` y `ethtool` cuando corresponda.

## Integración Qt

- `qt5ct`
- `qt6ct`

## Tipografía

- `fonts-inter`
- `fonts-jetbrains-mono`
- Noto como fallback amplio mediante paquetes Debian apropiados que se fijarán en el manifiesto final.

## Arranque gráfico

- `plymouth`

---

# Política de dependencias

## Depends

Solo componentes sin los cuales el paquete correspondiente no puede cumplir su función.

Ejemplo:
- recovery no debe depender de Picom;
- core no debe depender de OBS;
- assets no debe introducir servicios residentes.

## Recommends

Componentes de la experiencia normal que pueden faltar sin dejar SineOS inutilizable.

## Suggests

Herramientas avanzadas, experimentales o no esenciales.

---

# Componentes que NO son dependencia crítica

No deben convertirse en requisito para arrancar o recuperar:

- Picom;
- Rofi;
- Docklike;
- Global Menu;
- Flameshot;
- Gromit-MPX;
- grabadores;
- OBS;
- pantalla inalámbrica;
- Overview;
- autorandr.

---

# Árbol de archivos propuesto

## Configuración del usuario

```text
~/.config/sineos-desktop/
├── config-version
├── appearance.conf
├── accessibility.conf
├── shortcuts.conf
├── privacy.conf
├── updates.conf
└── hardware/
    ├── display.conf
    ├── gpu.conf
    └── power.conf
```

## Estado local

```text
~/.local/state/sineos-desktop/
├── logs/
│   └── remote-access/
├── reports/
│   ├── applications/
│   ├── hardware/
│   ├── health/
│   ├── recovery/
│   └── updates/
├── recovery/
│   ├── pre-sde/
│   ├── last-known-good/
│   └── checkpoints/
└── state/
```

## Datos compartidos del sistema

```text
/usr/share/sineos-desktop/
├── assets/
├── templates/
├── themes/
├── plymouth/
├── recovery/
└── schema/
```

## Ejecutables

```text
/usr/bin/sineos-desktop
/usr/libexec/sineos-desktop/
```

Los nombres finales de helpers se fijarán cuando se escriba la implementación.

---

# Archivos propiedad de SDE

SDE solo modifica o genera archivos que declare explícitamente como propios.

Nunca debe apropiarse indiscriminadamente de:
- todo `~/.config/xfce4`;
- todo `/etc/lightdm`;
- todo `/etc/tlp.conf`;
- toda configuración de NetworkManager.

Cuando sea necesario integrar archivos de terceros:
1. respaldar;
2. registrar hash/estado anterior;
3. modificar únicamente bloques/rutas conocidas;
4. validar;
5. permitir rollback.

---

# Respaldo pre-SDE

Antes del primer cambio se debe capturar, como mínimo:

- XFConf relevante;
- panel XFCE;
- perfil de panel;
- autostart;
- atajos;
- wallpaper;
- tema GTK/XFWM;
- iconos;
- cursor;
- Picom;
- LightDM;
- locker;
- TLP;
- configuración de displays;
- asociaciones relevantes;
- listado de paquetes implicados;
- versiones;
- fecha/hora;
- commit/release SDE que realizará la migración.

El respaldo debe incluir un manifiesto que permita saber exactamente qué se guardó.

---

# CLI mínima de Alpha 0.1

La primera CLI debe priorizar recovery sobre personalización.

```text
sineos-desktop status
sineos-desktop health
sineos-desktop backup pre-sde
sineos-desktop backup verify
sineos-desktop safe-mode
sineos-desktop repair
sineos-desktop rollback
sineos-desktop restore pre-sde
sineos-desktop version
```

Los nombres son baseline de diseño; la implementación puede ajustar sintaxis sin cambiar las capacidades.

---

# Scripts/helpers iniciales

Se prevén módulos separados para:

- inventario del sistema;
- captura pre-SDE;
- verificación de backup;
- apply;
- validate;
- rollback;
- safe-mode;
- restore;
- health;
- migración de esquema;
- logging.

Evitar un único script monolítico.

---

# Idempotencia

Ejecutar dos veces una operación debe:
- detectar estado existente;
- no duplicar paneles;
- no duplicar autostart;
- no crear backups idénticos sin motivo;
- no agregar repetidamente líneas a archivos;
- no reemplazar un Last Known Good sano por un estado fallido.

---

# Transacción de instalación

Conceptualmente:

```text
preflight
   ↓
inventario
   ↓
backup pre-SDE
   ↓
verify backup
   ↓
crear checkpoint
   ↓
aplicar cambio
   ↓
validar
   ↓
promover a Last Known Good
```

Ante falla:

```text
detener aplicación de cambios
   ↓
registrar error
   ↓
rollback del alcance modificado
   ↓
validar XFCE funcional
   ↓
Modo seguro si no se recupera
```

---

# Preflight obligatorio

Antes de modificar:
- Debian 13/Trixie;
- XFCE compatible;
- X11;
- LightDM;
- espacio libre suficiente;
- filesystem escribible;
- estado de dpkg/apt coherente;
- no existir actualización rota;
- backup path disponible;
- permisos correctos;
- hibernación no se toca todavía en Fase 1;
- no modificar servicios Podman/PostgreSQL ni infraestructura no relacionada.

---

# Alpha 0.1 — alcance concreto

## Entra

- estructura de paquetes;
- CLI mínima;
- inventario;
- backup pre-SDE;
- validación de backup;
- Last Known Good;
- checkpoint;
- rollback;
- restore pre-SDE;
- Modo seguro básico;
- health básico;
- logging;
- esquema/config-version;
- documentación de recuperación.

## No entra todavía

- tema final;
- wallpaper final;
- cursor final;
- panel final;
- Docklike final;
- Picom final;
- Plymouth final;
- Slick Greeter final;
- Super+P;
- políticas completas de red;
- impresión/escaneo;
- privacidad completa;
- hardware health completo.

Esos componentes aparecen en Alpha posteriores siguiendo el roadmap.

---

# Gates de Alpha 0.1

No se considera aprobada hasta demostrar físicamente:

1. el escritorio actual puede respaldarse;
2. el backup puede verificarse;
3. una segunda ejecución no corrompe el estado;
4. se puede aplicar una modificación SDE de prueba;
5. se puede hacer rollback;
6. se puede restaurar el estado pre-SDE;
7. XFCE sigue iniciando;
8. recovery funciona desde terminal/TTY;
9. el repositorio queda sincronizado con la versión probada;
10. existe documentación suficiente para repetirlo.

---

# Política de fuentes

Prioridad:

1. Debian 13/Trixie;
2. Debian Backports si hay justificación documentada;
3. paquete SineOS construido desde release upstream fijo;
4. nunca `main/master` móvil para producción;
5. sin PPA Ubuntu;
6. sin instaladores remotos opacos.

---

# Especificación de backup/restore

La especificación detallada y congelada del respaldo pre-SDE, propiedad de archivos, validación, dry-run, rollback y restauración reanudable se encuentra en:

`Documentation/Architecture/SDE-Alpha-0.1-Backup-Restore-Spec.md`

Decisiones obligatorias:
- backup local sin cifrado, con permisos estrictos;
- respaldo pre-SDE inmutable una vez validado;
- `manifest.json` + `README.md` + `checksums.sha256`;
- SHA-256;
- copias reales como baseline;
- preferencia por archivos `conf.d` propios;
- modelo original/aplicado/actual para conflictos;
- verify + restore dry-run obligatorios antes de modificar SDE;
- restore con un solo comando;
- orden funcional antes que visual;
- `restore-state.json` para reanudación;
- archivar estado de restore cuando termina bien y conservarlo cuando falla.

---

# Especificación de propiedad y conflictos

La especificación congelada del registro de propiedad, tipos `owned` / `managed-block` / `observed`, comparación previous/applied/current, resolución de conflictos y uninstall seguro se encuentra en:

`Documentation/Architecture/SDE-Alpha-0.1-Ownership-Conflict-Spec.md`

---

# Pendientes técnicos antes de escribir código

- confirmar inventario real de paquetes ya instalados en la laptop de referencia;
- confirmar arquitectura CPU;
- confirmar GPU y driver;
- confirmar esquema de particiones/swap;
- confirmar estado real de hibernación;
- confirmar compositor actual;
- confirmar greeter actual;
- confirmar configuración TLP actual;
- definir formato exacto del manifiesto de backup;
- definir formato del registro de propiedad de archivos;
- definir primer esquema `config_version=1`.

## Regla final

> Alpha 0.1 no tiene que verse diferente; tiene que demostrar que SDE puede modificar el sistema sin dejarlo atrapado.
