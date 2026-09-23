# 12 — SineOS NetworkPrivacy

**Estado:** VALIDADO

## Por qué existe

Administrar DNSCrypt, NetworkManager y el estado de Proton VPN desde terminal era posible, pero poco práctico para una operación cotidiana.

NetworkPrivacy convierte ese flujo en una aplicación nativa que muestra estado, previene acciones incompatibles y permite activar/restaurar DNS sin recordar comandos.

## Programa

```text
Apps/NetworkPrivacy/
├── sineos-network-privacy.py
└── network_policy.py
```

## Tecnología

```text
Python 3
GTK3 / PyGObject
NetworkManager / nmcli
dnscrypt-proxy
Polkit
```

## Dependencias

```bash
sudo apt update
sudo apt install -y \
  python3 python3-gi gir1.2-gtk-3.0 \
  network-manager dnsutils libnotify-bin \
  dnscrypt-proxy
```

Debe existir además un agente gráfico Polkit en la sesión.

## Instalación

```bash
cd "$HOME/Workspace/SineOS"
./Scripts/NetworkPrivacy/install-network-privacy.sh install
```

## Estado

```bash
./Scripts/NetworkPrivacy/install-network-privacy.sh status
```

## Lanzador

El instalador crea:

```text
~/.local/share/applications/sineos-network-privacy.desktop
```

La aplicación aparece en la categoría Internet de XFCE y se ejecuta sin terminal.

## Estado persistente

```text
~/.local/state/sineos-network-privacy/profiles.json
```

Permisos esperados:

```bash
stat -c '%a %n' ~/.local/state/sineos-network-privacy ~/.local/state/sineos-network-privacy/profiles.json 2>/dev/null || true
```

El directorio debe usar 700 y el archivo 600.

## Política

```text
Red de confianza -> DNSCrypt
Red nueva/pública -> DNS DHCP inicialmente
Proton VPN activa -> Proton controla DNS/routing
```

## Validación manual

```bash
nmcli connection show --active
systemctl is-active dnscrypt-proxy
cat /etc/resolv.conf
dig @127.0.2.1 debian.org +short
```

## Desinstalar integración

```bash
./Scripts/NetworkPrivacy/install-network-privacy.sh uninstall
```

Esto retira el lanzador; no borra silenciosamente el estado de perfiles ni modifica NetworkManager.

## Estándar derivado

NetworkPrivacy se convirtió en la aplicación de referencia para el estándar de apps nativas y UX de SineOS.

## Documentación

- `Documentation/Operations/NetworkPrivacy.md`
- `Documentation/Architecture/Native-Applications.md`
- `Apps/README.md`