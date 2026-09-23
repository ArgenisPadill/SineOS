# 02 — Configuración base de Debian

**Estado:** VALIDADO HISTÓRICAMENTE

## Repositorios y actualización

Se utilizó Debian 13 Trixie con repositorios normales, security y updates, incluyendo firmware no libre cuando fue necesario.

Comprobación:

```bash
grep -RhsE '^[[:space:]]*deb ' /etc/apt/sources.list /etc/apt/sources.list.d 2>/dev/null
sudo apt update
apt list --upgradable
```

## Herramientas base

Paquetes utilizados habitualmente en SineOS:

```bash
sudo apt install -y \
  git curl wget jq tree \
  ca-certificates openssh-client \
  btrfs-progs smartmontools \
  network-manager network-manager-gnome \
  python3 python3-gi gir1.2-gtk-3.0 \
  dnsutils libnotify-bin
```

## NetworkManager

Durante la construcción se corrigió la administración de red para que NetworkManager fuera el administrador efectivo de las interfaces y `ifupdown` quedara limitado al loopback.

Validación actual:

```bash
nmcli general status
nmcli device status
nmcli connection show
ip -br address
ip route
cat /etc/resolv.conf
```

## Wi-Fi

El equipo validado utiliza hardware Intel y el Wi-Fi quedó operativo después de corregir NetworkManager y firmware.

Comprobación:

```bash
lspci -nnk | grep -A3 -i network
nmcli radio wifi
nmcli device wifi list
```

## Audio

Durante la construcción se reparó la integración de audio y teclas multimedia de XFCE.

Validación:

```bash
pactl info
pactl list short sinks
pactl list short sources
```

## Servicios problemáticos

Antes de copiar configuraciones antiguas debe comprobarse siempre el estado real:

```bash
systemctl --failed --no-pager
journalctl -p err -b --no-pager
```

## Regla

No instalar paquetes únicamente porque aparecieron alguna vez durante el desarrollo. La lista definitiva de dependencias globales de SineOS sigue siendo deuda documental y deberá derivarse de una reconstrucción limpia.