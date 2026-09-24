# SineOS — Validación final de seguridad asistida por agente

**Etapa:** Final del bloque de seguridad  
**Estado:** PLANIFICADA / NO EJECUTADA  
**Fuente evaluada:** `mukul975/Anthropic-Cybersecurity-Skills`  
**Commit revisado:** `54a798831d2266a3ca61ce68a7acb80b81160d57`  
**Fecha de revisión:** 23-09-2026

## Propósito

Esta etapa añade una revisión de seguridad asistida por IA después de completar el hardening, backups, recuperación y demás controles base de SineOS.

No sustituye los controles existentes.

Su función es utilizar procedimientos especializados de seguridad para encontrar huecos que una revisión manual pueda haber omitido y convertirlos en hallazgos verificables.

## Fuente

El proyecto evaluado es una biblioteca comunitaria de skills de ciberseguridad para agentes de IA.

En el commit revisado contiene 818 skills y cubre áreas como:

- endpoint security;
- network security;
- container security;
- vulnerability management;
- incident response;
- supply-chain security;
- hardware/firmware security;
- AI security;
- backup/recovery;
- penetration testing y red teaming.

El proyecto declara explícitamente que es comunitario y que no está afiliado a Anthropic.

También incluye procedimientos ofensivos y de doble uso.

## Decisión de SineOS

> SineOS NO activa automáticamente la biblioteca completa.

La etapa final utiliza un perfil defensivo con una allowlist explícita.

Las técnicas ofensivas permanecen fuera del flujo automático normal.

## Momento de ejecución

Esta fase solo debe comenzar cuando estén cerrados o aceptados conscientemente los controles anteriores:

```text
AppArmor
LUKS / cifrado
inventario de puertos
nftables + Podman/netavark
exposición de Ollama
gestión de secretos
credenciales
backups
restore probado
snapshots
Disaster Recovery
```

Si esas capas siguen abiertas, el agente puede utilizarse para investigación puntual, pero la etapa no puede marcarse como completada.

## Modelo operativo

```text
estado real del sistema
        ↓
auditoría SineOS
        ↓
skills defensivas seleccionadas
        ↓
agente
        ↓
hallazgos y recomendaciones
        ↓
revisión humana
        ↓
cambio individual
        ↓
validación
        ↓
documentación
```

## Permisos

Por defecto la primera pasada debe ser de solo lectura.

El agente puede:

- consultar configuración;
- inspeccionar estado;
- leer logs previamente autorizados;
- analizar archivos de configuración;
- revisar imágenes/artefactos;
- comparar contra baselines;
- generar hallazgos y propuestas.

El agente no debe modificar automáticamente:

- nftables;
- NetworkManager;
- DNS;
- VPN;
- bootloader;
- Secure Boot;
- TPM;
- LUKS;
- particiones/filesystems;
- cuentas y grupos;
- sudoers;
- secretos;
- claves SSH;
- datos PostgreSQL;
- backups;
- contenedores productivos.

Los cambios de esas categorías requieren aprobación humana y ejecución como tarea independiente.

## Fuente externa reproducible

No se vendoriza la biblioteca completa dentro del repositorio SineOS.

Cuando se ejecute la etapa, se utilizará una copia externa y una referencia fijada.

Ejemplo de preparación controlada:

```bash
mkdir -p "$HOME/.local/share/sineos/security"
cd "$HOME/.local/share/sineos/security"

git clone https://github.com/mukul975/Anthropic-Cybersecurity-Skills.git
cd Anthropic-Cybersecurity-Skills

git checkout --detach 54a798831d2266a3ca61ce68a7acb80b81160d57
git rev-parse HEAD
```

Antes de una ejecución futura puede elegirse un commit más reciente, pero debe revisarse y registrarse primero.

## No usar instalación global automática inicialmente

El upstream ofrece:

```bash
npx skills add mukul975/Anthropic-Cybersecurity-Skills
```

SineOS no adopta inicialmente ese mecanismo porque incorpora la biblioteca completa al entorno del agente.

Se prefiere una integración controlada y selectiva hasta comprender exactamente el comportamiento del runtime utilizado.

## Frameworks útiles

La biblioteca se encuentra mapeada, entre otros, a:

- NIST CSF 2.0;
- MITRE ATT&CK;
- MITRE D3FEND;
- NIST AI RMF;
- MITRE ATLAS.

Para SineOS el principal marco defensivo de esta etapa será NIST CSF:

```text
Govern
Identify
Protect
Detect
Respond
Recover
```

## Resultados esperados

La ejecución final debe producir como mínimo:

1. inventario de hallazgos;
2. evidencia que sustenta cada hallazgo;
3. nivel de impacto/prioridad;
4. control o componente afectado;
5. recomendación;
6. riesgo de aplicar la recomendación;
7. mecanismo de rollback;
8. resultado de la revalidación.

## Regla de evidencia

Una recomendación del agente no equivale a un hallazgo confirmado.

El flujo obligatorio es:

```text
sugerencia
  ↓
evidencia local
  ↓
confirmación
  ↓
remediación
  ↓
revalidación
```

## Seguridad del propio agente

Las instrucciones externas también constituyen una entrada no confiable.

Por ello:

- no se conceden privilegios root permanentes;
- no se entregan secretos innecesarios al modelo;
- no se ejecutan comandos destructivos sin revisión;
- no se envían datos privados a modelos cloud salvo decisión explícita;
- los reports deben sanearse antes de publicarse;
- la biblioteca externa se trata como dependencia de terceros.

## Criterio de cierre

La etapa final puede marcarse como VALIDADA únicamente cuando:

```text
[ ] El commit de la biblioteca fue registrado
[ ] La allowlist defensiva fue revisada
[ ] La primera pasada fue de solo lectura
[ ] Los hallazgos fueron contrastados con evidencia local
[ ] Las remediaciones aceptadas se aplicaron individualmente
[ ] Cada remediación fue revalidada
[ ] No quedaron secretos en reports o Git
[ ] Se generó un informe final
[ ] Las excepciones/riesgos aceptados quedaron documentados
```

## Relación con SineOS

Esta etapa no convierte SineOS en una plataforma ofensiva.

Su objetivo es utilizar conocimiento de seguridad estructurado para comprobar defensivamente que la arquitectura construida durante todo el proyecto sigue cumpliendo sus controles.