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

## Lifecycle

`Documentation/Lifecycle/README.md` es el runbook vivo de construcción de SineOS.

Contiene capítulos numerados desde la preparación de la imagen de Debian hasta el estado actual, con comandos listos para terminal y marcas explícitas de qué fue validado y qué necesita revalidación.

También enlaza los programas propios, scripts, stacks y documentos profundos que sostienen cada etapa.

## Architecture

### AI-Architecture.md
Arquitectura híbrida de IA, modelos, routing, privacidad y relación con Ollama, Miyo, Obsidian y servicios cloud.

### Knowledge-Vault.md
Modelo del Knowledge Vault, separación respecto al repositorio y relaciones del sistema académico.

### Native-Applications.md
Estándar de aplicaciones nativas SineOS y principios de experiencia de usuario.

### Script-Standard.md
Clasificación, ciclo de vida, seguridad, documentación y criterios para conservar scripts.

### Documentation-Standard.md
Estándar general de documentación y Definition of Done documental para componentes SineOS.

### SineOS-Desktop-Experience.md
Plan de arquitectura congelado para **SineOS Desktop Experience (SDE)**: evolución visual y de interacción de XFCE/X11 orientada a bajo consumo, compatibilidad, escalabilidad, replicabilidad y recuperación. El documento está marcado como pendiente de implementación y se sigue mediante el issue maestro #1.

### SDE-Visual-Interaction-Refinements.md
Addendum congelado de refinamientos visuales e interacción: Snap Preview, fullscreen/maximizado, Launch/Progress Feedback, CSD/SSD, Docklike, Safe Areas, diálogos y soporte de resoluciones heredadas.

### SDE-Packaging-Recovery-Certification.md
Política congelada de empaquetado Debian, recuperación local/GitHub/offline, certificación C0-C5, estados de soporte de hardware y ciclo Alpha → Beta → RC → Stable.

### SDE-UX-Contract.md
Contrato formal de experiencia de usuario de SDE: latencia, feedback inmediato, No Dead Clicks, No Surprise Movement, Display Transactions, Last Known Good, Resume Validation, privacidad al proyectar, coordinación display/audio, accesibilidad, Edit Mode y criterios UX de aceptación.

### SDE-Session-Power-Experience.md
Política congelada del ciclo completo de sesión y energía: Plymouth en arranque/reinicio/apagado, LightDM + Slick Greeter para login, xfce4-screensaver para bloqueo, contraseña obligatoria, hibernación al cerrar tapa, TLP para políticas AC/BAT, Resume Validation y criterios de recuperación.

## Operations

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

## Recovery

### Backup-Policy.md
Política general de backups: disco externo `SineOsBackups`, ciclo trimestral, cifrado, validación por restore, Restic y sincronización GitHub.

### Backup-Status.md
Estado versionado del último respaldo externo validado.

### Backup-Log/
Bitácora histórica `Respaldo-<commit>.md` de respaldos certificados y sincronizados.

## Security

### README.md
Entrada a la documentación de seguridad.

### Security-Baseline.md
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