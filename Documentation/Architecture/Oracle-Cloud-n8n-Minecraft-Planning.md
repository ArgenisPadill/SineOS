# SineOS — Oracle Cloud, automatizaciones n8n y Minecraft

**Decisión de planificación:** 2026-10-09  
**Estado:** PLANIFICADO / NO IMPLEMENTADO / SIN INVENTARIO ACTUAL DE OCI  
**Prioridad global:** **3.ª**, sólo después de **1. Seguridad** (gate #2) y **2. SineOS Desktop Experience 1.0** (SDE, issue #1), y antes de la cola posterior de reproducibilidad y SLDE.  
**Seguimiento:** [issue #5](https://github.com/ArgenisPadill/SineOS/issues/5) · [roadmap maestro](../Operations/Project-Roadmap.md).

> Este documento no autoriza crear, destruir, reinstalar o publicar servicios. Su función es conservar requisitos, hipótesis, decisiones y pruebas pendientes. No cambia la planeación congelada de SDE ni el estado de la deuda técnica.

## 1. Objetivo y restricciones

Diseñar infraestructura híbrida para automatizaciones y ocio:
- **n8n local** en SineOS (Debian 13/Podman rootless), para automatizaciones del propio equipo, laboratorio, Ollama, Obsidian y Knowledge Vault/segundo cerebro, sin exponer información local por defecto.
- **n8n externo** alojado independientemente de SineOS, para correo, Telegram, WhatsApp por proveedores/API aprobados, aplicaciones web, salidas HTTP(S) y recepción de webhooks en internet.
- **Minecraft Java** opcional en la **misma VM** OCI, aislado con contenedor/unidad, recursos limitados y ciclo de vida independiente. La disponibilidad de n8n tiene prioridad cuando compitan por CPU/RAM.
- Se desea **24/7/365** para los flujos externos, incluso si la laptop está apagada. Es un **objetivo**, no una promesa de SLA ni de continuidad garantizada de Always Free.
- **Presupuesto de alojamiento deseado: cero**. Evitar Hostinger, VPS de pago y licencias recurrentes. Revisar de manera independiente posibles tarifas de WhatsApp, correo, dominios/DNS, tráfico y otros proveedores.
- Preferencia por tecnologías gratuitas y **open source** cuando existan; considerar licencias reales antes de adoptar cada componente.

### Precisión de licencia

**n8n Community self-hosted es gratuito para usos permitidos, pero su Sustainable Use License es «fair-code/source-available», no una licencia open source certificada por OSI.** Evaluar las restricciones si cambia el caso de uso, se ofrece la plataforma a terceros o se habilita edición de flujos por clientes. Si open source OSI resulta requisito obligatorio, evaluar **Node-RED** u opciones compatibles antes de decidir. No confundir costo cero con licencia OSI.

Referencias: [licencia de n8n](https://support.n8n.io/article/can-i-use-your-license-for-my-use-case), [documentación de n8n](https://docs.n8n.io/hosting/).

## 2. Arquitectura lógica candidata (sujeta a inventario y pruebas)

```text
Laptop SineOS (local, puede estar apagada)
  ├─ n8n local (Podman rootless; sólo localhost/LAN autorizada)
  ├─ Ollama / IA local
  ├─ Obsidian / Knowledge Vault (sin compartir indiscriminadamente)
  └─ datos y backup locales separados

                     INTERNET
                         │
               DNS + TLS (candidato)
                         │
         OCI Always Free: VM Linux (candidato ARM64)
           ├─ reverse proxy HTTPS: Caddy (candidato)
           │    └─ n8n externo: webhooks, integraciones, editor restringido
           ├─ PostgreSQL externo: sin puerto público
           ├─ Minecraft Java: servicio/contenedor independiente
           │    └─ puerto de juego TCP 25565 SÓLO si se autoriza
           └─ firewall/ACL, backup, monitorización, cuotas, alertas
```

- El almacenamiento, red, credenciales, claves de cifrado y datos de las dos instancias n8n serán **independientes**.
- **Podman/Quadlet** y PostgreSQL se consideran candidatos coherentes con SineOS; validar soporte de la distribución elegida, imágenes multi-arquitectura ARM64, actualizaciones y comportamiento de servicios persistentes.
- Para webhooks de terceros considerar HTTPS en 443; el editor y las páginas administrativas **no deben quedar expuestos sin protección**. Preferir red privada o acceso restringido para administración. SSH sólo por llave y fuentes autorizadas.
- Minecraft puede escuchar TCP 25565, sujeto a decisión posterior; aplicar listas de acceso/protecciones, límites de CPU/RAM y políticas de backup. No mezclar sus volúmenes con n8n.
- Workflows que dependen de Ollama/Obsidian locales **no pueden ejecutar esas etapas con la laptop apagada**. Deben desacoplarse mediante colas, reintentos y manejo de indisponibilidad; no abrir puertos locales a internet para «resolver» esa limitación.
- La topología final puede requerir **separar Minecraft de n8n** si las pruebas de recursos, latencia o seguridad lo aconsejan.

## 3. Oracle Cloud: hechos, incertidumbres y riesgo de costo

**Antecedente histórico, no verificación actual:** el 2026-08-25 se preparó un proyecto Minecraft en Oracle Cloud (región Querétaro; VCN/subred pública) y se intentó crear una VM **VM.Standard.A1.Flex** con **2 OCPU/12 GB**; la creación falló por **falta de capacidad**. **No está confirmado que hoy exista una VM encendida.** Sólo se sabe que se avanzó en preparativos de red.

Según [Oracle Always Free, versión consultada 2026-10-09](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm), el uso gratuito de Ampere A1 corresponde a **1,500 horas OCPU/mes y 9,000 GB-horas/mes**, equivalente en una tenencia Always Free a **2 OCPU y 12 GB de RAM**; estas cantidades son una **cuota**, no recursos ya asignados ni capacidad asegurada. Revisar además almacenamiento combinado de boot/block volumes, backups, IPs, región de origen, tráfico y vigencia de condiciones antes de provisionar.

**Política de preservación:** si hay VM Always Free útil, **no eliminarla por querer «empezar de cero»**: quizá no se pueda recuperar capacidad. Preferir respaldar/inventariar y reconstruir servicios en aislamiento. Si sólo existe infraestructura de red, planear su limpieza cuando esté documentado qué se conservará. Nunca efectuar borrados «a ciegas».

**Política de costo:** inventariar el tipo de cuenta y recursos cobrables, establecer presupuestos/alertas/cuotas, revisar el costo estimado de *cada* recurso y mantener un punto de aprobación si implica pasar a pago. «Always Free» no equivale a garantía 24/7 ni cubre automáticamente proveedores terceros.

## 4. Secuencia de ejecución aprobada (no iniciada)

### Gate 0 — Dependencias del roadmap
- [ ] Cerrar gate de **seguridad** con evidencia y recuperación, según issue #2.
- [ ] Implementar y **certificar SDE 1.0** según Definition of Done C0–C12, issue #1.
- [ ] **Sólo entonces** habilitar la ejecución de la presente iniciativa (issue #5). La planeación documental no inicia ni bloquea trabajos actuales.

### Gate 1 — Inventario y decisión OCI (desde equipo con consola)
- [ ] Verificar acceso a la cuenta sin almacenar contraseñas/tokens en GitHub.
- [ ] Comprobar si existe VM, estado, shape, ARM64/x86, imagen, OCPU/RAM, boot volume, IP, compartment, región de origen, AD, VCN, subnet, NSG/Security List y reglas efectivas.
- [ ] Auditar recursos «ocultos» con potencial de cobro, límites disponibles y factura/uso; registrar resultados **sin revelar identificadores sensibles**.
- [ ] Decidir conservar VM y rehacer servicios, recrear recursos concretos o posponer por falta de capacidad; registrar justificación y plan de reversión.

### Gate 2 — Diseño técnico, seguridad y licencias
- [ ] Registrar un ADR: elección de SO soportado, imágenes ARM64 y versiones fijadas, rootless/rootful justificado, red y acceso, límites y monitoreo.
- [ ] Confirmar licencia de n8n para el uso real o seleccionar alternativa OSI si cambia el requisito.
- [ ] Segregar editor n8n, webhooks, BD y Minecraft; exponer exclusivamente los puertos indispensables.
- [ ] Diseñar firewall en **ambas capas** (OCI NSG/Security List y host), gestión de claves SSH, actualizaciones, cuentas mínimas, secretos/volúmenes con permisos estrictos y rotación.
- [ ] Evaluar DNS, certificados automáticos HTTPS, restricciones de proveedor para webhook de WhatsApp/Telegram, reglas de egress y costos potenciales.
- [ ] Definir RAM/CPU máximos, prioridad para n8n, política de Minecraft on-demand/limitado e impacto real de tener varios servicios en una sola VM.

### Gate 3 — Continuidad, recuperación y pruebas
- [ ] Definir y probar **backup cifrado fuera de la propia VM** de workflows, BD, configuración y **clave maestra de cifrado n8n**; documentar restauración y rotación segura.
- [ ] Respaldar mundo/configuración Minecraft por separado; ejecutar restore de prueba.
- [ ] Monitorizar disponibilidad, disco, RAM, CPU, reinicios, errores de flujos, certificados y consumo OCI; alertar sin depender exclusivamente de la VM bajo fallo.
- [ ] Probar webhooks entrantes, salidas de correo/Telegram/WhatsApp según permisos, TLS, DNS, reboots, caída de SineOS local, límites Minecraft, pérdida de red y reintentos.
- [ ] Medir uso real y comprobar **costo no facturable**; establecer objetivos RPO/RTO realistas y procedimiento de migración a otra infraestructura si la capa gratuita deja de ser suficiente.
- [ ] Desplegar por etapas, registrar incidentes y resultados; **no marcar como «operativo 24/7» sin datos**.

## 5. Relación con otros pendientes de SineOS

1. **Prioridad 1:** Seguridad actual — no se altera ni se «hereda» su validación a OCI.
2. **Prioridad 2:** SDE — su alcance congelado permanece intacto.
3. **Prioridad 3:** Este proyecto híbrido Oracle + n8n local/externo + Minecraft — nuevo, pendiente.
4. **Después:** Reproducibilidad, deuda operativa restante, base SLDE y sus 16 módulos, conforme al roadmap y dependencias de riesgo.

Excepción: una tarea ya abierta que sea requisito imprescindible para **seguridad, recuperación o SDE** conserva su prioridad de gate. No se reabren/cancelan TD ni se convierten ideas en instalaciones. Mantener trazabilidad en issue #5 y estado global.

## 6. Definición de terminado (futura)

La iniciativa sólo se considerará validada si existe: inventario OCI verificable; arquitectura y licencia aprobadas; instancias aisladas; acceso HTTPS seguro; n8n local y externo probados; Minecraft opcional sin degradación inaceptable de automatizaciones; respaldos y restauración **realmente ejecutados**; monitoreo y límites; evaluación documentada de costo/riesgos. El calificativo **«24/7 garantizado» no corresponde a OCI Always Free**.

**Estado al 2026-10-09:** documentación y backlog exclusivamente. No se ha entrado a Oracle, ni validado VM, ni instalado n8n o Minecraft en esta sesión.
