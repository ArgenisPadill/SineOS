# Changelog

Todos los cambios relevantes de SineOS se documentan en este archivo.

## [Unreleased]

### Red, privacidad y seguridad — 2026-09-23

- Activado y validado nftables con política de entrada restrictiva y excepción de LocalSend limitada a la LAN configurada.
- Eliminados KDE Connect, i2pd y redsocks tras verificar que no eran necesarios para la operación actual.
- Reparado el servicio de split tunneling de Proton VPN instalando los headers del kernel y el metapaquete `linux-headers-amd64`.
- Validado el ciclo Proton VPN: interfaz WireGuard, policy routing y DNS de Proton durante la conexión.
- Integrado DNSCrypt en el perfil Wi-Fi de confianza sin imponerlo globalmente a redes nuevas o cautivas.
- Añadida NetworkPrivacy v0.3, aplicación GTK3 para administrar DNSCrypt por perfil, detectar Proton VPN y restaurar la configuración DNS original.
- Añadido instalador de NetworkPrivacy y lanzador para la categoría Internet de XFCE.
- PostgreSQL limitado a `127.0.0.1:5432` y ajustado a política de arranque manual.
- Conservados AnyDesk, Dropbox, MEGA y Avahi por uso funcional; permanecen sujetos a la política del firewall.
- Tor queda pendiente de determinar si alguna aplicación lo utiliza antes de retirarlo o conservarlo.
- Definida como etapa final de seguridad una validación defensiva asistida por agente basada en `mukul975/Anthropic-Cybersecurity-Skills`, con commit revisado, allowlist explícita y primera pasada de solo lectura.
- La biblioteca externa no se activa completa por defecto: SineOS separa los procedimientos defensivos de las técnicas ofensivas/dual-use y mantiene revisión humana antes de cualquier remediación.
- Auditado Stirling PDF 2.14.3: se confirmó que el entrypoint upstream restablece `/configs` a permisos 755 en cada arranque; el hallazgo queda documentado y pendiente de reevaluar en una futura versión estable sin introducir un parche local frágil.
- Adoptada la política formal de gestión de secretos de SineOS, incluyendo ubicaciones permitidas, permisos, inventario, escaneo con Gitleaks y criterios de rotación.
- Ejecutado Gitleaks 8.16.0 sobre el working tree y todo el historial Git: 0 hallazgos en ambos escaneos; reportes locales almacenados fuera del repositorio con permisos restrictivos.

### Automatización y organización

- La automatización visual de XFCE se trasladó a `Scripts/Desktop/`.
- La documentación visual se trasladó a `Documentation/Operations/XFCE-Visual-Configuration.md`.
- La aplicación NetworkPrivacy permanece en `Apps/NetworkPrivacy/`; su instalación e integración de escritorio se automatiza desde `Scripts/NetworkPrivacy/`.


### Documentación

- Creada `Documentation/Lifecycle/` como guía viva y numerada de construcción/reconstrucción de SineOS, desde preparación de Debian hasta el estado actual.
- Añadidos comandos operativos listos para terminal y estados `VALIDADO`, `VALIDADO HISTÓRICAMENTE` y `PENDIENTE DE REVALIDAR` para evitar documentar como hecho lo que aún no se ha reproducido desde cero.
- Creado `Apps/README.md` como catálogo de programas propios de SineOS; NetworkPrivacy queda registrada como primera aplicación de referencia.
- Integrados en la guía los ciclos de Debian, XFCE, Git/SSH, Podman, PostgreSQL, Ollama, Open WebUI, Knowledge Vault/Miyo, monitoreo, seguridad, NetworkPrivacy, automatización y auditoría.
- Identificados como huecos de reproducibilidad los timers de monitoreo y el ruleset nftables, que funcionan en el equipo pero todavía no están versionados como código.

- Creado un índice central de documentación en `Documentation/README.md`.
- Adoptado un estándar documental con Definition of Done por componente.
- Adoptado un estándar de ciclo de vida para scripts y automatizaciones.
- Creado `Scripts/README.md` como catálogo operativo de los scripts versionados.
- Clasificados scripts pilares, recurrentes, de instalación, migración, one-shot y experimentales.
- Registrados explícitamente los huecos documentales que deben cerrarse con procedimientos validados.

- Adoptado y documentado el estándar de aplicaciones nativas de SineOS a partir de la experiencia de NetworkPrivacy.
- Definido Python 3 + GTK3/PyGObject como patrón preferente para utilidades pequeñas de escritorio cuando una GUI aporta una mejora operativa real.
- Establecidos como entregables mínimos: código fuente, instalador reproducible, integración con el menú, dependencias, manual de instalación, documentación operativa, justificación y validación funcional.
- Congelado el estándar de experiencia de usuario para aplicaciones SineOS: uso cotidiano sin terminal, estado visible, acciones contextuales, lenguaje humano, divulgación progresiva, prevención de errores, safe defaults, feedback verificable, rollback, consistencia e integración natural con XFCE.

- Creado el `README.md` principal de SineOS.
- Documentada la arquitectura general del proyecto.
- Documentada la separación entre el repositorio operativo y el Knowledge Vault.
- Documentada la arquitectura híbrida de inteligencia artificial.
- Documentado el sistema académico basado en Obsidian y Templater.
- Documentadas las relaciones MAT, UNI, TAR, ACT, EXA, PRO y ETA.
- Documentadas las reglas de evaluación para Exámenes y Proyecto Integrador.
- Registrada la batería de pruebas funcionales de los siete templates académicos.

### Knowledge Vault

- Definida la arquitectura semántica principal del Vault.
- Establecida Obsidian como fuente permanente de verdad.
- Integrado Miyo como índice y motor de búsqueda semántica.
- Validada la consulta semántica mediante Miyo CLI.
- Validada la integración agentic entre modelos cloud y el Vault.
- Definida la convención de fechas `DD-MM-AAAA`.
- Adoptados identificadores estables para las entidades académicas.
- Establecido el principio de una única nota vigente para evitar recuperación semántica de versiones obsoletas.

### Inteligencia artificial

- Establecida la estrategia:

  `Local first → free cloud when useful → paid DeepSeek only when it adds value.`

- Ollama/Qwen definido para tareas locales, privadas y offline.
- Gemini 3.8 Flash definido como backend cloud principal.
- DeepSeek integrado y validado para razonamiento y programación.
- Groq probado y retirado de la arquitectura operativa debido a problemas observados durante la integración con Copilot/OpenCode.
- Codex reservado como agente especializado de programación.
- NotebookLM reservado como herramienta independiente de investigación y docencia.

### Sistema académico

Se validaron funcionalmente:

- `Materia.md`
- `Unidad.md`
- `Tarea.md`
- `Actividad.md`
- `Examen.md`
- `Proyecto-Integrador.md`
- `Etapa-Proyecto.md`

Se validaron:

- creación dinámica del árbol académico;
- relaciones padre-hijo mediante IDs estables;
- protección de notas estructurales;
- detección de duplicados;
- selección de Unidades;
- reglas de Exámenes según modalidad;
- creación de Proyecto Integrador;
- numeración automática de Etapas;
- relación única PRO + UNI → ETA;
- cálculo acumulativo del valor de las Etapas;
- rechazo de valores superiores al disponible;
- bloqueo de nuevas Etapas al alcanzar el valor total del Proyecto.

### Correcciones

Corregido `Etapa-Proyecto.md` para utilizar el contrato real de `Unidad.md`:

```text
fmUnidad.numero        → fmUnidad.unidad
fmUnidadActual.numero  → fmUnidadActual.unidad
```

La corrección fue posteriormente validada mediante pruebas funcionales.

SHA-256 de la versión validada:

```text
75bfeb327fdc5ee04a54f55eb0fb66de409b6559794399ade51bebb8ac5a5218
```

### Infraestructura en progreso

- Open WebUI configurado para acceso local.
- Integración Open WebUI → Ollama establecida.
- Añadida exclusión de reportes locales de auditoría en `.gitignore`.
- Desarrollada una nueva versión del auditor de SineOS para diagnóstico ampliado.

### Pendiente actual

- Fijar versión/digest de Open WebUI, definir secret persistente y retirar `restart: unless-stopped` de forma controlada.
- Determinar consumidores de Tor.
- Validar Ollama desde otro equipo y revisar nftables frente a Podman/netavark.
- Auditar AppArmor y formalizar gestión de secretos.
- Implementar backups, snapshots y recuperación ante desastre.
- Definir actualización del CLI de Miyo y crear templates técnicos.

---

## [2026-09-19]

### Academic Knowledge System

Cierre funcional de la primera versión completa del sistema académico de SineOS.

Estado:

```text
Materia               OK
Unidad                OK
Tarea                 OK
Actividad              OK
Examen                 OK
Proyecto Integrador    OK
Etapa Proyecto         OK
```
