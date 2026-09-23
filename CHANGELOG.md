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

### Automatización y organización

- La automatización visual de XFCE se trasladó a `Scripts/Desktop/`.
- La documentación visual se trasladó a `Documentation/Operations/XFCE-Visual-Configuration.md`.
- La aplicación NetworkPrivacy permanece en `Apps/NetworkPrivacy/`; su instalación e integración de escritorio se automatiza desde `Scripts/NetworkPrivacy/`.


### Documentación

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

### Pendiente

- Sustituir el arranque temporal de PostgreSQL por Quadlet definitivo.
- Corregir y validar la red del Quadlet de PostgreSQL.
- Formalizar política de firewall.
- Fijar versión o digest de Open WebUI.
- Formalizar gestión de secretos.
- Definir mecanismo de actualización del CLI de Miyo.
- Implementar estrategia completa de snapshots, backup y recuperación.
- Crear templates técnicos para Incidencias, Procedimientos y ADR.
- Continuar benchmarks semánticos entre múltiples notas.

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
