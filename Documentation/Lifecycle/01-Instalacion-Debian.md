# 01 — Instalación de Debian

**Estado:** VALIDADO EN ESTADO FINAL / PROCEDIMIENTO INICIAL PARCIALMENTE RECONSTRUIDO

## Estado que sí fue comprobado

```text
Debian GNU/Linux 13 Trixie
Kernel 6.12
x86_64
UEFI
Secure Boot habilitado
Btrfs como filesystem raíz
swapfile Btrfs de 16 GiB
fstrim.timer activo
```

Durante la instalación original se validó posteriormente una raíz Btrfs con opciones equivalentes a:

```text
compress=zstd:3
discard=async
space_cache=v2
```

## Decisiones

- Debian Stable como base;
- Btrfs para facilitar snapshots y recuperación futura;
- no se diseñó el sistema alrededor de hibernación;
- Secure Boot se conservó;
- el cifrado LUKS no debe asumirse como validado hasta completar su auditoría.

## Verificación después de instalar

```bash
cat /etc/os-release
uname -a
uname -m
findmnt /
lsblk -f
swapon --show
systemctl status fstrim.timer --no-pager
mokutil --sb-state 2>/dev/null || true
```

Para Btrfs:

```bash
sudo btrfs filesystem show
sudo btrfs filesystem usage /
sudo btrfs subvolume list /
```

## Punto pendiente

No se conservó con suficiente precisión el flujo de particionado del instalador Debian. No se publicará una receta ficticia.

En la próxima reconstrucción desde cero deben registrarse:

- tabla de particiones;
- tamaños;
- EFI;
- raíz Btrfs;
- creación del swapfile compatible con Btrfs;
- `fstab` final;
- decisión definitiva sobre LUKS.