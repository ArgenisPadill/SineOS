# SineOS — Política de evolución y compatibilidad tecnológica

**Decisión autorizada:** 11-10-2026  
**Estado de la directriz:** ADOPTADA / DOCUMENTADA  
**Estado de implementación:** DIFERIDA; ningún componente, lenguaje o framework nuevo queda autorizado para instalación o sustitución  
**Alcance:** SineOS Core, seguridad, recuperación, SDE, servicios, IA, automatizaciones y SLDE  
**Autoridad de prioridades:** [Roadmap maestro](../Operations/Project-Roadmap.md)

## 1. Propósito

Establecer una política duradera para que SineOS pueda evaluar avances en lenguajes, compiladores, runtimes, interfaces gráficas, inteligencia artificial, sistemas de contenedores, estándares y hardware sin perder su identidad ni deteriorar su operación.

> **La tecnología debe adaptarse a las necesidades de SineOS; SineOS no debe adaptarse automáticamente a las tendencias tecnológicas.**

Evolucionar no exige reemplazar: puede significar ampliar, integrar, optimizar, aislar o conservar lo existente. Una tecnología nueva no es una justificación suficiente para alterar un sistema funcional.

## 2. Decisión y alcance temporal

Esta política rige desde ahora como **criterio para tomar decisiones futuras**, pero **su implementación técnica queda diferida hasta concluir los compromisos de trabajo ya establecidos y contar con una base estable, reproducible y recuperable**. No existe fecha comprometida, instalación aprobada ni obligación de adoptar alguno de los candidatos.

Se preserva **íntegramente** la precedencia del roadmap: **A Seguridad → B SDE 1.0 → C Oracle Cloud/n8n/Minecraft → D Reproducibilidad y deuda operativa → E SLDE base → F módulos SLDE**, más sus dependencias, gates y criterios particulares. Esta política no crea una nueva prioridad intermedia ni desplaza fases o deuda ya aprobadas.

La valoración de compatibilidad puede registrarse documentalmente cuando sea útil; no habilita por sí sola pruebas sobre el host principal, implementaciones, cambios de configuración, nuevas dependencias, servicios ni migraciones. Cualquier ejecución futura requerirá autorización específica.

### Preservación de decisiones congeladas

- No reabrir o alterar el diseño aprobado de SDE 1.0, sus contratos de experiencia de usuario ni su estrategia de recuperación.
- No sustituir o reescribir aplicaciones ya funcionales como NetworkPrivacy y Mantenimiento por preferencia de lenguaje.
- No alterar la política de recuperación, secretos, firewall, backups y contenedores sin una decisión explícita y evidencia correspondiente.
- No cancelar, renumerar ni dar por cerrados los pendientes anteriores como consecuencia de esta política.
- Si una propuesta entra en conflicto con una especificación congelada, registrarla **por separado** y solicitar aprobación expresa antes de cambiar su fuente de verdad.

## 3. Invariantes de SineOS

Una incorporación futura deberá conservar o mejorar, con evidencias:

1. **Funcionalidad y estabilidad:** comportamiento verificable, compatibilidad hacia atrás cuando aplique y ausencia de regresiones críticas.
2. **Seguridad y privacidad:** mínimo privilegio; secretos fuera del repositorio; control explícito de exposición de red, datos y telemetría.
3. **Recursos proporcionados:** consumo de CPU, RAM, disco, batería y arranque adecuado al hardware real; evitar daemons innecesarios.
4. **Reproducibilidad:** instalación, construcción, actualización y configuración documentadas, fijación verificable de versiones y cadena de suministro.
5. **Recuperabilidad:** backup cuando corresponda, rollback probado, desinstalación limpia y último estado funcional recuperable.
6. **Modularidad razonable:** capacidades opcionales aislables, sin convertir una herramienta experimental en dependencia del camino crítico.
7. **Autonomía y mantenibilidad:** evitar bloqueo innecesario con proveedores, dependencias opacas o soluciones sin un ciclo de mantenimiento sostenible.
8. **Usabilidad:** las mejoras internas no deben complicar injustificadamente la experiencia cotidiana ni introducir procedimientos frágiles.

No se exige abstracción universal. **Se introducen contratos estables solo cuando exista una necesidad concreta de desacoplar** dos componentes.

## 4. Estrategia de compatibilidad y sustitución controlada

En los componentes donde corresponda, favorecer interfaces públicas pequeñas y verificables: CLI, códigos de salida, JSON/esquemas versionados, archivos de configuración documentados, APIs o D-Bus cuando sea adecuado. Son opciones, **no una pila tecnológica obligatoria**.

Antes de cambiar una implementación:

- Definir el contrato de entrada, salida, errores, permisos y efectos secundarios.
- Conservar pruebas de regresión y casos de compatibilidad de la implementación actual.
- Permitir coexistencia o sustitución reversible cuando el costo y el riesgo lo justifiquen.
- Asegurar que una falla del componente opcional no impida arrancar, operar o recuperar el sistema.
- Evitar migraciones de datos o cambios de esquema irreversibles sin respaldo y rollback comprobado.
- Documentar ruptura de compatibilidad, alternativa y procedimiento de retorno si existiera una razón excepcional para introducirla.

La adopción nunca se basa exclusivamente en benchmarks sintéticos o popularidad del lenguaje: el costo de mantenimiento, seguridad, empaquetado y soporte cuenta tanto como el rendimiento.

## 5. Proceso para evaluar una tecnología futura

**Gate 0 — Elegibilidad:** respetar prioridades previas y constatar una base estable certificada antes de cualquier incorporación técnica amparada por esta iniciativa.

1. **Necesidad demostrable:** especificar el problema concreto y la limitación de la solución existente.
2. **Alternativas:** contrastar no hacer nada, mejorar lo actual, integrar una biblioteca o utilizar otra tecnología.
3. **Viabilidad:** revisar compatibilidad con Debian y hardware objetivo, mantenimiento upstream, licencia, apertura del código cuando sea relevante, dependencias, suministros y soporte.
4. **Prueba aislada y autorizada:** realizar prototipo acotado fuera del entorno productivo, sin privilegios extra ni exposición de red por defecto.
5. **Evidencia:** medir rendimiento real, consumo, seguridad, pruebas funcionales, portabilidad, esfuerzo de implementación y costo de mantenimiento.
6. **Decisión explícita:** adoptar, adaptar, integrar parcialmente, sustituir, posponer o descartar; registrar motivos, riesgos y alternativas mediante ADR/documento equivalente.
7. **Integración controlada si se aprueba:** versionado, instalador reproducible, validación, monitoreo, manuales, rollback, desinstalación y actualización documental.

Ninguna fase se considera implementada o validada únicamente por existir documentación o una prueba aislada.

## 6. Tecnologías observadas (candidatos, no dependencias)

El listado es un inventario de investigación sujeto a revisión: **Rust, Mojo, Zig, Gleam, Odin, MoonBit, Hare, Carbon y Koka**, además de cualquier estándar, runtime o tecnología que surja posteriormente.

Áreas a observar sin compromiso de uso:

| Tecnología | Posible línea de estudio | Decisión actual |
|---|---|---|
| Rust | Herramientas CLI, validadores y utilidades nativas seguras | Candidato futuro |
| Zig | Interoperabilidad con C y compilación de utilidades de bajo nivel | Evaluación eventual |
| Mojo | Cómputo numérico y optimización local de IA | Investigación condicionada a hardware/benchmarks |
| Gleam | Servicios concurrentes y distribuidos | Solo si surge caso específico |
| Odin | Gráficos, datos y software nativo | Sin caso justificado |
| MoonBit | Componentes portátiles WebAssembly | Solo con necesidad de Wasm |
| Hare | Herramientas de sistemas estilo Unix | Sin caso justificado |
| Carbon | Evolución de código C++ | No aplicable actualmente |
| Koka | Investigación en tipado de efectos | Investigación, no producción |

Esta tabla **no es una aprobación de instalación, compatibilidad, madurez definitiva, reemplazo de Bash/Python/C/C++ ni un ranking permanente**.

SLDE ya contempla un módulo de Desarrollo. Si en el futuro se ofrecen toolchains opcionales, deberá utilizarse el catálogo y aislamiento previstos para SLDE, sin duplicar infraestructuras ni convertir esos toolchains en requisitos del sistema base.

## 7. Lo que esta política no autoriza

- Reescribir SineOS, el kernel, XFCE, SDE o las herramientas actuales para utilizar un lenguaje nuevo.
- Crear ahora un framework universal, runtime de plugins, daemon de compatibilidad o más capas abstractas sin necesidad probada.
- Instalar simultáneamente los nueve toolchains ni mantener procesos residentes que no aporten funciones.
- Sustituir Ollama, Miyo, Open WebUI, Podman o GTK por simple novedad tecnológica.
- Comprometer fechas de entrega, resultados de rendimiento, licencias compatibles o portabilidad sin verificarlos.

## 8. Criterios para considerar exitosa una futura incorporación

Se requiere como mínimo: problema resuelto; pruebas funcionales y de regresión; seguridad y permisos revisados; impacto CPU/RAM/disco medido; dependencias controladas; actualización y recuperación comprobadas; documentación vigente; aceptación expresa y ausencia de regresiones en los componentes existentes.

La posibilidad de **rechazar una tecnología y mantener el sistema actual** es un resultado válido y deseable cuando la propuesta no demuestra una mejora suficiente.

## 9. Relación con fuentes de verdad

- [Roadmap maestro](../Operations/Project-Roadmap.md): orden, dependencias, pendientes y gates.
- [SDE](SineOS-Desktop-Experience.md): diseño congelado del escritorio.
- [SLDE](SLDE-Planning.md): herramientas opcionales y laboratorios futuros.
- [Aplicaciones nativas](Native-Applications.md): estándar operativo actual Python 3 + GTK3/PyGObject.
- [Documentación](Documentation-Standard.md): documentación, evidencia y definiciones de terminado.
- [Deuda técnica](../Operations/Technical-Debt.md): pendientes existentes; esta política no los modifica.

**Estado al 11-10-2026:** decisión arquitectónica documentada, sin implementación técnica, sin instalación de dependencias, sin modificaciones del host o servicios y sin cambio de prioridades.
