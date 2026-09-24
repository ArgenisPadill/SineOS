# SineOS — Estado de salud trimestral

**Estado:** Implementación en progreso  
**Frecuencia:** Cada 3 meses

## Objetivo

Ejecutar una auditoría profunda del estado real de SineOS y conservar evidencia suficiente para decidir si el sistema está sano, requiere mantenimiento o presenta riesgos pendientes.

## Auditor

```text
Scripts/Audit/sineos-health-audit.sh
```

El auditor revisa, entre otros:

- Debian y kernel;
- sincronización Git/GitHub;
- unidades systemd fallidas;
- errores del journal;
- estado de APT y paquetes actualizables;
- paquetes obsoletos/sin fuente;
- coherencia de dpkg;
- vulnerabilidades mediante debsecan;
- uso de almacenamiento;
- Btrfs;
- SMART cuando es accesible;
- AppArmor;
- nftables;
- Podman y contenedores;
- auditoría de secretos;
- estado del último backup.

## Certificación

El script diferencia:

```text
RESULTADO: OK
RESULTADO: CON_ADVERTENCIAS
RESULTADO: REQUIERE_ATENCION
```

Un ciclo trimestral solo puede marcarse como completado cuando los errores hayan sido resueltos o explícitamente documentados y el evento quede sincronizado con GitHub.

## Dependencias importantes

Para certificar vulnerabilidades se requiere:

```text
debsecan
```

Para revisar SMART:

```text
smartmontools
```

La primera ejecución determinará qué dependencias ya están disponibles y cuáles deben añadirse.

## GitHub

GitHub es la fuente remota de configuración reproducible y evidencia del mantenimiento.

La aplicación de mantenimiento debe verificar:

```text
git status limpio
HEAD local = main remoto
```

antes de considerar cerrado el recordatorio trimestral.

## Recordatorio persistente

El estado pendiente no depende únicamente de una notificación visual.

La futura aplicación nativa guardará estado local persistente y un servicio/timer de usuario volverá a notificar mientras el ciclo siga vencido.

## Estado actual

```text
Auditor profundo          CREADO / PENDIENTE DE PRIMERA VALIDACIÓN
Aplicación nativa         PENDIENTE
Servicio/timer            PENDIENTE
Primer ciclo trimestral   PENDIENTE
```
