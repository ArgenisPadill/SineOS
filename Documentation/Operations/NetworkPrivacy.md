# SineOS — NetworkPrivacy

## Propósito

NetworkPrivacy es una aplicación GTK3 nativa de SineOS para administrar la política DNS de la conexión Wi-Fi actual sin ejecutar la interfaz como root.

La aplicación vive en:

```text
Apps/NetworkPrivacy/
├── network_policy.py
└── sineos-network-privacy.py
```

La automatización de instalación e integración con XFCE vive en:

```text
Scripts/NetworkPrivacy/install-network-privacy.sh
```

## Modelo de operación

La política diseñada para SineOS es:

```text
Red de confianza -> DNSCrypt por perfil de NetworkManager
Red nueva/pública -> DNS recibido por DHCP inicialmente
VPN Proton activa -> Proton controla DNS y routing
```

DNSCrypt no se impone globalmente. Esto permite que redes públicas y portales cautivos funcionen antes de activar Proton VPN.

## Dependencias

- Python 3
- GTK3 / PyGObject (`python3-gi`, `gir1.2-gtk-3.0`)
- NetworkManager y `nmcli`
- Polkit con agente gráfico de sesión
- `dnscrypt-proxy`
- `dig` para validación DNS
- `getent`
- `notify-send`

La modificación de perfiles de NetworkManager se realiza como usuario normal. NetworkManager/Polkit solicita autenticación solo si la política del sistema lo requiere.

## Estado persistente

Antes de activar DNSCrypt en un perfil, NetworkPrivacy conserva sus valores DNS originales en:

```text
~/.local/state/sineos-network-privacy/profiles.json
```

El directorio utiliza permisos 700 y el archivo 600. Este estado es local y no pertenece al repositorio Git.

La restauración no fuerza DHCP a ciegas: recupera los valores que tenía el perfil antes de ser administrado por SineOS.

## DNSCrypt

Dirección local utilizada:

```text
127.0.2.1:53
```

Al activar la protección, el perfil Wi-Fi recibe:

```text
ipv4.dns = 127.0.2.1
ipv4.ignore-auto-dns = yes
```

La aplicación reconecta el perfil y valida que la red continúe activa, que DNSCrypt responda y que la resolución del sistema funcione. Si falla la operación, intenta restaurar el estado anterior.

## Proton VPN

Cuando Proton VPN está activo, NetworkPrivacy no modifica la política DNS almacenada del Wi-Fi. La interfaz muestra DNSCrypt como **EN ESPERA** y Proton como DNS efectivo.

Al desconectar Proton, NetworkManager vuelve automáticamente a la política guardada en el perfil Wi-Fi.

## Interfaz

La aplicación actualiza su estado automáticamente cada dos segundos. Muestra:

- conexión Wi-Fi actual;
- estado de DNSCrypt;
- estado de Proton VPN;
- DNS efectivo;
- acción contextual para activar DNSCrypt o restaurar la configuración original.

La acción de activación se destaca visualmente; restaurar DNS utiliza una acción neutral. Las operaciones que reconectan la red requieren confirmación.

## Instalación e integración con XFCE

Desde la raíz del repositorio:

```bash
./Scripts/NetworkPrivacy/install-network-privacy.sh install
```

El instalador valida dependencias, crea el directorio de estado y registra:

```text
~/.local/share/applications/sineos-network-privacy.desktop
```

El lanzador aparece como **SineOS Privacidad de red** en la categoría **Internet** de XFCE y ejecuta la aplicación sin abrir una terminal.

Para revisar el estado:

```bash
./Scripts/NetworkPrivacy/install-network-privacy.sh status
```

Para retirar únicamente el lanzador:

```bash
./Scripts/NetworkPrivacy/install-network-privacy.sh uninstall
```

La desinstalación del lanzador no elimina el estado de perfiles ni modifica NetworkManager.

## Validaciones realizadas

Se validó el ciclo completo:

1. DNS automático -> activar DNSCrypt.
2. DNSCrypt activo -> restaurar DNS original.
3. DNSCrypt activo -> conectar Proton VPN -> DNSCrypt en espera.
4. Proton activo -> desconectar Proton -> DNSCrypt vuelve a ser efectivo.
5. Cambios externos de Proton detectados automáticamente por la interfaz.
6. Estado visual contrastado con `nmcli`, `/etc/resolv.conf` y resolución real.

## Limitaciones conocidas

La validación DNS utiliza conectividad externa. Una red con portal cautivo o sin Internet puede provocar una validación fallida y rollback aunque NetworkManager esté funcionando correctamente.

NetworkPrivacy no pretende reemplazar Proton VPN, NetworkManager ni dnscrypt-proxy; coordina la política entre estos componentes.
