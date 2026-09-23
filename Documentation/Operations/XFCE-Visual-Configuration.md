# SineOS — Configuración visual reproducible de XFCE

Esta carpeta contiene la configuración visual reproducible de **SineOS** para Debian con XFCE.

El objetivo no es convertir Debian en otro sistema operativo, sino conservar una instalación estable y predecible de Debian y aplicar una capa visual moderna, ligera y recuperable sobre XFCE.

La propuesta visual toma como referencia la organización de macOS:

- **Barra superior fija y translúcida**
  - menú principal;
  - menú global de la aplicación activa cuando la aplicación lo soporta;
  - bandeja e indicadores del sistema;
  - volumen, batería, fecha/hora y acciones de sesión.
- **Dock inferior**
  - accesos y aplicaciones abiertas agrupados por icono cuando Docklike está disponible;
  - tamaño compacto;
  - fondo translúcido;
  - autoocultación;
  - aparece al llevar el cursor al borde inferior.
- **Tema general**
  - Arc-Dark;
  - Papirus-Dark;
  - Noto Sans;
  - JetBrains Mono;
  - cursores Breeze;
  - compositor XFWM con sombras suaves;
  - wallpaper propio generado por el instalador.

---

## Archivos

```text
configuracion visual/
├── README.md
└── sineos-xfce-macos.sh
```

### `sineos-xfce-macos.sh`

Instalador y configurador reproducible.

Puede utilizarse tanto sobre una sesión XFCE existente como desde una instalación mínima de Debian.

---

# Filosofía de SineOS

Esta configuración sigue los principios que se han mantenido durante el desarrollo de SineOS:

1. **Debian primero.**
   Se priorizan paquetes disponibles en los repositorios oficiales de Debian.

2. **Sin Snap ni Flatpak como requisito.**
   La configuración no depende de ninguno de los dos.

3. **Sin repositorios externos innecesarios.**
   El instalador no agrega PPAs, repositorios de Ubuntu ni binarios descargados arbitrariamente.

4. **Estabilidad antes que minimalismo.**
   No se eliminan componentes funcionales únicamente para ahorrar unos cuantos paquetes o megabytes.

5. **Cambios visuales separados de los componentes críticos del sistema.**
   El script no modifica:
   - kernel;
   - GRUB;
   - EFI;
   - Secure Boot;
   - firmware;
   - configuración de NetworkManager;
   - conexiones VPN;
   - TLP;
   - suspensión o hibernación;
   - controladores gráficos;
   - configuración de audio existente.

6. **Respaldo antes de modificar XFCE.**
   Antes de aplicar cambios se conserva la configuración previa del usuario.

7. **Recuperación sencilla.**
   La configuración puede restaurarse con el comando `restore`.

8. **Cambios mediante XFConf.**
   Siempre que es posible, la configuración se aplica a XFCE en vivo.

9. **No reiniciar `xfce4-panel` durante una aplicación normal.**
   Durante las pruebas de SineOS se comprobó que `xfce4-panel --restart` puede cerrar el panel sin conseguir iniciarlo nuevamente en algunas sesiones. La versión actual evita ese comportamiento.

---

# Plataforma objetivo

Configuración principal:

```text
Sistema: Debian GNU/Linux
Escritorio: XFCE
Gestor de sesión: LightDM
Sesión: X11
```

La referencia principal del proyecto es **Debian 13 (Trixie)**.

El instalador comprueba dinámicamente qué paquetes están disponibles en la versión de Debian utilizada.

## Compatibilidad del Dock

Cuando `xfce4-docklike-plugin` está disponible, se utiliza como Dock principal.

Si el paquete no está disponible en los repositorios configurados, el script utiliza la lista de ventanas de XFCE como mecanismo de compatibilidad.

No descarga ni compila Docklike desde fuentes externas automáticamente.

## Compatibilidad del menú global

Cuando están disponibles, el instalador utiliza:

```text
xfce4-appmenu-plugin
appmenu-registrar
appmenu-gtk3-module
appmenu-gtk2-module
```

No todas las aplicaciones Linux exportan un menú global compatible.

Por ejemplo, algunas aplicaciones GTK4, Electron o aplicaciones que implementan sus propios menús pueden no mostrar `Archivo`, `Editar`, `Ver`, etc. en el panel superior.

Esto no indica un fallo de XFCE ni del instalador.

---

# Dependencias

El script instala automáticamente los paquetes disponibles que necesita.

Entre ellos se encuentran:

```text
task-xfce-desktop
lightdm
xfce4-goodies
xfce4-whiskermenu-plugin
xfce4-notifyd
xfce4-power-manager
xfce4-pulseaudio-plugin

network-manager-applet
nm-connection-editor

blueman
bluez
pavucontrol

mate-polkit
light-locker

arc-theme
papirus-icon-theme
fonts-noto-core / fonts-noto
fonts-jetbrains-mono
breeze-cursor-theme

xdg-user-dirs
dbus-x11
libnotify-bin
```

Dependiendo de la versión de Debian, también puede instalar:

```text
xfce4-appmenu-plugin
appmenu-registrar
appmenu-gtk3-module
appmenu-gtk2-module
xfce4-docklike-plugin
```

Todos los paquetes se comprueban antes de intentar su instalación.

---

# Instalación rápida

## Opción A — Debian ya tiene XFCE

Entrar a la carpeta:

```bash
cd "configuracion visual"
```

Dar permisos:

```bash
chmod +x sineos-xfce-macos.sh
```

Ejecutar:

```bash
./Scripts/Desktop/sineos-xfce-macos.sh install
```

El script pedirá privilegios administrativos únicamente cuando APT los necesite.

**No es necesario ejecutar todo el script con `sudo`.**

---

# Instalación desde una Debian mínima

En una instalación limpia sin XFCE:

```bash
cd "configuracion visual"
chmod +x sineos-xfce-macos.sh
./Scripts/Desktop/sineos-xfce-macos.sh install
```

El instalador:

1. detecta Debian;
2. actualiza los índices APT;
3. instala XFCE;
4. instala LightDM;
5. instala los paquetes visuales;
6. configura el arranque gráfico;
7. copia el instalador a:

```text
~/.local/bin/sineos-xfce-macos
```

8. programa una ejecución de primer inicio de sesión en:

```text
~/.config/autostart/sineos-xfce-first-login.desktop
```

Al no existir todavía una sesión XFCE/D-Bus activa, el diseño no se fuerza desde la terminal.

Después:

```bash
sudo reboot
```

Al iniciar sesión en XFCE, la personalización se aplica una sola vez.

---

# Instalación cuando no existe `sudo`

Algunas instalaciones mínimas de Debian no agregan automáticamente al usuario al grupo `sudo`.

En ese caso puede instalarse la parte del sistema como root:

```bash
su -
```

y ejecutar:

```bash
./Scripts/Desktop/sineos-xfce-macos.sh packages
```

Después se debe cerrar la sesión de root, entrar en XFCE como el usuario normal y ejecutar:

```bash
./Scripts/Desktop/sineos-xfce-macos.sh apply
```

La personalización del escritorio **siempre debe ejecutarse como el usuario normal**.

---

# Comandos

## Instalación completa

```bash
./Scripts/Desktop/sineos-xfce-macos.sh install
```

Instala dependencias y aplica el diseño.

Si todavía no existe una sesión gráfica activa, programa el diseño para el primer inicio de sesión.

---

## Instalar solamente paquetes

```bash
./Scripts/Desktop/sineos-xfce-macos.sh packages
```

No aplica la personalización.

---

## Aplicar o actualizar el diseño

```bash
./Scripts/Desktop/sineos-xfce-macos.sh apply
```

Debe ejecutarse:

- como usuario normal;
- dentro de una sesión XFCE activa;
- sin `sudo`.

---

## Consultar estado

```bash
./Scripts/Desktop/sineos-xfce-macos.sh status
```

Muestra, entre otros datos:

- Debian detectado;
- presencia de XFCE;
- Arc-Dark;
- Papirus;
- AppMenu;
- Docklike;
- estado del layout;
- posiciones de los paneles;
- autoocultación del Dock.

---

## Restaurar

```bash
./Scripts/Desktop/sineos-xfce-macos.sh restore
```

Restaura el último respaldo generado antes de aplicar cambios.

---

# Diseño de los paneles

## Panel superior

El instalador crea un panel superior:

```text
posición: superior
longitud: 100 %
altura: 30 px
autoocultación: desactivada
fondo: oscuro translúcido
```

Su organización lógica es:

```text
[ Whisker ] [ AppMenu ] [ espacio flexible ] [ estado ] [ volumen ] [ batería ] [ reloj ] [ acciones ]
```

AppMenu solamente aparece si el paquete correspondiente está disponible.

---

# Dock inferior

El Dock se configura aproximadamente como:

```text
posición: inferior
altura: 56 px
iconos: 42 px
longitud: ajustada al contenido
fondo: oscuro translúcido
autoocultación: siempre
```

Comportamiento:

- se oculta cuando deja de utilizarse;
- aparece al llevar el cursor al borde inferior;
- no resta espacio permanente a las aplicaciones maximizadas;
- permanece visible brevemente después de retirar el cursor para evitar parpadeos.

Valores visuales aproximados:

```text
aparición: ~120 ms
ocultación: ~1800 ms
```

---

# Tipografía

Configuración principal:

```text
Interfaz: Noto Sans 10
Títulos: Noto Sans SemiBold 10
Monoespaciada: JetBrains Mono 10
```

Se activa:

```text
antialiasing
hinting ligero
subpixel RGB
```

El objetivo es conseguir una interfaz clara y legible sin aumentar innecesariamente el tamaño del escritorio.

---

# Tema e iconos

```text
Tema GTK/XFWM: Arc-Dark
Iconos: Papirus-Dark
Cursor: Breeze
```

El instalador verifica que los temas existan antes de seleccionarlos.

---

# Wallpaper

El script genera localmente:

```text
~/Imágenes/Wallpapers/sineos-macos-dark.svg
```

o la ruta equivalente devuelta por `xdg-user-dir`.

No descarga fondos externos.

---

# Respaldo

Los respaldos se almacenan en:

```text
~/.local/state/sineos-xfce-macos/backups/
```

El respaldo incluye la configuración existente de XFCE y el CSS GTK previo.

El último respaldo utilizado queda registrado en:

```text
~/.local/state/sineos-xfce-macos/last-backup
```

---

# Idempotencia

Después de aplicar por primera vez el layout, el script crea:

```text
~/.local/state/sineos-xfce-macos/layout-applied
```

Si posteriormente se ejecuta:

```bash
./Scripts/Desktop/sineos-xfce-macos.sh apply
```

el script no reconstruye nuevamente la lista completa de plugins.

Solamente reafirma los parámetros visuales y el comportamiento esperado.

Esto reduce el riesgo de alterar una configuración ya funcional.

---

# Seguridad y alcance

Este script **no es una herramienta de optimización del sistema**.

No debe utilizarse para eliminar paquetes ni para sustituir componentes internos de Debian.

No realiza cambios en:

```text
/etc/default/grub
/boot
/boot/efi
Secure Boot
TPM
firmware
kernel
drivers
NetworkManager connections
VPN
TLP
suspensión
hibernación
PulseAudio/PipeWire
```

Su alcance termina en:

- instalación del entorno XFCE y componentes gráficos necesarios;
- configuración visual del usuario;
- estructura de los paneles;
- tema, iconos, cursor y fuentes;
- wallpaper;
- autoocultación del Dock.

---

# Solución de problemas

## Los paneles no aparecen

Primero comprobar:

```bash
pgrep -a xfce4-panel
```

Si no está ejecutándose:

```bash
nohup xfce4-panel >/tmp/xfce4-panel.log 2>&1 &
```

Después revisar:

```bash
cat /tmp/xfce4-panel.log
```

La configuración normal no utiliza `xfce4-panel --restart`.

---

## El Dock no se oculta

Consultar:

```bash
xfconf-query \
  -c xfce4-panel \
  -p /panels/panel-2/autohide-behavior
```

El valor esperado en el layout estándar de SineOS es:

```text
2
```

Para establecerlo manualmente:

```bash
xfconf-query \
  -c xfce4-panel \
  -p /panels/panel-2/autohide-behavior \
  -s 2
```

No es necesario reiniciar el panel.

---

## El Dock desaparece pero no vuelve

Mover el cursor completamente hasta el borde inferior.

El área sensible de autoocultación se mantiene deliberadamente pequeña.

Si todavía existe un problema:

```bash
./Scripts/Desktop/sineos-xfce-macos.sh restore
```

---

## El menú global no aparece para una aplicación

Comprobar:

```bash
dpkg -l | grep appmenu
```

Aunque los paquetes estén instalados, no todas las aplicaciones implementan un menú exportable.

Esto puede ser normal.

---

## Quiero volver a mi escritorio anterior

Ejecutar:

```bash
./Scripts/Desktop/sineos-xfce-macos.sh restore
```

La restauración evita `xfce4-panel --restart`.

Cuando necesita recuperar una configuración completa:

1. detiene el panel;
2. recupera el respaldo;
3. reinicia `xfconfd`;
4. inicia explícitamente `xfce4-panel`;
5. comprueba que el proceso se haya levantado.

---

# Validación del script

Antes de publicarlo se puede validar la sintaxis:

```bash
bash -n sineos-xfce-macos.sh
```

Debe finalizar sin mostrar errores.

Para consultar el estado después de instalar:

```bash
./Scripts/Desktop/sineos-xfce-macos.sh status
```

---

# Integración con el repositorio SineOS

La carpeta debe ubicarse en la raíz del repositorio:

```text
SineOS/
├── Ansible/
├── Archive/
├── Containers/
├── Documentation/
├── Foundation/
├── Infrastructure/
├── Lab/
├── Platform/
├── Scripts/
├── Terraform/
└── configuracion visual/
    ├── README.md
    └── sineos-xfce-macos.sh
```

Desde el repositorio local:

```bash
cd ~/Workspace/SineOS
```

Crear la carpeta si todavía no existe:

```bash
mkdir -p "configuracion visual"
```

Copiar los archivos y validar:

```bash
chmod +x "Scripts/Desktop/sineos-xfce-macos.sh"
bash -n "Scripts/Desktop/sineos-xfce-macos.sh"
```

Revisar:

```bash
git status
git diff --check
```

Preparar commit:

```bash
git add "configuracion visual"
```

Commit sugerido:

```bash
git commit -m "feat(xfce): add reproducible visual configuration"
```

Subir a `main`:

```bash
git push origin main
```

---

# Mantenimiento

Cuando se modifique el instalador:

1. validar con `bash -n`;
2. probar `status`;
3. probar `install` o `apply` en una sesión de prueba;
4. comprobar el panel superior;
5. comprobar autoocultación del Dock;
6. comprobar `restore`;
7. revisar `git diff`;
8. documentar cualquier cambio relevante;
9. hacer commit;
10. subir a GitHub.

No debe publicarse una versión que dependa de un estado local no documentado.

---

# Estado actual

Versión del instalador:

```text
4.0.0
```

Objetivo principal:

```text
Debian 13 (Trixie) + XFCE
```

Estado:

```text
reproducible
con respaldo
restaurable
sin repositorios externos obligatorios
sin Snap/Flatpak
orientado a laptop y escritorio
```

---

## SineOS

Esta configuración forma parte del proyecto SineOS y sigue su enfoque de mantener una base Debian limpia, reproducible y documentada, separando la infraestructura y los servicios de la personalización del entorno de usuario.