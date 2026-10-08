# SDE — Configuración avanzada y checkpoints

**Fecha de decisión:** 07-10-2026  
**Estado:** planeación congelada / obligatorio para SDE 1.0  
**Issue maestro:** https://github.com/ArgenisPadill/SineOS/issues/1

## Objetivo

SineOS debe ofrecer una configuración limpia para uso normal y permitir acceso a opciones técnicas sin exponer accidentalmente controles que puedan romper sesión, red, recuperación o energía.

La configuración avanzada existe dentro de Configuración de SineOS; no se coloca en el menú contextual del escritorio ni se activa mediante mecanismos ocultos.

# Acceso

Ruta conceptual:

`Configuración de SineOS → Sistema → Mostrar configuración avanzada`

Reglas:
- está oculta por defecto;
- el usuario puede activarla explícitamente;
- la elección persiste entre sesiones;
- desactivarla vuelve a ocultar las opciones avanzadas sin borrar sus valores;
- no se crea un “modo experto” separado del escritorio.

# Niveles de ajustes

## Nivel 1 — técnico editable

Ajustes que pueden modificarse directamente porque tienen impacto limitado y rollback claro.

Ejemplos:
- intensidad visual;
- comportamiento de componentes opcionales;
- parámetros no críticos de panel/dock;
- opciones de diagnóstico.

## Nivel 2 — delicado

Ajustes que pueden afectar experiencia, conectividad, pantallas, composición o energía.

Antes de aplicar:
- explicar qué cambia;
- explicar el riesgo principal;
- crear checkpoint ligero cuando corresponda;
- pedir confirmación;
- validar después del cambio.

## Nivel 3 — crítico

Ajustes que podrían comprometer arranque, login, recovery, red crítica o integridad del sistema.

Regla:
- no exponer edición directa si no existe una forma segura de aplicarlo;
- mostrar información en modo lectura cuando aporte valor;
- requerir flujo administrativo explícito o terminal cuando corresponda;
- nunca convertir Configuración avanzada en un editor genérico de archivos del sistema.

# Checkpoints de configuración avanzada

Antes de un cambio avanzado importante, SineOS crea un checkpoint pequeño y específico de la configuración afectada.

No es:
- un backup completo;
- un reemplazo de Restic;
- el respaldo pre-SDE;
- Last Known Good.

Retención:
- **7 días**;
- eliminación automática después de ese periodo;
- puede eliminarse antes cuando ya no sea necesario y exista estado sano validado.

Cada checkpoint debe registrar:
- componente;
- valor/estado anterior;
- valor/estado aplicado;
- fecha;
- versión SDE;
- método de reversión;
- resultado de validación.

# Reversión automática

Si un cambio avanzado provoca inmediatamente una falla crítica claramente atribuible al cambio, SineOS revierte automáticamente al checkpoint anterior.

Ejemplos:
- compositor deja inutilizable la sesión;
- panel crítico desaparece y no puede recuperarse;
- pantalla principal queda en estado inválido;
- conectividad esencial se rompe por el ajuste;
- un componente de sesión deja de iniciar.

Después:
- informar qué se revirtió;
- registrar resultado;
- conservar datos suficientes para diagnóstico.

# Inestabilidad no crítica

Si el sistema sigue siendo utilizable pero aparecen señales de inestabilidad después del cambio:

- no revertir automáticamente;
- mostrar recomendación de volver al estado anterior;
- ofrecer **Revertir cambio**;
- ofrecer **Mantener configuración**;
- explicar qué comportamiento disparó la recomendación;
- registrar la decisión.

# Reglas de seguridad

- no cambiar valores críticos silenciosamente;
- no encadenar varios ajustes delicados dentro de un único checkpoint opaco;
- no reemplazar Last Known Good con un estado no validado;
- no borrar checkpoints necesarios para una reversión en curso;
- los checkpoints respetan el registro de propiedad de SDE;
- un conflicto con una edición manual se maneja según `SDE-Alpha-0.1-Ownership-Conflict-Spec.md`.

# Integración con Last Known Good

Un checkpoint es temporal.

Last Known Good representa un estado SDE completo que ya fue validado.

Flujo conceptual:

```text
estado sano
   ↓
checkpoint ligero
   ↓
aplicar ajuste
   ↓
validar
   ├─ crítico/falla → revertir checkpoint
   ├─ inestable → recomendar revertir
   └─ sano → conservar configuración
```

Un cambio aislado no promueve automáticamente todo el sistema a Last Known Good.

# Criterios de aceptación

Debe validarse:
- opción avanzada oculta por defecto;
- activación explícita;
- persistencia de la preferencia;
- edición de Nivel 1;
- confirmación y checkpoint de Nivel 2;
- protección de Nivel 3;
- checkpoint conservado 7 días;
- rollback automático ante falla crítica;
- recomendación ante inestabilidad no crítica;
- mantenimiento manual de configuración posible;
- conflicto con cambio manual no destruye datos;
- ausencia de cambios silenciosos sobre configuración crítica.

## Regla final

> Configuración avanzada debe dar más control, no más oportunidades de romper SineOS por accidente.
