# Documentación de SineOS

Este directorio es el punto de entrada a la documentación técnica de SineOS.

El objetivo no es únicamente describir componentes aislados, sino permitir entender, operar, reconstruir, mantener y recuperar el sistema de forma reproducible.

## Cómo está organizada

```text
Documentation/
├── Lifecycle/      # guía ordenada para construir y reconstruir SineOS
├── Architecture/   # por qué existe cada diseño y cómo se relacionan sus partes
├── Operations/     # cómo se usa, valida, mantiene y diagnostica
├── Security/       # controles, riesgos, políticas y hardening
└── Recovery/       # se incorporará cuando existan procedimientos validados
```

No se crean directorios vacíos solo para representar una arquitectura futura.

## Ciclo de vida

`Documentation/Lifecycle/README.md` es el runbook vivo de construcción de SineOS.

Contiene capítulos numerados desde la preparación de la imagen de Debian hasta el estado actual, con comandos listos para terminal y marcas explícitas de qué fue validado y qué necesita revalidación.

También enlaza los programas propios, scripts, stacks y documentos profundos que sostienen cada etapa.

## Arquitectura

### AI-Architecture.md
Arquitectura híbrida de IA, modelos, routing, privacidad y relación con Ollama, Miyo, Obsidian y servicios cloud.

### Knowledge-Vault.md
Modelo del Knowledge Vault, separación respecto al repositorio y relaciones del sistema académico.

### Native-Applications.md
Estándar de aplicaciones nativas SineOS y principios de experiencia de usuario.

### Script-Standard.md
Clasificación, ciclo de vida, seguridad, documentación y criterios para conservar scripts.

### Documentation-Standard.md
Estándar general de documentación y definición de terminado para componentes SineOS.

### SineOS-Desktop-Experience.md
Plan de arquitectura congelado para **SineOS Desktop Experience (SDE)**: evolución visual y de interacción de XFCE/X11 orientada a bajo consumo, compatibilidad, escalabilidad, replicabilidad y recuperación. El documento está marcado como pendiente de implementación y se sigue mediante el issue maestro #1.

### SDE-Visual-Interaction-Refinements.md
Anexo congelado de refinamientos visuales e interacción: vista previa de ajuste de ventanas, pantalla completa/maximizado, respuesta de inicio/progreso, CSD/SSD, Docklike, áreas seguras, diálogos y soporte de resoluciones heredadas.

### SDE-Packaging-Recovery-Certification.md
Política congelada de empaquetado Debian, recuperación local/GitHub/offline, certificación C0-C5, estados de soporte de hardware y ciclo Alpha → Beta → RC → Estable.

### SDE-UX-Contract.md
Contrato formal de experiencia de usuario de SDE: latencia, respuesta inmediata, sin clics muertos, sin movimientos inesperados, transacciones de pantalla, último estado funcional, validación posterior a reanudación, privacidad en pantallas externas, coordinación pantalla/audio, accesibilidad, modo de edición y criterios de aceptación UX.

### SDE-Session-Power-Experience.md
Política congelada del ciclo completo de sesión y energía: Plymouth en arranque/reinicio/apagado, LightDM + Slick Greeter para inicio de sesión, xfce4-screensaver para bloqueo, contraseña obligatoria, hibernación al cerrar tapa, TLP para políticas AC/BAT, validación posterior a reanudación y criterios de recuperación.

### SDE-System-Integration.md
Integración congelada de red, portales cautivos, Ethernet/Wi-Fi, VPN, Bluetooth, USB, almacenamiento y política de drivers/firmware.

### SDE-Devices-Printing-Scanning.md
Política congelada de impresión y escaneo: instalación guiada, hoja de prueba SineOS, consumibles, mantenimiento, OCR, PDF buscable y revisión previa al guardado.

### SDE-Privacy-Permissions-Remote-Access.md
Política congelada de privacidad, permisos sensibles, autorizaciones Polkit temporales, acceso remoto, indicadores y bitácoras.

### SDE-Hardware-Health.md
Política congelada de salud de hardware: batería, temperatura, SMART, RAM, CPU, GPU, sistema de archivos, modo seguro y reportes técnicos.

### SDE-Updates-Migration.md
Política congelada de actualizaciones, puntos de restauración y migración desde el XFCE actual hacia SDE.

### SDE-Implementation-Roadmap.md
Orden congelado de implementación de SDE 1.0, desde recovery y respaldo pre-SDE hasta certificación final.

### SDE-Definition-of-Done-1.0.md
Criterios obligatorios para declarar SDE 1.0 terminado y estable.

### SDE-Alpha-0.1-Technical-Manifest.md
Manifiesto técnico inicial de Alpha 0.1: paquetes, propiedad de archivos, estructura de configuración/estado, CLI mínima, respaldo pre-SDE, transacción de instalación, rollback, gates y pendientes previos a implementación.

## Operaciones

### Academic-Templates.md
Sistema académico de Obsidian/Templater y validación de sus entidades.

### Miyo.md
Operación, arquitectura, integración, actualización y troubleshooting de Miyo.

### NetworkPrivacy.md
Funcionamiento e integración de la aplicación de privacidad de red.

### Ollama.md
Instalación operativa, modelos, seguridad, rendimiento, backup, migración y troubleshooting.

### Open-WebUI.md
Arquitectura y operación del stack Open WebUI.

### PostgreSQL.md
Estado operativo actual de PostgreSQL 18 sobre Podman rootless.

### Technical-Debt.md
Deuda técnica abierta y decisiones ya cerradas.

### Quarterly-Health.md
Política y estado de la auditoría profunda trimestral de salud de SineOS.

### Health-Status.md
Último estado trimestral validado que sirve como evidencia versionada para el gate GitHub.

### Maintenance.md
Arquitectura, instalación y operación de la aplicación nativa SineOS · Mantenimiento.

### XFCE-Visual-Configuration.md
Instalación, aplicación, respaldo, restauración y mantenimiento del escritorio XFCE reproducible.

## Recuperación

### Backup-Policy.md
Política general de backups: disco externo `SineOsBackups`, ciclo trimestral, cifrado, validación por restore, Restic y sincronización GitHub.

### Backup-Status.md
Estado versionado del último respaldo externo validado.

### Backup-Log/
Bitácora histórica `Respaldo-<commit>.md` de respaldos certificados y sincronizados.

## Seguridad

### README.md
Entrada a la documentación de seguridad.

### Seguridad-Baseline.md
Baseline de seguridad, estado de controles, red, servicios, secretos, backups y hardening.

### Documentation-Privacy.md
Reglas para evitar publicar secretos, rutas privadas, identificadores y reportes sensibles.

### Secrets-Management.md
Política de almacenamiento, permisos, inventario, escaneo y rotación de secretos.

### Agentic-Security-Validation.md
Diseño de la etapa final de validación defensiva asistida por agente.

### Agentic-Security-Allowlist.md
Allowlist inicial de skills defensivas autorizadas para evaluación de SineOS.

## Programas propios

El catálogo de aplicaciones y programas desarrollados específicamente para SineOS se encuentra en:

`Apps/README.md`

## Scripts

El catálogo operativo de scripts se encuentra en:

`Scripts/README.md`

La política de scripts se encuentra en:

`Documentation/Architecture/Script-Standard.md`

## Documentación que todavía falta

Estos huecos no se consideran documentación terminada hasta que exista implementación o validación suficiente.

### Prioridad alta

- instalación completa de SineOS desde Debian 13 limpio;
- inventario global de dependencias;
- backup y restore probado de PostgreSQL;
- backup y recuperación del Knowledge Vault;
- Disaster Recovery completo;
- procedimiento global de actualización de SineOS.

### Prioridad media

- documento operativo del auditor;
- documento operativo del sistema de monitoreo;
- runbook específico de nftables/firewall;
- troubleshooting general por capas;
- instalación/actualización/recuperación completa de Stirling PDF;
- instalación/actualización/recuperación completa de Uptime Kuma;
- instalación inicial completa y restore de Open WebUI.

## Regla

> La ausencia de documentación se registra como deuda; no se rellena con procedimientos no probados.

Cuando un procedimiento sea validado, debe sustituir la deuda correspondiente y quedar enlazado desde este índice.