# SineOS — Roadmap maestro de pendientes

**Fecha de decisión:** 08-10-2026; **actualización explícita de prioridades:** 09-10-2026
**Estado:** vigente para priorización; modificaciones exclusivamente documentales.
**Seguimiento maestro:** [GitHub issue #4](https://github.com/ArgenisPadill/SineOS/issues/4)

## Regla de precedencia aprobada

1. **Seguridad:** terminar hardening pendiente y obtener evidencia real de los controles críticos.
2. **SineOS Desktop Experience (SDE):** ejecutar el diseño ya consolidado, certificarlo y recuperar si falla.
3. **Oracle Cloud + automatizaciones:** plan híbrido n8n local/externo y Minecraft opcional, sujeto a capacidad, costo cero, seguridad y recuperación; implementación **después de certificar SDE**.
4. **Resto de pendientes:** reproducibilidad → gestor modular SLDE → módulos ligeros → laboratorios aislados → cargas pesadas.

**A → B → C es el orden expresamente solicitado el 09-10-2026.** Las fases D en adelante conservan alcance, evidencia, riesgos y dependencias propias; ninguna deuda crítica para seguridad/SDE se aplaza por esta repriorización. No hay fechas comprometidas ni instalaciones autorizadas por este documento.

## Actualización de prioridad aprobada (09-10-2026)

- Nueva **fase C (Prioridad 3)**: [Oracle Cloud, n8n local/externo y Minecraft](../Architecture/Oracle-Cloud-n8n-Minecraft-Planning.md), [issue #5](https://github.com/ArgenisPadill/SineOS/issues/5).
- **La implementación no ha comenzado:** no se verificó consola OCI ni si existe VM; no se borró, instaló ni modificó infraestructura.
- Las fases antes C/D/E pasan ahora a **D/E/F** respectivamente; sus tareas y estados **no cambian**. La nueva precedencia es una decisión explícita posterior y se impone solamente para ordenar la ejecución futura, sin saltarse gates críticos anteriores.

## Regla de continuidad y preservación de acuerdos anteriores (08-10-2026)

**Todo lo que estaba planeado, documentado, congelado, aprobado, implementado o pendiente antes de la conversación del 08-10-2026 se mantiene tal como estaba.** Esta ampliación del roadmap es **aditiva**, no sustituye documentos anteriores, no altera el alcance técnico congelado de SDE, no modifica los 15 registros TD existentes ni cambia sus criterios de cierre, evidencia, dependencias o estado. Las certificaciones y decisiones técnicas anteriores siguen siendo válidas en el alcance en que fueron documentadas.

- El 08-10 se aprobó **Seguridad → SDE** y el 09-10 se añadió expresamente **Oracle/n8n/Minecraft como prioridad inmediata posterior a SDE**. Los gates y requisitos de Seguridad y SDE se conservan.
- Los proyectos y pendientes preexistentes **no se cancelan, eliminan, reinician, reemplazan, degradan ni se consideran concluidos** por incluirlos en este roadmap. Sus especificaciones y fuentes originales conservan autoridad.
- A partir del 09-10, **Oracle/n8n/Minecraft precede al resto posterior a SDE**; el orden de las iniciativas **después de Oracle** continúa como sugerencia organizativa, sin desplazar dependencias de seguridad/recuperación ni cambiar compromisos de cada tarea.
- El catálogo SLDE y los métodos de integración son **candidatos por estudiar**, no un listado obligatorio de instalaciones, soluciones escogidas ni compromisos de compatibilidad.
- Ante una duda futura se evaluará la necesidad real, factibilidad, ventajas, restricciones, seguridad, rendimiento, mantenimiento, costos/licencias, compatibilidad con SineOS y opciones equivalentes o mejores. El resultado posible incluye **adoptar, sustituir, adaptar, ejecutar remoto, posponer o descartar**, documentando el motivo y la alternativa.
- **No se modifica una decisión congelada ni se cierra un pendiente anterior por inferencia.** Si surge una propuesta que lo contradice, se documenta aparte y se solicita una decisión explícita antes de tocar la especificación original.
- La evaluación futura tampoco autoriza instalaciones o cambios de configuración por sí sola: se mantiene la regla de pruebas, backup, rollback y validación.

**Principio:** continuidad primero; las nuevas ideas amplían el inventario sin borrar historia, compromisos anteriores ni tareas abiertas.

## Situación al aprobar el roadmap

- Base Debian 13/XFCE, Podman rootless, apps nativas y servicios principales: funcionales según evidencia versionada.
- Backup, restore y DR: cuentan con pruebas certificadas anteriores. No equivale a verificar su estado físico actual.
- Seguridad: controles importantes cerrados; hardening restante en curso.
- SDE 1.0: planeación funcional y preparación técnica Alpha 0.1 consolidadas; implementación física **sin iniciar**.
- SLDE y sus 16 módulos: iniciativa nueva **planificada**, ningún componente nuevo instalado por este cambio.

## A · PRIORIDAD 1 — Seguridad (EN CURSO)

**Issue:** [#2 — Gate de seguridad](https://github.com/ArgenisPadill/SineOS/issues/2).
**Fuente de verdad:** [Security-Baseline](../Security/Security-Baseline.md), [Technical-Debt](Technical-Debt.md) y [estado global](../Lifecycle/15-Estado-actual.md).

- [ ] TD-010: auditar AppArmor con perfiles aplicados y evidencia.
- [ ] Verificar LUKS, cifrado de disco y posibilidad de recuperación; documentar si falta.
- [ ] Inventariar puertos efectivos con `ss -tulpn` y consumidores de cada servicio.
- [ ] TD-008: verificar reglas nftables, Podman/netavark y efecto de recargas con rollback.
- [ ] TD-009: verificar desde otra máquina exposición LAN de Ollama :11434.
- [ ] Comprobar y endurecer SSH **si** está activo; sin perder acceso legítimo.
- [ ] TD-011: identificar consumidores de Tor antes de decidir su permanencia.
- [ ] Revisar credenciales pendientes y rotaciones sin revelar secretos.
- [ ] Formalizar y probar snapshots/rollback Btrfs, diferentes de Restic.
- [ ] TD-024: automatizar y probar ownership de Uptime Kuma al restaurar sobre host limpio.
- [ ] Resolver o aceptar explícitamente el riesgo de TD-006/007 (imagen/restart Open WebUI) y TD-019 (permisos Stirling PDF).
- [ ] TD-018: pasar la auditoría defensiva asistida por agente **después** del hardening tradicional, con allowlist, evidencia y revalidación.
- [ ] Registrar evidencia de host real, rollback y cualquier riesgo aceptado; revalidar servicios afectados.

**Gate de salida:** no basta con marcar casillas ni actualizar Markdown; se requieren pruebas del host, recuperación disponible y ausencia de riesgos críticos no aceptados. El cierre del gate habilita trabajar físicamente en SDE, pero no lo certifica.

## B · PRIORIDAD 2 — SDE 1.0 (PLANEACIÓN TERMINADA; IMPLEMENTACIÓN PENDIENTE)

**Issue:** [#1 — SDE](https://github.com/ArgenisPadill/SineOS/issues/1).
**Fuentes:** [roadmap específico](../Architecture/SDE-Implementation-Roadmap.md) y [Definition of Done](../Architecture/SDE-Definition-of-Done-1.0.md).

- [x] Congelar diseño funcional SDE 1.0, decisiones UX, requisitos de recovery, especificaciones Alpha 0.1 y criterios C0–C12.
- [ ] Autorizar inicio de Alpha 0.1 **sólo después** del gate A.
- [ ] Inventario real pre-SDE, backup local seguro, verificación SHA-256, dry-run y rollback probado.
- [ ] Implementación controlada: sesión/login, escritorio visual, displays, red/dispositivos, privacidad, impresión, salud, configuración y launcher, siguiendo fases específicas de SDE.
- [ ] Certificación final en hardware de referencia C0–C12, rendimiento, rollback, desinstalación y release reproducible.
- [ ] Registrar riesgos y elementos diferidos a SDE 1.1 sin declararlos entregados.

**Aclaración:** el script XFCE reproducible y el DR ya validados no significan que SDE 1.0 esté instalado o certificado.

## C · PRIORIDAD 3 — Oracle Cloud + n8n + Minecraft (PLANIFICADO; POST-SDE)

**Issue:** [#5 — Oracle / n8n / Minecraft](https://github.com/ArgenisPadill/SineOS/issues/5). **Diseño:** [plan de arquitectura](../Architecture/Oracle-Cloud-n8n-Minecraft-Planning.md).

- [ ] Finalizar gates A y B; no comenzar instalaciones antes de certificar SDE 1.0.
- [ ] Inventariar cuenta e infraestructura OCI previamente usada para Minecraft: VM (si existe), región, cuota Always Free, volúmenes, red, IP, reglas y facturación. **No borrar recursos por defecto.**
- [ ] Confirmar factibilidad de alojamiento externo gratuito 24/7 (sin SLA garantizado); si no hay capacidad, registrar bloqueo y alternativas sin asumir pagos.
- [ ] Diseñar dos instancias aisladas: **n8n local** en Podman SineOS para Ollama/Obsidian/segundo cerebro; **n8n externo** en OCI para webhooks, correo, Telegram, WhatsApp mediante API y apps web.
- [ ] Evaluar el alojamiento separado de Minecraft Java en la misma VM, con límites de recursos y prioridad de servicio para n8n.
- [ ] Validar licencias: n8n Community gratuito pero **fair-code, no OSI open source**; comparar opción OSI si procede. Verificar costos externos de APIs y cuota OCI.
- [ ] Implementar **sólo después de una decisión técnica**: acceso seguro, TLS, firewall de OCI+host, secretos, backup externo, restore probado, monitoreo, pruebas de disponibilidad y riesgo aceptado.

**Estado actual:** decisión y backlog documentados; no existe confirmación de VM operativa ni despliegue de n8n o Minecraft.

## D · PRIORIDAD 4 — Reproducibilidad y deuda operativa restante (PENDIENTE; POST-ORACLE)

Las 15 TD vigentes se mantienen **exclusivamente** en [Technical-Debt](Technical-Debt.md), no se renumeran ni cierran aquí. Algunas TD de seguridad se priorizan en A; las no críticas quedan ordenadas después de SDE.

- [ ] Instalación integral reproducible de SineOS sobre Debian 13 limpio, distinta de DR certificado.
- [ ] Inventario global versionado de dependencias y matriz de compatibilidad.
- [ ] Procedimiento integral de actualización, rollback y troubleshooting general por capas.
- [ ] TD-015: formalizar procedimiento de migración.
- [ ] Instalación reproducible de Podman Desktop, Obsidian y Miyo.
- [ ] Documentar instalación, servicios/timers de monitoreo y ruleset nftables saneado; no publicar secretos.
- [ ] TD-025: portabilidad del auditor `sineos-audit.sh` y detección dinámica de raíz.
- [ ] TD-014: revisar `apt autoremove --dry-run`, sin eliminación automática.
- [ ] TD-012: actualizar Miyo CLI/AppImage con rollback.
- [ ] TD-013: benchmark semántico multinota de Miyo.
- [ ] TD-017: templates técnicos Incidencia / Procedimiento / ADR del Vault.
- [ ] Completar runbooks específicos del auditor, firewall, Stirling PDF, Uptime Kuma y Open WebUI.

**Regla:** si un pendiente resulta ser necesario para seguridad, disponibilidad o un gate SDE, se adelanta a A/B y no espera esta fase.

## E · PRIORIDAD 5 — SLDE base modular (PLANIFICADO; POST-D)

**Issue:** [#3 — SLDE](https://github.com/ArgenisPadill/SineOS/issues/3). **Diseño:** [SLDE-Planning](../Architecture/SLDE-Planning.md).

- [ ] Congelar alcance, política de seguridad, matriz nativo / Podman / VM / remoto y presupuesto de recursos.
- [ ] Diseñar manifiestos por herramienta, catálogo sin duplicaciones y detección del software instalado.
- [ ] Prototipo ligero de SineOS LaboratoryManager, sin demonios residentes innecesarios.
- [ ] Gate de instalación opcional: requisitos, estado, pruebas, backup/restore, desinstalación y rollback.
- [ ] Piloto con herramienta sencilla, mediciones reales y recuperación validada.

## F · PRIORIDAD 6 — Despliegue gradual de los 16 módulos SLDE (PENDIENTE)

- [ ] E1: Desarrollo (04), Matemáticas/Estadística (09), Ofimática (11), Certificaciones (15).
- [ ] E2: Bases de Datos (03), Ingeniería de Software (05), Comunicación (12).
- [ ] E3: Redes (01), Sistemas Operativos (02), Ciberseguridad (06), Cloud/DevOps (07), Virtualización/Servidores (08), Electrónica/Hardware (10).
- [ ] E4: Ciencia de Datos (13), Procesamiento de Imágenes (14), IA Local ampliada (16).

Los módulos se instalan **bajo demanda**. Los laboratorios privilegiados, la seguridad ofensiva y las cargas GPU se aíslan o se derivan a máquinas remotas cuando corresponda.

## Fuentes de verdad y cambios de estado

| Información | Fuente principal |
|---|---|
| Orden de proyectos e iniciativas | Este roadmap + issue #4 |
| Estado global validado | `Documentation/Lifecycle/15-Estado-actual.md` |
| Deuda técnica real (TD) | `Documentation/Operations/Technical-Debt.md` |
| Riesgos y gate de seguridad | `Documentation/Security/Security-Baseline.md` + issue #2 |
| SDE | Issue #1 y `Documentation/Architecture/SDE-*.md` |
| Oracle / n8n / Minecraft (prioridad 3) | Issue #5 y `Documentation/Architecture/Oracle-Cloud-n8n-Minecraft-Planning.md` |
| SLDE | Issue #3 y `Documentation/Architecture/SLDE-Planning.md` |
| Historial de cambios | `CHANGELOG.md` |

No confundir «planificado», «implementado», «validado» y «certificado». Los cierres reales requieren evidencia y actualización documental coherente. No se alteran sistemas, credenciales, imágenes, servicios ni datos durante este registro.
