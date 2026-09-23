# SineOS

**SineOS** es un entorno personal de infraestructura, administración de sistemas, desarrollo y conocimiento construido sobre Debian GNU/Linux.

El proyecto busca mantener un entorno reproducible, documentado, modular y recuperable, evitando depender de configuraciones manuales difíciles de reconstruir.

> La mejor IA no es el modelo más pesado, sino la que soporta el equipo de cómputo.

## Objetivos

SineOS busca integrar en una misma arquitectura:

- administración de sistemas Linux;
- infraestructura reproducible;
- contenedores rootless;
- bases de datos;
- desarrollo de software;
- automatización y auditoría;
- monitoreo;
- inteligencia artificial local y cloud;
- gestión estructurada del conocimiento;
- documentación técnica;
- recuperación y migración del entorno.

El proyecto está diseñado para evolucionar de manera incremental: cada componente debe poder documentarse, auditarse, mantenerse y eventualmente reconstruirse.

## Plataforma base

Entorno actualmente utilizado:

```text
Sistema operativo : Debian GNU/Linux 13 (Trixie)
Escritorio         : XFCE 4.20
Kernel             : Linux 6.12
Arquitectura       : x86_64
Filesystem         : Btrfs
Contenedores       : Podman rootless
Control de versiones: Git + GitHub
```

### Hardware principal

SineOS se desarrolla actualmente sobre una laptop Gateway GWTN141-10.

```text
CPU       : Intel Core i5-1135G7
Núcleos   : 4
Hilos     : 8
GPU       : Intel Iris Xe integrada
RAM       : 16 GB LPDDR4
SSD       : 512 GB SATA
Firmware  : UEFI
Secure Boot: habilitado
```

La arquitectura se diseña considerando los recursos reales del equipo y evitando desplegar servicios o modelos cuyo costo computacional no aporte un beneficio práctico.

## Arquitectura del repositorio

La estructura versionada actual es:

```text
SineOS/
├── Apps/
├── Containers/
├── Documentation/
├── Scripts/
├── .gitignore
├── CHANGELOG.md
└── README.md
```

Las responsabilidades se dividen actualmente en:

- **Apps:** aplicaciones propias de SineOS. Actualmente incluye NetworkPrivacy.
- **Containers:** definiciones reproducibles de los servicios desplegados mediante Podman. Los datos persistentes, respaldos, secretos y logs permanecen fuera de Git.
- **Documentation:** arquitectura, operación, seguridad y registro técnico.
- **Scripts:** auditoría, diagnóstico, mantenimiento y automatización, incluida la configuración visual reproducible de XFCE, monitoreo e instaladores de aplicaciones.

Directorios adicionales como Ansible, Terraform, Lab, Foundation, Infrastructure o Platform podrán incorporarse cuando exista una implementación real que justifique versionarlos. No se mantienen directorios vacíos únicamente como scaffolding.

## Contenedores

SineOS utiliza **Podman rootless** como plataforma principal de contenedores.

La estructura general es:

```text
Containers/
├── stacks/
├── volumes/
├── backups/
├── configs/
├── secrets/
└── logs/
```

Los datos persistentes, secretos, respaldos y logs no deben incorporarse accidentalmente al repositorio Git.

Los stacks con definición operativa actual incluyen:

```text
postgres
open-webui
stirling-pdf
uptime-kuma
```

No se conservan stacks vacíos como scaffolding. Un servicio se incorpora a `Containers/stacks/` cuando existe una definición operativa que deba versionarse.
## PostgreSQL

La base de datos principal desplegada actualmente en SineOS es **PostgreSQL 18**.

Se ejecuta mediante Podman rootless y cuenta con:

- persistencia en el host;
- acceso publicado únicamente en `127.0.0.1`;
- arranque y detención manual desde Podman Desktop;
- usuario y base de datos propios de SineOS;
- almacenamiento separado del archivo de composición;
- validación de persistencia después de reinicios.

La información sensible, como contraseñas y archivos `.env`, no debe almacenarse en Git.

La configuración se encuentra en:

```text
Containers/stacks/postgres/
```

Los datos persistentes se mantienen fuera del seguimiento de Git.

## Inteligencia artificial

SineOS utiliza una arquitectura híbrida de IA basada en el principio:

> Local first → free cloud when useful → paid DeepSeek only when it adds value.

La arquitectura actualmente definida es:

```text
                    ┌──────────────┐
                    │   Obsidian   │
                    │ Source of    │
                    │    Truth     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │     Miyo     │
                    │  Semantic    │
                    │    Index     │
                    └──────┬───────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Copilot/OpenCode  │
                 │   Agent Layer     │
                 └─────────┬─────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        Ollama/Qwen    Gemini Flash    DeepSeek
          Local           Cloud          Cloud
```

### Ollama

Ollama proporciona ejecución local de modelos para tareas privadas, simples y offline.

Modelos locales seleccionados:

```text
qwen3.5:2b
qwen2.5-coder:3b-instruct
```

Los modelos locales pequeños no se utilizan como agentes complejos cuando el costo del prompt, las herramientas y el contexto supera sus capacidades prácticas.

### Open WebUI

Open WebUI proporciona una interfaz local para interactuar con Ollama.

Configuración actual:

```text
http://127.0.0.1:3000
```

La comunicación con Ollama se realiza mediante:

```text
http://host.containers.internal:11434
```

El servicio utiliza persistencia dentro de la estructura de volúmenes de SineOS.

La imagen actualmente utiliza una etiqueta móvil y queda pendiente fijar una versión o digest antes de considerarla una configuración endurecida y reproducible.

### Gemini

Gemini 3.8 Flash funciona como modelo cloud principal para:

- contexto amplio;
- documentos;
- tareas agentic;
- integración con herramientas;
- consultas que exceden las capacidades prácticas de los modelos locales.

### DeepSeek

DeepSeek se utiliza como backend cloud de pago para tareas donde un modelo de mayor capacidad aporta valor adicional, especialmente razonamiento y programación.

La integración fue validada de extremo a extremo mediante:

```text
DeepSeek
   ↓
Copilot/OpenCode
   ↓
miyo-search
   ↓
Miyo CLI
   ↓
Servicio Miyo
   ↓
Índice semántico
   ↓
Obsidian Vault
```

### Proveedores descartados

Groq fue probado durante el desarrollo de la arquitectura.

La integración con Copilot/OpenCode presentó ciclos relacionados con la compactación del contexto utilizando los modelos evaluados, por lo que fue retirado de la arquitectura operativa.

No se agregan proveedores únicamente por disponer de una capa gratuita.

## Knowledge Vault

El conocimiento permanente de SineOS se administra mediante **Obsidian**.

El Vault se encuentra en:

```text
${SINEOS_VAULT}
```

El repositorio Git se encuentra en:

```text
${SINEOS_REPO}
```

Son componentes diferentes.

**El Vault no es un repositorio Git de SineOS.**

El repositorio contiene infraestructura y código.

El Vault contiene conocimiento, decisiones, procedimientos, incidencias y documentación académica y profesional.

Miyo proporciona búsqueda semántica sobre este conocimiento.

La arquitectura detallada está documentada en:

```text
Documentation/Architecture/Knowledge-Vault.md
```
## Sistema académico

SineOS incluye un sistema de gestión académica construido sobre Obsidian y Templater.

Actualmente existen siete templates funcionalmente validados:

```text
Materia.md
Unidad.md
Tarea.md
Actividad.md
Examen.md
Proyecto-Integrador.md
Etapa-Proyecto.md
```

Las entidades utilizan identificadores estables:

```text
MAT-YYYYMMDD-XXXX
UNI-YYYYMMDD-XXXX
TAR-YYYYMMDD-XXXX
ACT-YYYYMMDD-XXXX
EXA-YYYYMMDD-XXXX
PRO-YYYYMMDD-XXXX
ETA-YYYYMMDD-XXXX
```

El sistema implementa validación de relaciones padre-hijo, protección de notas estructurales, detección de duplicados, generación dinámica de directorios y reglas de evaluación.

La documentación completa se encuentra en:

```text
Documentation/Operations/Academic-Templates.md
```

## Auditoría

SineOS dispone de herramientas propias de auditoría y diagnóstico.

El auditor actualmente desarrollado inspecciona, entre otros:

- sistema operativo y kernel;
- hardware;
- almacenamiento y Btrfs;
- memoria y swap;
- APT y paquetes;
- servicios systemd;
- journal;
- red;
- seguridad básica;
- Git y GitHub;
- SSH;
- Podman;
- contenedores SineOS;
- PostgreSQL;
- XFCE;
- audio;
- dispositivos de entrada;
- SMART;
- procesos y recursos;
- entorno de usuario.

El auditor está diseñado para diagnóstico y evita modificar deliberadamente la configuración del sistema.

Los reportes generados no deben incorporarse automáticamente al historial de Git.

## Seguridad

SineOS adopta una estrategia de seguridad por capas.

La arquitectura prevista contempla:

1. baseline y hardening del sistema operativo;
2. control de acceso obligatorio mediante AppArmor;
3. firewall;
4. SSH;
5. aislamiento mediante Podman rootless;
6. gestión de secretos;
7. cifrado y almacenamiento;
8. snapshots y recuperación;
9. monitoreo y auditoría;
10. VPN y privacidad cuando sean necesarias;
11. gestión de credenciales;
12. backup y recuperación ante desastres.

No todas estas capas se consideran actualmente terminadas.

Las configuraciones pendientes se documentan como deuda técnica en lugar de presentarlas como controles ya implementados.

## Estado actual

Componentes validados o funcionales:

- Debian GNU/Linux 13 como plataforma base;
- Btrfs;
- Git y acceso a GitHub mediante SSH;
- Podman rootless;
- PostgreSQL 18 con persistencia;
- Ollama;
- Open WebUI;
- Obsidian;
- Miyo;
- búsqueda semántica local;
- integración agentic con el Vault;
- Gemini como backend cloud principal;
- DeepSeek como backend adicional;
- arquitectura académica;
- siete templates académicos funcionalmente validados;
- configuración visual reproducible de XFCE con barra superior translúcida, Dock auto-ocultable, tema, iconos y tipografías documentadas;
- firewall nftables activo con política de entrada restrictiva;
- Proton VPN validado con DNS propio durante la conexión;
- DNSCrypt integrado por perfil de NetworkManager para redes de confianza;
- NetworkPrivacy v0.3 para activar/restaurar DNSCrypt por red y mostrar el estado de Proton VPN;
- lanzador de NetworkPrivacy integrado al menú Internet de XFCE.

## Servicios locales y monitoreo

| Componente | Ejecución | Acceso host |
|---|---|---|
| PostgreSQL 18 | Podman rootless, manual | `127.0.0.1:5432` |
| Open WebUI | Podman rootless | `127.0.0.1:3000` |
| Stirling PDF | Podman rootless, manual | `127.0.0.1:8080` |
| Uptime Kuma | Podman rootless, manual | `127.0.0.1:3001` |
| Ollama 0.34.0 | host | `*:11434`, protegido por nftables |
| DNSCrypt | host | `127.0.2.1:53` |
| Tor | host, en revisión | `127.0.0.1:9050` |

Uptime Kuma usa la red `sineos-monitoring`. Stirling PDF se comprueba directamente en esa red; Open WebUI y PostgreSQL usan scripts Push desde el host. Las URLs Push permanecen fuera de Git en `~/.config/sineos/monitoring/`.

## Trabajo pendiente

- fijar versión/digest de Open WebUI, definir secret persistente y retirar `restart: unless-stopped` mediante recreación controlada;
- determinar si Tor tiene consumidores reales;
- validar Ollama desde otro dispositivo de la LAN;
- revisar `flush ruleset` de nftables frente a Podman/netavark;
- completar auditoría de AppArmor;
- revisar manualmente candidatos de `apt autoremove`;
- definir backups de PostgreSQL/Vault, snapshots y Disaster Recovery;
- formalizar actualización de Miyo y continuar benchmarks semánticos;
- crear templates de Incidencia, Procedimiento y ADR.

## Principios del proyecto

SineOS sigue cuatro principios fundamentales:

**Reproducibilidad**
Una configuración importante debe poder reconstruirse.

**Documentación**
Una decisión técnica relevante debe quedar explicada.

**Seguridad**
Los secretos y datos persistentes no pertenecen al repositorio.

**Pragmatismo**
Las herramientas se seleccionan según el valor que aportan y los recursos reales disponibles.

---

SineOS es un proyecto personal en evolución. Los componentes marcados como pendientes o experimentales no deben interpretarse como configuraciones de producción terminadas.
