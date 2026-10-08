# SineOS Desktop Experience (SDE)

**Decisión congelada:** 07-10-2026  
**Estado:** Plan congelado / pendiente de implementación  
**Issue maestro:** https://github.com/ArgenisPadill/SineOS/issues/1  
**Plataforma objetivo:** Debian 13 (Trixie) + XFCE 4.20 + X11 + LightDM

## Propósito

SineOS Desktop Experience (SDE) es la evolución planificada de la capa visual y de interacción de SineOS.

SineOS es un sistema de propósito general. SDE no debe diseñarse alrededor de un oficio, entorno académico o perfil de usuario específico; sus funciones deben ser útiles y comprensibles en escenarios cotidianos de trabajo, aprendizaje, creación, administración y exploración de Linux.

Su objetivo es llevar XFCE al máximo nivel razonable de pulido visual, ergonomía y coherencia sin sustituirlo por otro escritorio y sin sacrificar las razones por las que XFCE fue elegido: bajo consumo, estabilidad, control, simplicidad operativa y facilidad de recuperación.

SDE no pretende imitar otro escritorio. Toma buenas ideas de interfaces modernas —global menu, dock, blur, microanimaciones, OSD, launcher, control de pantallas, consistencia visual— y las integra de forma compatible con XFCE.

## Principios congelados

1. **XFCE sigue siendo el escritorio.**
   SDE no sustituye XFCE por GNOME Shell, KDE Plasma, KWin, Hyprland, Wayfire, Compiz u otro escritorio.

2. **Debian primero.**
   Se priorizan paquetes oficiales de Debian 13 y proyectos upstream activos.

3. **Bajo consumo.**
   Instalar una herramienta no implica mantenerla residente. Captura, grabación, anotación, localizador de cursor, pantalla inalámbrica y otras funciones se cargan bajo demanda.

4. **Sin puntos únicos de fallo visuales.**
   Un fallo de Picom, Rofi, Docklike, AppMenu o una herramienta auxiliar no debe impedir usar XFCE.

5. **Replicabilidad.**
   La experiencia debe poder reconstruirse en otra instalación limpia sin depender de cambios manuales olvidados.

6. **Escalabilidad.**
   El diseño debe adaptarse a distintas resoluciones y DPI sin mantener configuraciones independientes por máquina.

7. **Recuperabilidad.**
   Todo cambio relevante requiere backup, rollback y una ruta clara para volver a XFCE funcional.

8. **Compatibilidad antes que efectos.**
   Ningún efecto visual justifica romper aplicaciones, proyectores, suspensión, hardware o el flujo normal del usuario.

9. **Sin telemetría por defecto.**
   Logs y diagnóstico permanecen locales.

10. **Configuración explícita y versionada.**
    El estado visual debe poder describirse, migrarse y auditarse.

---

# Arquitectura

SDE se divide en tres capas.

## 1. Núcleo de escritorio SineOS

Responsable de que el escritorio sea utilizable incluso si las capas visuales opcionales fallan.

Base prevista:

- Debian 13;
- XFCE 4.20;
- X11;
- LightDM;
- XFWM4;
- xfce4-panel;
- xfce4-settings;
- xfce4-notifyd;
- Clipman;
- Thunar;
- Whisker como fallback.

No debe depender de GNOME Shell, Plasma o un segundo window manager.

## 2. Capa visual SineOS

Responsable de la identidad visual.

Incluye:

- Picom como compositor externo;
- Docklike;
- Genmon;
- Colloid como base de tema/iconografía;
- Inter para interfaz;
- JetBrains Mono para terminal y código;
- cursor SineOS propio;
- wallpaper SineOS;
- decoración XFWM propia;
- CSS GTK;
- integración visual Qt;
- menús contextuales;
- tooltips;
- OSD;
- pantalla de bloqueo;
- microanimaciones;
- estados activo/inactivo;
- sistema de tokens visuales.

## 3. Herramientas SineOS

Funciones auxiliares que se ejecutan bajo demanda:

- Rofi;
- Flameshot;
- vokoscreenNG;
- Gromit-MPX;
- localizador de cursor;
- OBS opcional;
- SineOS Display;
- módulo opcional de pantalla inalámbrica.

Estas herramientas no forman parte del camino crítico de arranque del escritorio.

---

# Barra superior

Se mantiene el concepto de barra superior fija.

Organización conceptual:

```text
[ SineOS ] [ Aplicación activa ] [ Global Menu ] [ espacio ]
[ workspaces ] [ estado ] [ red ] [ audio ] [ batería ] [ hora ]
```

## Global Menu

Se conserva `xfce4-appmenu-plugin`.

Comportamiento:

- cuando una aplicación exporta un menú compatible, el menú aparece en el panel superior;
- cuando no es compatible, su menú permanece dentro de la aplicación;
- nunca se fuerza una integración que pueda dejar una aplicación sin menú;
- GTK4, Electron, Chromium, Firefox y Qt moderno pueden requerir fallback.

La compatibilidad funcional tiene prioridad sobre la uniformidad estética.

---

# Dock

El dock inferior seguirá basado en XFCE mediante Docklike.

Características previstas:

- autohide;
- iconos consistentes;
- fondo translúcido;
- blur selectivo;
- hover discreto;
- dimensiones adaptativas;
- estructura recuperable mediante xfce4-panel.

Si Docklike no está disponible o falla, XFCE debe conservar una lista de ventanas usable.

---

# Composición y efectos

## Picom

Picom será el único compositor externo cuando esté activo.

XFWM conserva el rol de window manager.

SDE utilizará Picom para:

- VSync;
- sombras;
- transparencia;
- blur selectivo;
- fade;
- esquinas;
- transiciones cortas.

## Reglas de rendimiento

No aplicar blur donde no puede verse.

Ejemplos:

```text
Panel               blur
Rofi                blur
Dock                blur
Menús               blur
Notificaciones      blur

Thunar opaco        sin blur de fondo
Chromium opaco      sin blur de fondo
LibreOffice opaco   sin blur de fondo
Vídeo fullscreen    sin blur
OBS                  sin blur
```

Las animaciones de geometría/movimiento que sigan siendo experimentales no forman parte obligatoria de SDE 1.0.

## Lenguaje de movimiento

La interfaz debe utilizar una gramática coherente:

- abrir -> fade + scale discreto;
- cerrar -> fade;
- menús -> fade rápido;
- notificaciones -> slide + fade;
- launcher -> scale/fade;
- Super+P -> transición corta;
- dock hover -> lift mínimo.

Las animaciones nunca deben retrasar la interacción.

---

# Apariencia

## Dirección

Visual general:

- oscuro;
- profesional;
- azul/cian;
- cristal selectivo;
- contraste alto;
- sin estética gamer/neón excesiva;
- superficies claramente diferenciadas.

Paleta base prevista:

```text
background       #090E14
surface          #101822
surface-raised   #182331
border           #273444

text-primary     #E6EDF5
text-secondary   #8B9AAC

accent           #3B82F6
accent-cyan      #22C7E8
success          #34C759
warning          #F5A524
error            #F04444
```

## Tokens

La implementación final no debe repetir valores arbitrarios por múltiples archivos.

Debe existir una definición central para:

- colores;
- radios;
- sombras;
- spacing;
- opacidades;
- duraciones;
- escala;
- tipografía.

Ejemplos conceptuales:

```text
radius-small
radius-medium
radius-large

spacing-xs
spacing-sm
spacing-md
spacing-lg

shadow-low
shadow-medium
shadow-high

animation-fast
animation-normal
animation-slow
```

---

# Tipografía

UI prevista:

- Inter Regular/Medium;
- Inter SemiBold para títulos;
- JetBrains Mono para terminal y código;
- Noto Sans como fallback amplio.

Debe configurarse:

- antialiasing;
- hinting;
- subpixel cuando aplique;
- DPI;
- escala según pantalla.

La nitidez en monitor externo/proyector es un criterio funcional, no solo estético.

---

# GTK y Qt

SDE debe evitar que las aplicaciones Qt parezcan pertenecer a otro escritorio.

Se planifica configurar Qt sin instalar Plasma como escritorio.

Objetivos:

- tipografía consistente;
- iconografía consistente;
- densidad similar;
- paleta coherente;
- buen contraste;
- no depender de KDE Plasma para ejecutar Qt.

Las diferencias inevitables entre toolkits se aceptan cuando forzar uniformidad implique riesgo.

---

# Cursor

SDE tendrá un cursor propio basado en el formato estándar XCursor.

Objetivos:

- alta legibilidad;
- tamaños 24/32/48 px o equivalentes;
- contraste en fondos claros/oscuros;
- usable en proyectores;
- identidad propia;
- cero daemon adicional.

Debe cubrir al menos:

- default;
- pointer;
- text;
- wait;
- progress;
- move;
- resize;
- drag;
- forbidden;
- help.

El localizador de cursor será una herramienta separada y bajo demanda.

---

# OSD

SDE debe unificar los indicadores visuales de:

- volumen;
- mute;
- micrófono;
- brillo;
- Caps Lock;
- cambios de pantalla;
- conexión/desconexión relevante.

Los OSD deben ser cortos, legibles y coherentes con el resto de la interfaz.

---

# Login y bloqueo

LightDM se mantiene.

La pantalla de bloqueo debe utilizar mecanismos normales de autenticación y no introducir un sistema de seguridad independiente.

Objetivo visual:

```text
LightDM
  ->
SineOS Desktop
  ->
Pantalla de bloqueo
```

sin saltos de identidad visual.

---

# Thunar

Thunar se mantiene como file manager.

Áreas a pulir:

- sidebar;
- miniaturas;
- carpetas;
- estados hover/selected;
- dispositivos;
- barra de ubicación;
- separadores;
- iconografía;
- espaciado.

No se sustituirá Thunar únicamente por estética.

---

# Captura, grabación y presentación

## Captura

Principal prevista:
- Flameshot.

Fallback:
- xfce4-screenshooter.

## Grabación

Estándar:
- vokoscreenNG.

Avanzado:
- OBS opcional.

Se estudiará codificación por hardware cuando la GPU lo permita.

## Anotación

- Gromit-MPX.

## Cursor

- localizador activado solo cuando se necesite.

Ninguna de estas herramientas debe iniciar permanentemente con la sesión salvo que exista una razón validada.

---

# Pantallas

## Super + P

Debe existir una única interfaz SineOS con exactamente cuatro opciones:

1. Duplicar
2. Extender
3. Solo esta pantalla
4. Pantalla inalámbrica

Navegación:

- Super+P abre;
- flechas seleccionan;
- Enter aplica;
- Esc cancela;
- mouse funciona.

## Duplicar

Debe:

- buscar la mejor resolución exacta común;
- preservar relación de aspecto;
- evitar escalado fraccional cuando sea posible;
- priorizar nitidez;
- preferir refresh rate estable.

## Extender

Debe:

- usar resolución nativa de cada salida cuando sea viable;
- mantener disposición consistente;
- recuperar ventanas fuera de pantalla.

## Solo esta pantalla

Significa:

- mantener pantalla interna/principal;
- apagar temporalmente salidas externas.

No significa «solo segunda pantalla».

## Pantalla inalámbrica

Será un módulo opcional.

La falla del backend inalámbrico nunca debe afectar HDMI o el escritorio.

La selección final de backend queda pendiente de validación.

---

# Privacidad en pantallas externas

SDE debe poder reducir la exposición accidental de información sensible cuando exista una pantalla externa, independientemente del contexto de uso.

Objetivo:

- evitar mostrar contenido detallado de notificaciones sensibles en una salida proyectada;
- no alterar permanentemente la configuración del escritorio;
- preservar el acceso normal a las notificaciones en la pantalla principal cuando sea técnicamente viable.

---

# Resolución y DPI

SDE no debe asumir 1920x1080.

Debe adaptarse a:

- 1366x768;
- 1600x900;
- 1920x1080;
- 1920x1200;
- 2560x1440;
- 4K/HiDPI.

Elementos adaptables:

- panel;
- dock;
- tipografía;
- cursor;
- Rofi;
- padding;
- radios;
- iconos;
- notificaciones.

El cálculo se realizará al iniciar sesión o cuando cambie la configuración de pantallas; no requiere un daemon pesado permanente.

Se documentarán explícitamente las limitaciones de DPI mixto bajo X11.

---

# Mouse y touchpad

Se mantiene libinput.

Objetivos:

- sensibilidad moderada;
- aceleración adaptable;
- movimiento coherente entre monitores;
- opciones de tap/natural scrolling mediante XFCE/libinput;
- cursor visible y consistente.

No se añadirá una capa gestual pesada al baseline sin necesidad demostrada.

---

# Personalización

El usuario podrá cambiar:

- wallpaper;
- color de acento;
- claro/oscuro;
- blur;
- transparencia;
- animaciones;
- Reduced Motion;
- tamaño de texto;
- cursor;
- tamaño del dock;
- comportamiento de autohide;
- número de workspaces;
- hora;
- indicadores;
- atajos.

## Presets

### Ligero

- sombras;
- fade;
- blur mínimo;
- transparencias ligeras;
- animaciones básicas.

### Equilibrado

Preset por defecto.

- sombras;
- blur;
- transparencia;
- fade;
- scale;
- microanimaciones.

### Máximo visual

- mayor blur;
- sombras profundas;
- transparencias;
- efectos avanzados certificados.

Los presets ajustan intensidad, no cambian de escritorio.

---

# Accesibilidad

Debe planificarse desde el inicio:

- Reduced Motion;
- alto contraste;
- texto grande;
- cursor grande;
- indicadores grandes;
- duración extendida de notificaciones;
- navegación por teclado.

---

# Atajos

Mapa previsto:

```text
Super                 Launcher
Super + P             Pantallas
Super + L             Bloquear
Super + V             Portapapeles
Super + E             Thunar
Super + Enter         Terminal
Super + Shift + S     Captura
Super + Shift + R     Grabación

Super + Left          Snap izquierda
Super + Right         Snap derecha
Super + Up            Maximizar
Super + Down          Restaurar/minimizar
```

SDE aplica su mapa de atajos desde una base limpia. Los atajos anteriores se conservan en el respaldo pre-SDE; se preservan teclas de hardware y multimedia que no entren en conflicto.

---

# Configuración

Fuente de verdad prevista:

```text
~/.config/sineos-desktop/
├── appearance.conf
├── shortcuts.conf
├── accessibility.conf
├── version
└── hardware/
    ├── display.conf
    └── gpu.conf
```

## Portable vs local

Portable:

- apariencia;
- atajos;
- accesibilidad;
- preferencias SineOS.

Local:

- monitor;
- GPU;
- outputs;
- seriales;
- ajustes dependientes de hardware.

Un export nunca debe trasladar MAC, credenciales, redes Wi-Fi, seriales ni secretos.

---

# Configuración generada

Los archivos controlados por SDE deben indicar claramente su origen.

Ejemplo:

```text
# GENERATED BY SINEOS DESKTOP EXPERIENCE
# Do not edit directly.
```

Las plantillas deberán existir bajo una ruta controlada por el proyecto y los valores reales vivir en la configuración SDE.

---

# CLI futura

La interfaz gráfica no debe ser la única forma de reproducir el estado.

Interfaz conceptual:

```bash
sineos-desktop config get appearance.blur
sineos-desktop config set appearance.blur true
sineos-desktop config set appearance.accent blue
```

También se prevén:

- status;
- health;
- safe-mode;
- repair;
- reset;
- export;
- import;
- uninstall.

La sintaxis final se definirá durante implementación.

---

# Backup, rollback y uninstall

Antes de modificar XFCE debe existir backup.

SDE debe permitir:

- reset de apariencia;
- reset de panel;
- reset de dock;
- reset de display;
- reset de shortcuts;
- reset completo;
- restore de estado anterior;
- uninstall sin borrar datos ajenos.

No debe reemplazarse indiscriminadamente todo `~/.config/xfce4`.

---

# Degradación elegante

Contrato obligatorio:

```text
Picom falla
-> compositor XFWM

Global Menu incompatible
-> menú interno

Docklike falla
-> panel XFCE funcional

Rofi falla
-> Whisker

Flameshot falla
-> xfce4-screenshooter

Pantalla inalámbrica falla
-> HDMI/XRandR siguen funcionando

Tema SineOS falla
-> tema fallback conocido
```

Ninguna mejora visual debe ser un punto único de falla.

---

# Rendimiento

La razón original para usar XFCE sigue vigente.

Objetivos iniciales de ingeniería sobre baseline real:

```text
RAM adicional idle:        objetivo <= 150 MB
CPU adicional idle:        objetivo ~0–1 %
procesos residentes extra: objetivo <= 2–3
grabadores residentes:     0
servicios duplicados:      0
escrituras continuas:      0
```

Estos valores son objetivos y deberán validarse con mediciones reales antes de cerrar SDE 1.0.

## Genmon

No crear múltiples scripts ejecutándose cada segundo.

Preferencia:

- un estado agrupado;
- métricas rápidas cada 3–5 s;
- métricas lentas cada 30–60 s;
- tareas caras solo bajo demanda.

---

# Dependencias

Política prevista:

1. Debian Stable.
2. Backports cuando exista justificación.
3. Paquete .deb mantenido por SineOS desde release upstream fijo.
4. No instalar desde `main/master` en producción.
5. No usar PPAs de Ubuntu.
6. No ejecutar instaladores remotos opacos.
7. Registrar versión, fuente, checksum y rollback de dependencias externas.

Las dependencias críticas deben ser pocas.

---

# Versionado y migraciones

La configuración tendrá versión de esquema.

Ejemplo:

```text
config_version=1
```

Las migraciones deben ser:

- explícitas;
- idempotentes;
- reversibles cuando sea viable;
- respaldadas antes de aplicar;
- documentadas.

---

# Logs y diagnóstico

Ruta prevista:

```text
~/.local/state/sineos-desktop/
```

Debe contener solo información necesaria para operación y troubleshooting.

Se prevé:

- logs pequeños;
- rotación;
- health report local;
- ausencia de telemetría automática.

---

# Seguridad y límites de alcance

SDE no debe modificar infraestructura crítica **por razones puramente visuales**. Las integraciones operativas aprobadas para energía, red, VPN, drivers, hibernación, actualizaciones y recuperación se rigen por sus documentos específicos y siempre requieren validación, rollback y límites claros.

No modificar por motivos visuales:

- kernel;
- GRUB;
- EFI;
- Secure Boot;
- TPM;
- firmware;
- drivers;
- VPN;
- conexiones de NetworkManager;
- TLP;
- hibernación;
- servicios Podman;
- PostgreSQL;
- política de backup;
- firewall;
- infraestructura crítica.

Debe respetar la separación existente entre escritorio e infraestructura.

---

# Multiusuario

Paquetes y assets pueden instalarse globalmente.

Preferencias visuales y configuración SDE son por usuario.

Una instalación de SDE no debe sobrescribir la configuración visual de otros usuarios sin intervención explícita.

---

# Internacionalización

La interfaz SDE debe diseñarse al menos para:

- es_MX;
- en.

Los textos no deben quedar hardcodeados de forma que impida localización futura.

---

# Futuro Wayland

SDE 1.x tiene X11 como plataforma estable objetivo.

La arquitectura debe separar:

- lógica de negocio;
- UI;
- backend de displays;
- compositor.

Esto permitirá reemplazar en el futuro:

- XRandR;
- Picom;
- integraciones X11;

sin rediseñar todo SDE cuando XFCE/Wayland alcance la madurez requerida.

---

# Especificaciones operativas consolidadas

Forman parte obligatoria de la planeación congelada de SDE:

- `SDE-System-Integration.md`
- `SDE-Devices-Printing-Scanning.md`
- `SDE-Privacy-Permissions-Remote-Access.md`
- `SDE-Hardware-Health.md`
- `SDE-Updates-Migration.md`
- `SDE-Implementation-Roadmap.md`
- `SDE-Definition-of-Done-1.0.md`
- `SDE-Advanced-Settings-Policy.md`
- `SDE-Alpha-0.1-Technical-Manifest.md`
- `SDE-Alpha-0.1-Backup-Restore-Spec.md`
- `SDE-Alpha-0.1-Ownership-Conflict-Spec.md`

En caso de conflicto entre una regla general antigua y una decisión específica más reciente de estos documentos, prevalece la especificación específica más reciente.

---

# Criterios de aceptación de SDE 1.0

## Arranque y recuperación

Debe validarse:

- login;
- logout;
- reboot;
- hibernación;
- reanudación;
- fallo de Picom;
- fallo/reinicio de panel;
- tema ausente;
- restore a XFCE funcional.

## Pantallas

Debe validarse:

- pantalla interna;
- HDMI;
- hot-plug;
- Duplicar;
- Extender;
- Solo esta pantalla;
- pantalla inalámbrica cuando exista backend certificado (no bloqueante para SDE 1.0);
- cambio de resolución;
- recuperación de ventanas;
- DPI mixto.

## Aplicaciones

Debe probarse:

- GTK/XFCE;
- GTK4;
- Qt5;
- Qt6;
- Electron;
- Chromium/Firefox;
- Global Menu compatible;
- Global Menu incompatible.

## Rendimiento

Debe medirse:

- RAM idle;
- CPU idle;
- uso GPU;
- blur;
- multimonitor;
- grabación;
- proyección;
- tiempo de login.

## Replicabilidad

Debe validarse:

- Debian 13 limpio;
- segunda ejecución del instalador;
- upgrade;
- rollback;
- uninstall;
- restore;
- usuario adicional.

---


# Ampliación congelada: materiales, vista general, ajuste de ventanas y lenguaje de movimiento

**Decisión congelada:** 07-10-2026

Esta ampliación surge de comparar patrones visuales y de interacción de GNOME, KDE Plasma, COSMIC, elementary/Pantheon, Cinnamon, compositores modernos como Hyprland, Windows 11 y macOS.

El objetivo no es copiar otro escritorio ni incorporar sus dependencias. SDE adopta ideas de interacción que puedan implementarse de forma compatible con XFCE/X11, manteniendo bajo consumo, degradación elegante y recuperación.

## Materiales SineOS

SDE formaliza tres tipos de superficie:

### Surface

Para ventanas y superficies de trabajo normales.

Objetivos:
- alta legibilidad;
- fondo prácticamente opaco;
- costo gráfico mínimo;
- no aplicar blur cuando el contenido de fondo no es visible.

### Frost

Para superficies transitorias y de navegación:
- panel;
- dock;
- Rofi;
- notificaciones;
- menús;
- popovers.

Características:
- transparencia moderada;
- tint SineOS;
- blur selectivo;
- posible textura de ruido extremadamente sutil;
- contraste suficiente para conservar legibilidad.

### Overlay

Para interfaces que requieren elevar el foco:
- Super+P;
- apagado/reinicio;
- confirmaciones;
- recovery;
- diálogos importantes;
- overlays de organización.

Características:
- superficie elevada;
- fondo atenuado;
- blur localizado cuando aporte valor;
- jerarquía visual claramente superior a Surface/Frost.

Los materiales se definirán mediante tokens centrales, no con valores dispersos por aplicación.

## Vista general SineOS

SDE podrá incorporar una vista espacial de ventanas y escritorios en 1.0 únicamente si la implementación elegida supera las pruebas de estabilidad, rendimiento y recuperación. Si no las supera, el Overview completo se difiere a 1.1 y XFWM/Alt+Tab permanece como fallback.

Atajo previsto:

```text
Super + Tab
-> SineOS Overview
```

Objetivos:
- visualizar ventanas abiertas;
- visualizar workspaces;
- seleccionar una ventana con teclado o mouse;
- facilitar orientación cuando existan muchas ventanas;
- mantener una salida inmediata al escritorio normal.

### Candidato técnico

`xfdashboard` es candidato para la implementación inicial.

No entra automáticamente en Desktop Core.

Antes de declararlo dependencia soportada deberá:
- empaquetarse desde una release fija;
- probarse con XFCE 4.20/X11;
- medirse en RAM/CPU;
- verificarse con multimonitor;
- validar recuperación si el proceso falla;
- disponer de fallback.

Fallback obligatorio:
- Alt+Tab/XFWM;
- selector normal de workspaces;
- escritorio completamente utilizable sin Overview.

## Ajuste de ventanas SineOS

SDE añadirá organización visual de ventanas inspirada en los mejores patrones de snapping modernos sin sustituir XFWM.

Atajo previsto:

```text
Super + Z
-> SineOS Snap
```

Layouts previstos según geometría disponible:

Pantallas convencionales:
- 50/50;
- 70/30;
- 30/70;
- cuatro cuadrantes.

Pantallas ultrawide:
- 33/33/33;
- 25/50/25;
- combinaciones equivalentes útiles.

Pantallas pequeñas:
- 50/50;
- maximizada;
- layouts reducidos que no produzcan ventanas inutilizables.

Backend conceptual:
- Rofi para selección visual;
- libwnck para ventanas;
- XRandR para geometría de monitores;
- scripts SineOS sin daemon residente permanente.

Los layouts deben calcularse usando el monitor activo y no coordenadas hardcodeadas.

## Lenguaje de movimiento SineOS

SDE define un lenguaje de movimiento propio. No se añadirán animaciones de forma independiente sin respetar estas reglas.

Duraciones iniciales:

```text
FAST      ~90 ms
STANDARD ~140 ms
EMPHASIS ~180 ms
```

Comportamientos previstos:
- menú -> aparece desde el contexto/origen cuando sea viable;
- notificación -> slide corto desde el borde + fade;
- Rofi -> scale discreto + fade;
- ventana -> entrada sutil, sin rebote;
- cierre -> fade + reducción mínima;
- Super+P -> overlay + transición corta;
- diálogo -> aparece sobre su ventana/contexto;
- Overview -> zoom out;
- salida de Overview -> retorno hacia la ventana seleccionada;
- hover del dock -> elevación mínima, nunca magnificación exagerada.

Reglas:
- ninguna animación debe retrasar la interacción;
- evitar rebotes y elasticidad innecesaria;
- mantener coherencia entre componentes;
- respetar Reduced Motion;
- priorizar frame pacing y estabilidad sobre espectacularidad.

## Animaciones de geometría

Las animaciones de posición/size de Picom no quedan habilitadas por defecto en SDE 1.0 mientras su comportamiento no sea suficientemente estable para el baseline.

Política prevista:

```text
Ligero        -> OFF
Equilibrado   -> OFF
Máximo visual -> opcional/experimental, solo tras validación
```

Mover y redimensionar manualmente una ventana debe seguir siendo inmediato y predecible.

## Enfoque visual SineOS

La ventana activa debe ser identificable sin recurrir a bordes brillantes o estética gamer.

Ventana activa:
- título al 100 %;
- sombra completa;
- borde/acento muy sutil;
- posible tinte azul mínimo en sombra si las pruebas muestran buen resultado.

Ventana inactiva:
- título atenuado;
- borde neutro;
- sombra reducida;
- contenido no debe perder legibilidad.

El efecto debe ser suficientemente discreto para trabajar muchas horas.

## Movimiento reducido global

Reduced Motion es una función de accesibilidad global, no un perfil de bajo rendimiento.

Cuando esté activo:
- scale espacial -> off;
- slide -> off o sustituido por fade corto;
- transiciones de workspaces -> off;
- motion del dock -> off;
- geometry animations -> off;
- fade corto -> permitido.

Todas las herramientas SDE deberán respetar esta preferencia.

## Radios sistémicos

Los radios dejan de ser valores arbitrarios por componente.

Tokens previstos:

```text
radius-sm
radius-md
radius-lg
radius-xl
```

Deben aplicarse coherentemente a:
- ventanas;
- menús;
- Rofi;
- dock;
- panel popups;
- notificaciones;
- OSD;
- Super+P;
- pantalla de bloqueo;
- overlays.

## Smoke / atenuación modal

Los diálogos críticos pueden atenuar temporalmente el contenido que queda detrás para hacer evidente el foco.

Aplicable a:
- apagar;
- reiniciar;
- reset;
- recovery;
- confirmaciones destructivas;
- diálogos críticos de SDE.

Reglas:
- no bloquear innecesariamente;
- transición corta;
- no introducir blur global caro;
- respetar Reduced Motion.

## Cursor: fuente vectorial

El cursor SineOS tendrá un SVG maestro como fuente de diseño.

Pipeline previsto:

```text
SVG maestro
├── 24 px
├── 32 px
├── 48 px
└── 64 px
    -> assets XCursor
```

Ventajas:
- consistencia entre tamaños;
- mejor nitidez;
- fuente reutilizable para un futuro backend Wayland;
- mantenimiento centralizado del diseño.

## Efectos explícitamente fuera del baseline

SDE 1.0 no incorporará por defecto:
- wobbly windows;
- desktop cube;
- fall-apart;
- efectos tipo genie exagerados;
- magnificación agresiva del dock;
- refracción costosa en tiempo real;
- transparencia completa de aplicaciones de trabajo;
- animaciones largas;
- geometría experimental obligatoria;
- glow/neón permanente alrededor de ventanas.

Estos efectos podrán evaluarse en laboratorio, pero no forman parte de la identidad ni de los criterios de aceptación del release.

## Criterios de aceptación adicionales

Antes de considerar terminadas estas funciones deberá validarse:
- Overview con 1 y múltiples monitores;
- Overview ausente/fallando sin afectar XFCE;
- Snap en resoluciones pequeñas, 1080p, 1440p, 4K y ultrawide cuando exista hardware de prueba;
- Snap en monitor interno y externo;
- layouts que nunca coloquen ventanas fuera del área visible;
- Reduced Motion aplicado de forma coherente;
- materiales legibles sobre wallpapers claros/oscuros;
- rendimiento de blur/transparencia medido;
- animaciones sin stutter perceptible bajo carga razonable;
- Focus claramente visible sin glow excesivo;
- overlays accesibles por teclado;
- salida con Esc donde corresponda.


---

# Pendientes de planificación

Antes de comenzar implementación deben cerrarse todavía:

1. **Empaquetado y distribución**
   - estructura de paquetes;
   - qué entra en Core/Visual/Tools;
   - estrategia de `.deb` propios;
   - política de instalación limpia.

2. **Actualizaciones y migraciones**
   - canales;
   - compatibilidad;
   - versiones;
   - rollback entre releases.

3. **Matriz de hardware**
   - Intel;
   - AMD;
   - NVIDIA;
   - laptop/desktop;
   - resoluciones;
   - monitores externos;
   - proyectores;
   - HiDPI;
   - hibernación/reanudación.

4. **Documentación final de 1.0**
   - installation;
   - operation;
   - troubleshooting;
   - recovery;
   - uninstall;
   - manifest;
   - support matrix.

5. **Backend inalámbrico**
   - validar técnicamente candidato final antes de declararlo soportado.

6. **Presupuesto real**
   - medir baseline XFCE real;
   - fijar thresholds definitivos.

---

# Definición de terminado

SDE 1.0 no estará terminado por verse bien.

Debe:

1. mantener XFCE como base funcional;
2. poder instalarse de forma reproducible;
3. ser idempotente;
4. poder actualizarse;
5. poder desinstalarse;
6. restaurar estado previo;
7. sobrevivir fallos de componentes visuales;
8. pasar pruebas de pantalla y suspensión;
9. cumplir presupuesto de recursos;
10. documentar sus dependencias;
11. no introducir dependencias ocultas de otro escritorio;
12. no depender de memoria o conversación para reconstruirse.

## Regla final

> SineOS Desktop Experience debe sentirse como una experiencia propia sin dejar de ser un XFCE ligero, estable, recuperable y reproducible.
