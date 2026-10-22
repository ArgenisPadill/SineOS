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

El detalle del contrato de trabajo, los niveles de riesgo y los criterios de aceptación están en el estándar enlazado. Los estándares más específicos de cada componente, las políticas de seguridad y sus gates siguen aplicando íntegramente.
