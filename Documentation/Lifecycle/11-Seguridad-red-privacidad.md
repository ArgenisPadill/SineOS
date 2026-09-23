# 11 — Seguridad, red y privacidad

**Estado:** PARCIALMENTE VALIDADO / HARDENING EN PROGRESO

## Principio

Los cambios de seguridad de SineOS siguen:

```text
diagnóstico
   ↓
plan
   ↓
cambio
   ↓
validación
   ↓
persistencia
   ↓
documentación
```

## nftables

Estado validado:

- servicio operativo;
- cadena INPUT con política `drop`;
- loopback permitido;
- `established,related` permitido;
- ICMP/ICMPv6 permitido;
- LocalSend TCP/UDP 53317 limitado a la LAN de confianza;
- Ollama protegido frente a conexiones LAN no solicitadas.

Comprobar:

```bash
systemctl status nftables --no-pager
sudo nft list ruleset
ss -tulpn
```

## Hueco crítico

El ruleset operativo de nftables todavía no está versionado como artefacto reproducible de SineOS. La guía no inventa esas reglas.

Antes de una reconstrucción definitiva debe recuperarse y sanearse la configuración real, parametrizando la LAN como `<TRUSTED_LAN_CIDR>`.

## DNSCrypt

DNSCrypt fue validado en:

```text
127.0.2.1:53
```

Comprobar:

```bash
systemctl status dnscrypt-proxy --no-pager
ss -lunp | grep ':53'
dig @127.0.2.1 debian.org +short
```

DNSCrypt se aplica por perfil de NetworkManager, no globalmente.

## Proton VPN

Cuando Proton VPN está activo, Proton controla DNS y routing. Se validó el ciclo WireGuard/policy routing y el retorno a DNSCrypt al desconectar.

Comprobar estado de red:

```bash
nmcli -t -f NAME,TYPE,DEVICE connection show --active
ip -br address
ip route
cat /etc/resolv.conf
```

## Servicios revisados

Durante el hardening:

```text
KDE Connect -> retirado
i2pd        -> retirado
redsocks    -> retirado
AnyDesk     -> conservado por uso real
Dropbox     -> conservado por uso real
MEGA        -> conservado por uso real
Avahi       -> conservado
Tor         -> pendiente de identificar consumidores
```

## Tor

Comprobar antes de eliminar:

```bash
systemctl status tor --no-pager
ss -ltnp | grep ':9050' || true
```

No retirar Tor hasta identificar si existe un consumidor real.

## AppArmor

AppArmor está presente en la arquitectura, pero su auditoría formal sigue pendiente.

```bash
systemctl status apparmor --no-pager
sudo aa-status
```

## Secure Boot

```bash
mokutil --sb-state
```

## Pendientes para cerrar seguridad

- auditoría AppArmor;
- verificación de LUKS;
- gestión formal de secretos;
- rotación/gestión de credenciales;
- revisión nftables + Podman/netavark;
- validación de Ollama desde otro dispositivo;
- backups y restore;
- Disaster Recovery.

## Documentación

- `Documentation/Security/Security-Baseline.md`
- `Documentation/Operations/Technical-Debt.md`