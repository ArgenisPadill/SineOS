# SDE — Salud de hardware y protección operativa

**Fecha de decisión:** 07-10-2026  
**Estado:** planeación congelada / obligatorio para SDE 1.0  
**Issue maestro:** https://github.com/ArgenisPadill/SineOS/issues/1

## Principio

SineOS debe detectar degradación o fallas importantes de hardware, informar con claridad y priorizar la preservación de datos. No debe fingir que puede reparar hardware físicamente defectuoso.

# Batería

## Salud

- Si la salud baja de **70 %**, mostrar aviso informativo.
- Permitir **Recordar en 30 días**.
- Si la salud baja aproximadamente a **50 % o menos**, mantener aviso informativo y ofrecer **Recordar en 15 días**.
- No bloquear el sistema por desgaste de batería.
- Mostrar capacidad de diseño y capacidad máxima actual cuando estén disponibles.
- Si la batería no carga correctamente, el porcentaje queda estancado o existe comportamiento anómalo de carga, avisar solamente.

# Temperatura y refrigeración

- No usar un umbral universal fijo para todos los equipos.
- Basarse en sensores y límites reportados por el hardware.
- Avisar ante temperatura alta sostenida y cercanía a límites térmicos.
- Antes de cambiar automáticamente de Rendimiento a Equilibrado/Ahorro por temperatura, pedir confirmación.
- Cuando la temperatura se normalice, restaurar automáticamente el perfil anterior y mostrar un aviso informativo.
- Si el ventilador permanece al máximo durante mucho tiempo y la temperatura no baja, avisar de posible problema de refrigeración o mantenimiento.

# Disco interno y SMART

## Advertencia crítica

Errores SMART o señales serias de fallo:
- aviso inmediato;
- indicar unidad afectada;
- mostrar tipo de alerta;
- ofrecer abrir la herramienta de respaldo.

## Modo de protección de almacenamiento

Si el disco entra en estado crítico:
- permitir uso ligero;
- recordar que la unidad debe reemplazarse;
- evitar escrituras pesadas innecesarias;
- pausar actualizaciones del sistema;
- bloquear operaciones normales de APT mediante mecanismos de protección;
- estas protecciones no son una barrera absoluta frente a un root que deliberadamente las retire.

Tras reemplazar/restaurar el disco:
- SineOS debe detectar que proviene de una restauración;
- verificar salud del nuevo medio;
- ejecutar validación completa;
- reparar automáticamente errores menores cuando sea seguro;
- generar reporte si algo queda pendiente;
- reactivar actualizaciones cuando el sistema vuelva a estar saludable.

# RAM

Una falla seria de RAM se considera crítica.

Ante señales fiables:
- aviso inmediato;
- acción principal: abrir respaldo;
- priorizar primero Documentos y datos personales;
- después configuración del sistema y demás componentes respaldables;
- si no hay medio externo, esperar a que el usuario conecte un disco o USB;
- si no hay espacio suficiente, avisar y esperar un medio adecuado;
- no fragmentar el respaldo entre múltiples dispositivos de forma automática.

El respaldo usa el esquema normal de respaldos de SineOS; no se marca como “emergencia”.

Si existen archivos irrecuperables o corrupción durante el respaldo:
- recuperar todo lo posible;
- generar un único reporte asociado con lo que no pudo validarse o copiarse.

# CPU y GPU

Se aplica la misma política crítica que RAM cuando existe evidencia seria de fallo físico.

Si el problema parece térmico o de controlador:
1. intentar medidas seguras de reducción de carga;
2. aplicar política térmica aprobada;
3. reiniciar de forma controlada componente/servicio cuando sea seguro;
4. validar;
5. escalar a protocolo crítico solo si persiste o aparece evidencia física.

# Sistema de archivos

Ante corrupción seria:
- no reparar agresivamente mientras el sistema de archivos esté montado y en uso;
- avisar;
- recomendar respaldo cuando sea posible;
- programar verificación/reparación en reinicio o modo de mantenimiento;
- generar reporte;
- si la reparación no deja el sistema saludable, iniciar en Modo seguro.

Antes de reiniciar:
- dar oportunidad de guardar trabajo;
- detectar contenedores, máquinas virtuales y servicios relevantes;
- avisar cuáles están activos;
- esperar a que el usuario los detenga o suspenda, salvo peligro crítico de empeorar la corrupción.

# Aplicaciones congeladas

Cuando una aplicación deja de responder:
- avisar que está congelada;
- ofrecer **Intentar recuperar** o **Forzar cierre**;
- si el usuario elige Forzar cierre, ejecutar la acción sin añadir advertencias repetitivas.

## Inestabilidad recurrente

Si una misma aplicación se congela **3 veces en 7 días**:
- marcar como inestable;
- informar al usuario;
- ofrecer Diagnosticar;
- revisar versión, logs, recursos, GPU/driver, actualizaciones recientes y errores relacionados;
- proponer reparaciones seguras;
- pedir confirmación para acciones destructivas o de alto impacto;
- generar reporte si no puede resolverse.

# Reportes técnicos

Ruta base:

`~/.local/state/sineos-desktop/reports/`

Subcarpetas conceptuales:
- `recovery/`
- `health/`
- `hardware/`
- `updates/`
- `applications/`

Cada evento genera **un archivo nuevo e independiente**, no incremental.

Retención:
- **6 meses desde su creación**;
- después se elimina automáticamente.

Convención de nombre:
`<tipo>-sineos_DDMMAA.pdf`

Ejemplos:
- `reporte-recuperacion-sineos_071026.pdf`
- `reporte-hardware-sineos_071026.pdf`

El reporte puede mostrar datos técnicos completos cuando sean relevantes:
- IP;
- IDs de hardware;
- nombres de dispositivos;
- rutas locales;
- versiones;
- servicios;
- errores.

Cuando se genera un reporte:
- mostrar ruta exacta;
- ofrecer botón **Abrir ubicación**;
- abrir Thunar en la carpeta y señalar el archivo cuando sea posible.

# Modo seguro

Si después de una restauración o reparación quedan errores críticos:
- iniciar XFCE funcional en modo reducido;
- desactivar Picom y efectos;
- desactivar módulos visuales opcionales;
- conservar red, Thunar, terminal, navegador, respaldo, diagnóstico y reparación;
- mantener actualizaciones pausadas si corresponde;
- mostrar claramente que el sistema está en Modo seguro;
- ofrecer Ver reporte, Abrir ubicación e Intentar reparar;
- regresar al modo normal solo después de validación satisfactoria.

## Regla final

> Ante una falla física o corrupción seria, SineOS prioriza datos, diagnóstico y recuperación antes que rendimiento o estética.
