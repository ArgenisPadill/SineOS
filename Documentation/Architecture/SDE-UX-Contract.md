# SineOS Desktop Experience — Contrato de experiencia de usuario

**Fecha de decisión:** 07-10-2026  
**Estado:** planeación congelada / obligatorio para SDE 1.0  
**Issue maestro:** https://github.com/ArgenisPadill/SineOS/issues/1  
**Plataforma objetivo:** Debian 13 + XFCE 4.20 + X11 + LightDM

## Propósito

Este documento define el contrato de experiencia de usuario de SineOS Desktop Experience (SDE).

SDE no se considera correcto únicamente porque reproduzca el diseño visual previsto. También debe ser predecible, responsivo, recuperable, accesible y consistente durante el uso cotidiano.

El contrato existe para evitar problemas recurrentes observados en escritorios Windows, macOS y Linux: falta de respuesta visible, movimientos inesperados de ventanas, personalización frágil, configuraciones fragmentadas, problemas de escalado, exposición de notificaciones al usar pantallas externas, comportamiento inconsistente entre toolkits y fallas de recuperación.

Los reportes de comunidades y foros se consideran evidencia cualitativa, no prueba estadística. Los requisitos obligatorios son las reglas y criterios de aceptación definidos en este documento.

---

# Reglas centrales de UX

## 1. Respuesta inmediata

Toda acción del usuario debe producir una respuesta visible o perceptible con suficiente rapidez para dejar claro que la entrada fue recibida.

Ejemplos:
- iniciar una aplicación;
- abrir Super+P;
- cambiar una disposición de pantallas;
- montar o desmontar almacenamiento;
- iniciar captura o grabación;
- aplicar configuración de SDE;
- ejecutar reparación o recuperación.

Una acción aceptada por el sistema pero sin feedback perceptible se considera un defecto de UX.

## 2. Sin clics muertos

Un clic, atajo de teclado o acción de menú nunca debe parecer ignorado.

Si la operación todavía se está preparando, SDE debe mostrar un estado intermedio, por ejemplo:
- Abriendo…;
- Detectando…;
- Aplicando…;
- Conectando…;
- Iniciando…;
- Esperando….

El estado intermedio no debe generar una segunda operación de fondo si el usuario vuelve a presionar el mismo control.

## 3. Sin movimientos inesperados

SDE no debe mover, redimensionar, maximizar, minimizar ni cambiar de workspace o monitor una ventana sin:
- intención explícita del usuario; o
- una condición de recuperación que, de no corregirse, dejaría la ventana inaccesible.

Ejemplo válido:
- se desconecta un monitor externo;
- una ventana queda completamente fuera del escritorio visible;
- SDE la devuelve al área visible principal.

Ejemplo inválido:
- reorganizar automáticamente ventanas visibles porque otra disposición parece más estética.

## 4. Persistencia

Un reinicio, cierre/inicio de sesión, hibernación/reanudación o actualización normal no debe reorganizar arbitrariamente:
- panel;
- dock;
- workspaces;
- preset visual;
- preferencias de pantalla;
- indicadores de estado de aplicaciones.

Los cambios validados deben persistir de forma predecible.

## 5. Una configuración, un lugar

Cada preferencia visible para el usuario debe tener un propietario autoritativo y una única fuente de verdad documentada.

SDE debe evitar exponer el mismo ajuste de forma independiente en interfaces que puedan entrar en conflicto.

Ejemplos:
- intensidad de blur pertenece a la configuración de apariencia de SDE;
- topología de pantallas pertenece a la configuración de pantallas de SDE;
- atajos propios de SDE pertenecen a la configuración de atajos de SDE.

La configuración subyacente de XFCE, Picom o Rofi puede seguir existiendo, pero los valores generados por SDE no deben crear fuentes de verdad competidoras.

## 6. Automatización segura

Toda automatización debe ser:
- entendible;
- reversible cuando sea práctico;
- limitada al alcance mínimo necesario;
- visible cuando cambie un estado importante.

Los cambios automáticos importantes deben ofrecer Deshacer o Revertir cuando sea técnicamente viable.

Ejemplos:
- cambiar salida de audio HDMI;
- aplicar una disposición de pantallas;
- reparar un perfil del panel.

## 7. Degradación elegante

Un componente visual u opcional puede fallar sin volver inutilizable el escritorio.

El contrato de degradación existente sigue siendo obligatorio:
- falla Picom → compositor XFWM;
- falla o incompatibilidad de Global Menu → menú local de la aplicación;
- falla Docklike → acceso funcional a ventanas mediante XFCE;
- falla Rofi → Whisker;
- falla Flameshot → xfce4-screenshooter;
- falla pantalla inalámbrica → pantalla cableada sigue funcionando.

## 8. Último estado funcional

SDE mantiene un estado operativo **Last Known Good / Último estado funcional** separado de los respaldos históricos.

Este estado existe para recuperar rápidamente la operación normal después de:
- aplicar una configuración fallida;
- una topología de pantallas inválida;
- un ajuste visual defectuoso;
- una migración incompleta;
- una reparación fallida después de reanudar.

El respaldo histórico y el Último estado funcional son conceptos distintos.

## 9. Estado accesible

Los estados importantes nunca deben comunicarse únicamente mediante color.

Se debe combinar:
- forma;
- posición;
- icono;
- etiqueta;
- grosor de línea o indicador;
- color.

Aplica especialmente a:
- estado activo/inactivo de Docklike;
- solicitudes de atención;
- workspace seleccionado;
- éxito, advertencia y error;
- selección de pantalla.

## 10. Conciencia de contexto

SDE puede adaptar su comportamiento al contexto cuando esa adaptación sea predecible y reversible.

Contextos:
- pantalla completa;
- proyector o pantalla externa;
- pantalla duplicada;
- estado de batería;
- hibernación/reanudación;
- grabación o captura;
- Reduced Motion.

La adaptación nunca debe cambiar silenciosamente preferencias no relacionadas.

## 11. Tolerancia entre toolkits

GTK3, GTK4, Qt5, Qt6, Chromium/Electron y otros toolkits pueden no verse idénticos.

SDE prioriza:
1. funcionamiento correcto;
2. legibilidad;
3. interacción predecible con teclado y mouse;
4. coherencia visual.

Está prohibido forzar uniformidad visual perfecta cuando eso rompa el comportamiento de una aplicación.

## 12. El rendimiento es parte de la UX

Una función visualmente pulida que provoque lag perceptible, entrada retrasada, stutter o consumo excesivo se considera defectuosa.

Las pruebas de rendimiento forman parte de la certificación UX; no son una optimización opcional posterior.

---

# Presupuesto de latencia

Objetivos iniciales de ingeniería:

| Interacción | Objetivo |
|---|---:|
| confirmación de entrada | <= 100 ms |
| respuesta visible de menú / Rofi / Super+P | <= 150 ms |
| operación local corta | <= 500 ms sin bloquear interacción |
| operación > 500 ms | mostrar estado o progreso |
| operación > 2 s | mostrar progreso y Cancelar cuando sea seguro |

Reglas:
- las animaciones no deben retrasar la ejecución del comando;
- la entrada debe procesarse antes de que termine el movimiento decorativo;
- la entrada repetida no debe iniciar operaciones duplicadas;
- la recolección costosa de estado no debe ejecutarse en la ruta crítica de UI.

Estos valores son objetivos de SDE y deberán validarse en el hardware físico disponible.

---

# Transacción de pantalla

Los cambios de pantalla son transaccionales.

Aplica a:
- resolución;
- frecuencia de actualización;
- duplicar;
- extender;
- pantalla principal;
- cambios importantes de topología.

Flujo:

```text
capturar estado actual conocido como funcional
        ↓
aplicar estado propuesto
        ↓
validar salidas
        ↓
mostrar confirmación
        ↓
Mantener / Revertir
        ↓
timeout → reversión automática
```

Tiempo inicial sugerido de confirmación: alrededor de 15 segundos; podrá ajustarse después de pruebas de usabilidad.

Una falla de confirmación gráfica no debe dejar permanentemente al usuario en un estado de pantalla inutilizable.

La recuperación de pantallas también debe estar disponible desde TTY o herramientas de recuperación.

---

# Último estado funcional del escritorio

SDE debe mantener un estado operativo compacto que incluya, cuando corresponda:
- perfil del panel;
- disposición del dock;
- preset visual;
- versión del esquema SDE;
- modo del compositor;
- topología de pantallas;
- estado de DPI/escala;
- workspaces;
- preferencia local de audio asociada al contexto de pantalla.

Después de validar una configuración, esta puede promoverse a Último estado funcional.

Al iniciar o reparar:
- validar el estado actual;
- reparar solo el área dañada cuando sea posible;
- evitar restablecer preferencias no relacionadas.

---

# Validación después de reanudar

Después de una reanudación, SDE realiza una validación de una sola ejecución.

Puede comprobar:
- que xfce4-panel esté activo;
- estado válido del compositor;
- topología de pantallas válida;
- que no existan ventanas completamente fuera del área visible;
- salida de audio válida;
- estado correcto del dock;
- ausencia de overlays SDE obsoletos;
- configuración razonable de DPI y pantallas.

El validador termina al concluir. No debe convertirse en un daemon de sondeo permanente.

Las reparaciones deben ser puntuales y quedar registradas localmente.

---

# Coordinación entre pantalla y audio

La topología de pantallas y la salida de audio están relacionadas, pero son estados distintos.

SDE puede recordar preferencias locales para un contexto conocido, por ejemplo:

```text
Proyector
- extendida
- resolución nativa/común certificada
- audio permanece en la laptop
```

o:

```text
TV
- duplicada
- audio por HDMI
```

Reglas:
- no exportar identificadores de dispositivos como parte de perfiles portables;
- los cambios automáticos de audio deben mostrar feedback visible;
- ofrecer Deshacer cuando sea práctico;
- si desaparece un dispositivo de audio, usar una salida válida en vez de hacer fallar la transacción de pantalla.

---

# Privacidad e interrupciones de notificaciones

La presencia de una pantalla externa aumenta el riesgo de exposición accidental.

SDE debe ofrecer una política segura para pantallas externas sin crear perfiles ligados a una profesión o tipo de usuario.

Al duplicar o proyectar:
- se puede ocultar el contenido sensible de notificaciones;
- puede mostrarse una notificación genérica de la aplicación;
- la notificación original debe seguir disponible en el sistema cuando sea técnicamente viable.

En pantalla completa:
- los banners no urgentes no deben cubrir contenido innecesariamente;
- las notificaciones deben seguir siendo recuperables y no desaparecer silenciosamente.

El comportamiento de privacidad debe ser explícito y configurable.

---

# Modo de edición

La edición estructural del panel y dock no debe estar disponible accidentalmente durante el uso normal.

Estado normal:
- disposición protegida contra arrastre o eliminación accidental.

Flujo de edición:

```text
Configuración de SineOS
  → Personalizar escritorio
  → Editar disposición
```

Al entrar en modo de edición se debe crear un punto de restauración ligero.

Controles requeridos:
- Guardar;
- Deshacer/Revertir;
- Restaurar disposición SineOS.

Al salir se vuelve a proteger la estructura.

---

# Tamaños de interacción

Un icono visual pequeño puede tener una zona efectiva de clic mayor.

Objetivo inicial para escritorio:
- los controles clicables deben ofrecer, cuando el diseño lo permita, un área efectiva de aproximadamente 32×32 px como mínimo.

Para una futura interfaz orientada a touch se puede usar como objetivo aproximadamente 44×44 px o tamaño físico equivalente.

Esto no obliga a que el icono visual sea grande.

---

# Comportamiento de Snap

Snap Preview debe requerir intención clara mediante mouse o teclado.

Reglas:
- no redimensionar de forma prematura solo por acercarse a un borde;
- mostrar preview antes de aplicar;
- aplicar al soltar o confirmar;
- conservar la ventana actual hasta confirmar la operación;
- calcular el layout usando el área útil del monitor activo;
- Esc cancela overlays cuando corresponda.

SDE prioriza snapping predecible sobre automatización agresiva.

---

# Semántica de estados del dock

Los indicadores de Docklike deben entenderse sin depender solamente del color de acento.

Estados conceptuales:

```text
cerrada             sin indicador de ejecución
abierta/inactiva    indicador corto
activa              indicador más fuerte
varias ventanas     indicador + conteo/forma
atención            pulso o símbolo temporal
```

Las animaciones de atención:
- deben ser cortas;
- terminan solas;
- no parpadean indefinidamente;
- se eliminan o reducen con Reduced Motion.

---

# Arquitectura de información de Configuración

La configuración de SDE debe presentar conceptos del usuario, no tecnologías internas.

Categorías preferidas:
- Apariencia;
- Pantallas;
- Audio;
- Mouse y teclado;
- Notificaciones;
- Accesibilidad;
- Atajos;
- Escritorio y disposición;
- SDE avanzado.

No se debe obligar al usuario a comprender:
- detalles internos de Picom;
- sintaxis XRandR;
- rutas XFConf;
- CSS GTK;
- archivos de configuración de Rofi.

Los controles técnicos avanzados pueden existir en una sección explícitamente avanzada.

---

# Certificación de flujos entre toolkits

La certificación debe probar tareas, no solo capturas de pantalla.

Como mínimo:
- Abrir archivo;
- Guardar como;
- Elegir carpeta;
- Cancelar diálogo;
- navegación por teclado;
- comportamiento de Esc;
- portapapeles;
- drag-and-drop;
- pantalla completa;
- escalado del selector de archivos.

Familias:
- XFCE/GTK3;
- GTK4;
- Qt5;
- Qt6;
- Chromium;
- Electron;
- Firefox cuando su comportamiento sea materialmente distinto.

---

# Criterios de aceptación UX para SDE 1.0

## Respuesta
- sin clics muertos en interacciones principales del shell;
- launcher y Super+P reconocen la entrada dentro del objetivo de latencia en el hardware certificado;
- operaciones lentas muestran progreso o estado.

## Predictibilidad
- sin movimiento arbitrario de ventanas;
- un reinicio normal no reorganiza panel o dock;
- cada preferencia tiene un propietario autoritativo.

## Pantallas
- Transacción de pantalla con rollback automático;
- recuperación de ventanas perdidas;
- los cambios de pantalla no corrompen silenciosamente la preferencia de audio;
- la política de privacidad al duplicar/proyectar funciona según lo diseñado.

## Reanudación
- la validación de una sola ejecución termina correctamente;
- la reparación no restablece estado no relacionado.

## Accesibilidad
- los estados importantes se distinguen sin depender solamente del color;
- Reduced Motion se respeta;
- navegación por teclado utilizable.

## Falla
- un componente opcional roto no elimina acceso al escritorio;
- funciona la restauración de Último estado funcional;
- siguen disponibles recuperación local y recuperación certificada desde GitHub.

## Toolkits
- los flujos certificados pasan en la matriz de aplicaciones/toolkits disponible.

## Rendimiento
- los presupuestos de latencia UX y recursos cumplen los umbrales definidos.

---

# Antipatrones prohibidos en SDE

- cambios de estado silenciosos;
- parpadeo infinito para solicitar atención;
- acciones que obligan a hacer clic dos veces porque la primera no muestra feedback;
- configuraciones duplicadas en frontends competidores;
- reorganización automática de ventanas sin necesidad de recuperación;
- cambios de pantalla irreversibles sin confirmación;
- extensión de terceros obligatoria para una función crítica;
- estados comunicados únicamente por color;
- animaciones que bloquean entrada;
- sondeo en segundo plano cuando basta un evento o acción puntual;
- actualizaciones que restablecen una disposición válida del usuario sin migración.

---

# Referencias que informan este contrato

El comportamiento normativo lo define este documento; las fuentes externas son contexto.

- Guía de Microsoft sobre capacidad de respuesta: https://learn.microsoft.com/windows/apps/develop/performance/responsive
- Notificaciones y No molestar en Windows: https://support.microsoft.com/windows/experience/notifications-and-do-not-disturb-in-windows
- Especificaciones SDE relacionadas:
  - `Documentation/Architecture/SineOS-Desktop-Experience.md`
  - `Documentation/Architecture/SDE-Visual-Interaction-Refinements.md`
  - `Documentation/Architecture/SDE-Packaging-Recovery-Certification.md`

## Regla final

> SineOS debe ser sencillo cuando el usuario solo quiere trabajar, potente cuando decide profundizar y predecible en todo momento.
