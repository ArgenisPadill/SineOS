# SineOS — Lineamiento general de ingeniería y entregas verificables

**Decisión adoptada:** 22-10-2026  
**Estado:** VIGENTE / OBLIGATORIO para nuevas intervenciones en SineOS  
**Ámbito:** SineOS Core, Debian/XFCE, SDE, SLDE, aplicaciones nativas, scripts, contenedores, bases de datos, redes, seguridad, automatización, IA, Office experimental, integración externa, migraciones, documentación y recuperación.  
**Naturaleza:** norma transversal de **cómo** trabajar; no añade una fase ni autoriza la ejecución de un pendiente.

## Regla fundamental

> **Cada cambio de SineOS debe entregar un avance útil, tener pruebas que demuestren su funcionamiento y permitir volver de forma controlada al último estado funcional antes de continuar.**

En términos operativos: **pensar → planear → preparar → construir → revisar → probar → recuperar/verificar reversión → documentar → aceptar**.

Esta norma no exige que una gran iniciativa esté terminada para poder aprovechar sus componentes ya aceptados. Favorece entregas incrementales, pequeñas y coherentes, sin convertir una demostración parcial en una certificación completa.

## Principios obligatorios

1. **Incrementalidad con propósito.** Dividir trabajos amplios en incrementos verificables con alcance claro y beneficio identificable. No mezclar cambios independientes o de distinta exposición al riesgo. No producir cambios cosméticos sin valor para satisfacer una cuota de entregas.
2. **Estado de referencia.** Antes de intervenir, conocer el estado efectivo, las dependencias, el resultado esperado y los mecanismos existentes de protección/recuperación. Si el estado es incierto, empezar por diagnóstico **de solo lectura**.
3. **Seguridad por diseño y mínimo privilegio.** Proteger datos, credenciales, red, servicios y sesiones. Jamás subir secretos, respaldos privados, discos de VM o logs crudos al repositorio. No desactivar defensas para facilitar una prueba.
4. **Reversibilidad proporcional al riesgo.** Los cambios de configuración, infraestructura, almacenamiento, seguridad, cuentas, kernel, escritorio, servicio o VM requieren un procedimiento de reversión o recuperación probado **antes** de ejecutarse. Los cambios triviales solo documentales requieren revisión y la posibilidad normal de revertir el commit; no necesitan una restauración física.
5. **Pruebas basadas en evidencia.** Separar comprobaciones estáticas y simuladas de pruebas sobre el sistema real. Definir un criterio de aceptación por cambio y verificar tanto la función nueva como las existentes que puedan verse afectadas. No declarar PASS por intención, por haber escrito código o porque un agente diga haber terminado.
6. **No avanzar sobre una regresión.** Si un cambio falla, detener la cadena, diagnosticar, corregir o revertir antes de continuar. No encadenar arreglos improvisados sobre un sistema incierto.
7. **Fallback funcional.** Preferir que el estado conocido y operativo permanezca disponible mientras se incorpora una función nueva. Una mejora parcial no debe bloquear el uso normal de SineOS.
8. **Documentación contemporánea.** Versionar decisiones, dependencias, configuración reproducible, pruebas, límites, riesgos, rollback y pendientes; separar claramente **propuesto, experimental, operativo, validado y certificado**.
9. **Aprobación explícita de intervenciones.** Una propuesta, issue, diseño, investigación, borrador, prueba estática o instrucción a un agente **no es permiso** para cambiar la laptop ni infraestructura externa. Confirmar autorización y alcance especialmente ante operaciones destructivas, acceso a secretos o cambios que alteren decisiones congeladas.
10. **Mejora medida y sobriedad técnica.** Comparar consumo, complejidad, mantenimiento, latencia y resultados cuando sean relevantes. No introducir dependencias, procesos residentes o automatizaciones porque estén de moda.
11. **Asistencia de IA bajo control.** Codex y otros agentes pueden analizar, programar, probar y documentar dentro del alcance autorizado. **No sustituyen la validación del usuario, la prueba física o la aceptación final.** No deben asumir que herramientas, hardware o estados no observados cumplen una condición.
12. **Conservación del historial.** No sobrescribir respaldos verificados, borrar contextos anteriores, cerrar deuda sin evidencia ni presentar un piloto como integración completa. Mantener fuentes de verdad y trazabilidad.

## Contrato de cada incremento

Antes de implementar, dejar claro (en issue, plan de trabajo o documentación equivalente):

| Campo | Pregunta mínima |
| --- | --- |
| Propósito | ¿Qué problema concreto resuelve y cómo sabremos que aporta valor? |
| Alcance | ¿Qué componentes se tocarán y cuáles están expresamente fuera? |
| Baseline | ¿Qué estado actual comprobado estamos preservando? |
| Dependencias y riesgos | ¿Qué podría interrumpirse o corromperse? |
| Gate y autorización | ¿Hay un requisito previo? ¿Está autorizado intervenir? |
| Verificación | ¿Qué pruebas demuestran el éxito y evitan regresiones? |
| Respaldo y reversión | ¿Cómo volvemos al último estado funcional según el riesgo? |
| Evidencia | ¿Qué resultados se observaron realmente, dónde están los informes saneados y qué quedó PENDING? |
| Cierre | ¿Quién acepta el resultado y qué pendientes permanecen? |

### Ruta de ejecución sugerida

1. **Pensar/diagnosticar:** inspección de solo lectura, alternativas y decisión de alcance.
2. **Planear:** especificar entregable, dependencias, criterios PASS/FAIL, contingencia y autorización.
3. **Preparar:** verificar recuperación aplicable, recursos y punto de control. No crear respaldos inútiles para cambios de texto.
4. **Construir:** aplicar la modificación mínima; preferir idempotencia, configuración declarativa y cambios rastreables.
5. **Revisar:** pruebas estáticas, revisión de código/configuración, privacidad y compatibilidad.
6. **Probar:** ejecutar pruebas funcionales y de regresión, observando el componente real.
7. **Recuperar/verificar reversión:** probar rollback de forma aislada cuando sea viable; registrar límites de lo no probado.
8. **Documentar y aceptar:** registrar estado, evidencia y deudas; promover versión solo con aceptación adecuada.

**No todos los incrementos necesitan las mismas herramientas, tiempos o rituales.** La profundidad de cada comprobación depende del riesgo. El principio sí es obligatorio.

## Gates según impacto

| Clase de cambio | Comprobación mínima de avance |
| --- | --- |
| **Documentación pura, sin alterar operación** | exactitud, referencias, privacidad, diff/revisión y reversión Git |
| **Código o script que no modifica el host** | revisión, lint/pruebas, datos de prueba, compatibilidad y rollback Git |
| **Configuración o aplicación de usuario** | backup específico o reversión comprobable; pruebas funcionales sobre el entorno afectado |
| **Servicios, contenedores, BD, red, credenciales, VM o seguridad** | preflight, respaldo consistente recuperable, plan de rollback, validación de servicios dependientes y aceptación explícita |
| **Arranque, almacenamiento, cifrado, escritorio/login o hardware crítico** | recuperación fuera de banda cuando aplique, rollback ensayado, pruebas en hardware real y autorización antes de ejecutar |

Ante cambios irreversibles, probar la **recuperación alternativa** y declarar el riesgo; no fingir que todo puede deshacerse. Si no es posible proteger razonablemente el estado, **diferir** es una decisión correcta.

## Qué significa «terminado»

- **Avance aceptado:** incremento probado y reversible dentro de su alcance; puede ser utilizado sin esperar a que el proyecto completo termine.
- **Operativo/experimental:** describe su utilidad o madurez local, no certifica automáticamente seguridad, reproducibilidad ni soporte.
- **Certificado:** solo cuando satisface todos los gates y Definition of Done específicos del componente con evidencia vigente; ningún agente puede inferirlo.
- **Pendiente/bloqueado:** lo que no fue comprobado queda identificado como PENDING o FAIL, no como PASS.

No convertir estimaciones generadas con IA en compromisos de calendario.

## Aplicación a iniciativas de SineOS

Este estándar se aplica por igual a:
- **Seguridad:** inventario, una corrección a la vez, revalidación y protección de conectividad.
- **SDE:** Alpha 0.1 prueba primero recuperación/transacción; luego incrementos visuales/funcionales, con C0–C12 como certificación final.
- **Aplicaciones, herramientas y scripts:** desarrollo incremental, pruebas, desinstalación y mantenimiento documentados.
- **Contenedores, BD y automatización:** cambios aislados, integridad de datos, verificaciones de arranque/persistencia y recovery.
- **SLDE y laboratorios:** funcionalidades opcionales y aisladas, presupuesto de recursos y regresiones.
- **SineOS Office:** conservar [piloto congelado](../Operations/SineOS-Office-Pilot-Frozen-2026-10-21.md); el estándar NO autoriza descongelarlo, optimizar Windows ni modificar credenciales antes de su gate y autorización.

## Precedencia, excepciones y fuentes

- **No cambia** el orden maestro **Seguridad → SDE → Oracle/n8n/Minecraft → reproducibilidad → SLDE**, ni la planeación congelada o los criterios particulares de cada componente.
- Las obligaciones de seguridad, privacidad y recuperación de mayor exigencia **prevalecen** sobre la ruta mínima de esta norma; no se pueden reducir por conveniencia.
- En incidentes de alta urgencia puede definirse una intervención de alcance acotado con riesgos y aprobación documentados, sin saltarse controles críticos. Después se verifica, registra y reconcilia con el estado objetivo.
- Este documento es la **fuente normativa transversal** del método de ingeniería. Los documentos específicos definen el detalle y los gates de su subsistema.

### Referencias

- [Roadmap maestro y prioridades](../Operations/Project-Roadmap.md).
- [Estándar de documentación](Documentation-Standard.md).
- [Estándar de scripts](Script-Standard.md).
- [Política de evolución tecnológica](Technology-Evolution-Policy.md).
- [Seguridad](../Security/Security-Baseline.md).
- [SDE: roadmap de implementación](SDE-Implementation-Roadmap.md).
- [Seguimiento global](https://github.com/ArgenisPadill/SineOS/issues/4).

**Alcance de esta adopción:** exclusivamente gobierno documental y lineamiento de trabajo. No se ejecutan cambios físicos, configuraciones, instalaciones, servicios o nuevas pruebas del host al publicar esta regla.
