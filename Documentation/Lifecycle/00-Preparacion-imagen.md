# 00 — Preparación de la imagen de instalación

**Estado:** PENDIENTE DE REVALIDAR DESDE CERO

## Objetivo

Preparar un medio de instalación de Debian 13 amd64 para iniciar la construcción de SineOS.

El sistema final validado utiliza Debian 13 Trixie, UEFI y Secure Boot habilitado. No quedó conservado el procedimiento exacto usado originalmente para grabar la USB, por lo que este capítulo documenta un procedimiento reproducible que deberá revalidarse en la próxima instalación limpia.

## Antes de escribir una USB

Identificar dispositivos:

```bash
lsblk -o NAME,SIZE,MODEL,TRAN,MOUNTPOINTS
```

Calcular el hash de la ISO descargada:

```bash
sha256sum /ruta/a/debian-13-amd64-netinst.iso
```

Comparar el resultado con el SHA256 publicado por Debian antes de continuar.

## Escribir la imagen

**ATENCIÓN:** el dispositivo destino se sobrescribe por completo. Confirmar cuidadosamente el nombre de la USB.

```bash
ISO="/ruta/a/debian-13-amd64-netinst.iso"
USB="/dev/sdX"

lsblk -o NAME,SIZE,MODEL,TRAN,MOUNTPOINTS "$USB"
sudo cp "$ISO" "$USB"
sync
```

No utilizar una partición como `/dev/sdX1`; debe indicarse el dispositivo completo.

## Arranque esperado

- modo UEFI;
- Secure Boot puede permanecer habilitado;
- arquitectura amd64/x86_64.

## Validación posterior

Este capítulo se considerará VALIDADO cuando se repita el proceso completo en una instalación limpia y se registre el hash de la imagen utilizada y el método exacto de escritura.