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

### Technical-Debt.md\nDeuda técnica abierta y decisiones ya cerradas.\n\n### Quarterly-Health.md\nPolítica y estado de la auditoría profunda trimestral de salud de SineOS.

### XFCE-Visual-Configuration.md
Instalación, aplicación, respaldo, restauración y mantenimiento del escritorio XFCE reproducible.

## Recovery

### Backup-Policy.md
Política general de backups: clasificación de datos, frecuencia, retención, cifrado, verificación, restore y relación con Btrfs/Snapper y Restic.

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