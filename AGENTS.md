# Instrucciones de trabajo para agentes en SineOS

**Norma principal:** [Lineamiento general de ingeniería y entregas verificables](Documentation/Architecture/Engineering-Delivery-Standard.md). Aplica a todo el repositorio, no solo a SDE o Office.

## Regla de oro

> **Cada cambio debe entregar valor, demostrarse con pruebas y ser reversible de manera proporcional a su riesgo antes de continuar.**

- **Diagnosticar antes de intervenir.** Consultar estado real, dependencias, prioridad y la documentación pertinente. Si no existe evidencia, informar incertidumbre.
- **Seguir el roadmap y los gates vigentes:** Seguridad → SDE → Oracle/n8n/Minecraft → reproducibilidad → SLDE. No interpretar una instrucción de planeación como permiso para ejecutar.
- **Trabajar por incrementos pequeños y coherentes.** Evitar cambiar varios subsistemas por conveniencia. No avanzar con regresiones conocidas; corregir o revertir.
- **Proteger el último estado funcional.** Para cambios de alto riesgo, contar con recuperación viable y probarla cuando corresponda. No destruir datos, credenciales, respaldos, volúmenes, historial Git o sesiones con documentos sin autorización explícita.
- **Probar de verdad.** Registrar PASS/FAIL/PENDING con evidencia. Una prueba simulada o informe de un agente no certifica hardware, servicios reales ni la experiencia de usuario.
- **Mantener la documentación vigente y saneada.** No publicar secretos, `.env`, llaves, licencias, respaldos, imágenes de VM, logs privados o datos personales.
- **Preservar decisiones congeladas.** SineOS Office es un piloto local operativo **no certificado ni completamente integrado**. Su congelamiento y los estados de SDE/SDE Alpha no se alteran por inferencia.
- **Antes de publicar:** revisar cambios, referencias, privacidad, pruebas y estado del repositorio; no inventar cierres de issues ni alterar el roadmap.
- **La IA acelera el trabajo, no concede autorización.** Solicitar decisión explícita antes de ejecutar cambios con impacto operativo fuera del alcance ya autorizado.

## Biblioteca de skills del proyecto

## Trabajo multiagente: planeado, no activado

- **Propuesta vigente:** [Arquitectura y plan multiagente para Codex](Documentation/AI/Multiagent-Codex-Planning.md) · [pendiente #11](https://github.com/ArgenisPadill/SineOS/issues/11).
- **Esta referencia NO autoriza lanzar subagentes de manera automática.** Solo delegar cuando el usuario solicite expresamente un trabajo multiagente o apruebe una sesión futura concreta con su alcance y sus límites de permisos.
- El piloto futuro prevé **1 coordinador + hasta 3 subagentes** con tareas independientes de Seguridad, Arquitectura y QA. Sin compartir escritura, Git, servicios ni recursos mutables; coordinar resultados y comprobar evidencias antes de cualquier adopción.
- **Importante:** los agentes heredan el sandbox y las aprobaciones del coordinador; un rol que diga «solo lectura» **no** crea aislamiento real. No modificar `.codex/config.toml`, `~/.codex/config.toml`, crear roles, instalar plugins ni ejecutar pruebas sin autorización posterior.
- La implementación queda **PENDIENTE** y subordinada al gate de Seguridad, al roadmap y a la regla de ingeniería. Office sigue congelado.

- **Catálogo verificado de candidatos externos:** [Documentation/AI/Agent-Skills/README.md](Documentation/AI/Agent-Skills/README.md), [catálogo curado](Documentation/AI/Agent-Skills/External-Catalog-2026-10-22.md) y [protocolo de evaluación](Documentation/AI/Agent-Skills/Skill-Adoption-Protocol.md).
- **Skills nativas de SineOS para Codex:** `.agents/skills/sineos-security-triage/`, `.agents/skills/sineos-systematic-debugging/`, `.agents/skills/sineos-verify-delivery/` y `.agents/skills/sineos-third-party-skill-review/`. Usar solo cuando la tarea corresponda; no invocarlas todas automáticamente.
- **Distinción obligatoria:** skills SineOS versionadas = disponibles para descubrimiento del agente **tras sincronizar localmente**; candidatos externos = únicamente enlaces de investigación, **no instalados ni autorizados**. Requieren revisión de seguridad y aprobación antes de añadir scripts, plugins o MCP.
- **Sin privilegios nuevos:** una skill no permite eludir los gates de Seguridad, ejecutar sobre Debian sin permiso, publicar secretos, ni descongelar el piloto Office.

El detalle del contrato de trabajo, los niveles de riesgo y los criterios de aceptación están en el estándar enlazado. Los estándares más específicos de cada componente, las políticas de seguridad y sus gates siguen aplicando íntegramente.
