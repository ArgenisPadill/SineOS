# SineOS Desktop Experience — Refinamientos visuales operativos

**Decisión congelada:** 07-10-2026  
**Estado:** aprobado para planificación SDE 1.0 / algunos elementos diferibles a 1.1  
**Documento maestro:** `Documentation/Architecture/SineOS-Desktop-Experience.md`  
**Issue maestro:** https://github.com/ArgenisPadill/SineOS/issues/1

## Propósito

Este addendum completa detalles de interacción y pulido visual que deben sentirse coherentes con SineOS sin añadir otro escritorio, otro window manager ni dependencias residentes innecesarias.

## 1. Vista previa de ajuste de ventanas

Al arrastrar una ventana hacia una zona compatible con snapping, SDE debe mostrar una previsualización clara del área que ocupará antes de soltarla.

Requisitos:
- respuesta visual inmediato;
- overlay ligero y legible;
- cálculo por monitor activo;
- compatibilidad con SineOS Snap;
- sin daemon permanente adicional;
- respetar Reduced Motion;
- no invadir panel/dock fuera del área objetivo.

## 2. Pantalla completa y maximizado

Pantalla completa:
- desactivar blur de fondo innecesario;
- evitar sombras invisibles;
- ocultar panel/dock cuando corresponda;
- evitar animaciones que interfieran con vídeo, presentación o grabación.

Maximizado:
- eliminar radios externos que desperdicien píxeles;
- reducir/eliminar sombra exterior;
- conservar contraste de título/controles;
- restaurar el estilo normal al salir de maximizado.

## 3. Feedback de inicio y progreso

Toda acción que pueda tardar debe indicar que fue recibida.

Aplicable a:
- lanzamiento de aplicaciones;
- montaje/desmontaje de dispositivos;
- cambios de pantalla;
- operaciones de archivos;
- configuración SDE;
- recovery.

Debe distinguir:
- progreso;
- éxito;
- advertencia;
- error;
- timeout.

No debe dejar procesos visuales residentes después de finalizar.

## 4. Consistencia CSD / SSD

SDE debe validar aplicaciones con decoración del lado cliente y del lado de XFWM.

Objetivos:
- evitar dobles barras de título;
- evitar botones duplicados;
- aproximar tipografía, radios, espaciado e iconografía;
- aceptar diferencias cuando forzar uniformidad rompa una aplicación.

Matriz mínima:
- GTK3;
- GTK4/libadwaita;
- Qt5;
- Qt6;
- Chromium;
- Electron.

## 5. Drag & Drop

Estados visuales inequívocos:
- copiar;
- mover;
- crear enlace cuando aplique;
- operación no permitida;
- destino válido.

El cursor y respuesta visual deben usar iconografía SineOS y buen contraste.

## 6. Diálogos del sistema

La matriz de compatibilidad debe incluir:
- abrir archivo;
- guardar como;
- elegir carpeta;
- autenticación;
- impresión;
- selección de color;
- diálogos GTK/Qt relevantes.

Los diálogos críticos SDE pueden usar Smoke/Overlay, pero la funcionalidad nativa tiene prioridad.

## 7. Transiciones de workspaces

Según preset:
- Ligero: sin movimiento espacial o fade mínimo;
- Equilibrado: transición corta y discreta;
- Máximo visual: desplazamiento/zoom solo si está certificado;
- Reduced Motion: sin movimiento espacial.

## 8. Docklike: estados de aplicación

Debe distinguir visualmente:
- cerrada;
- abierta;
- activa;
- minimizada;
- múltiples ventanas;
- atención requerida.

La indicación será discreta y consistente.

## 9. Atención requerida

Una aplicación que solicite atención podrá producir:
- pulso corto en Docklike;
- cambio temporal de indicador;
- señal breve en workspace cuando sea viable.

Debe finalizar automáticamente y respetar Reduced Motion.

## 10. Iconografía externa inconsistente

Reglas previstas:
- padding;
- escala visual;
- máscara/fondo solo cuando sea necesario;
- fallback symbolic para panel;
- nunca deformar logos oficiales.

## 11. Escritorio limpio

Política predeterminada:
- sin acumulación automática de iconos;
- papelera opcional;
- dispositivos removibles solo cuando aporte utilidad;
- wallpaper como elemento visual principal.

## 12. Wallpaper multimonitor

Deseable, no bloqueante para 1.0:
- recorte independiente por salida;
- preservar relación de aspecto;
- evitar estiramiento;
- degradar correctamente en 4:3 y 16:10.

Puede pasar a SDE 1.1 si complica el baseline.

## 13. Proyectores y resoluciones heredadas

La matriz debe incluir:
- 1024x768;
- 1280x800;
- 1366x768;
- 1920x1080;
- 1920x1200;
- 2560x1440;
- 4K cuando exista hardware.

Rofi, panel, OSD y Super+P no deben quedar fuera de pantalla.

## 14. Sistema sonoro

Feedback opcional y mínimo para:
- conectar/desconectar dispositivo;
- captura realizada;
- error relevante;
- login/logout si se aprueba.

Reglas:
- sin sonidos por cada clic;
- configurable/desactivable;
- sin dependencia de otro escritorio.

## 15. Historial de notificaciones

Candidato para SDE 1.1 o para 1.0 solo si puede integrarse sin daemon pesado.

Debe mantener:
- bajo consumo;
- privacidad;
- integración con xfce4-notifyd;
- limpieza sencilla.

## 16. Áreas seguras

Rofi, OSD, notificaciones, Super+P, Snap Preview y overlays deben respetar:
- panel superior;
- dock;
- monitor activo;
- geometría disponible.

Dos overlays críticos no deben ocultarse entre sí.

## 17. Captura y grabación

La interfaz debe conservar contraste y legibilidad al:
- capturarse;
- comprimirse en vídeo;
- compartirse por videollamada;
- proyectarse.

Frost/Overlay no debe depender de transparencias tan sutiles que desaparezcan en grabaciones.

## Prioridad SDE 1.0

### Obligatorio
- vista previa de ajuste de ventanas;
- reglas fullscreen/maximizado;
- respuesta visual de inicio y progreso;
- consistencia CSD/SSD;
- estados básicos de Docklike;
- áreas seguras;
- pruebas de diálogos;
- proyectores/resoluciones heredadas.

### Puede pasar a SDE 1.1
- historial avanzado de notificaciones;
- wallpapers distintos por monitor;
- sistema sonoro completo;
- normalización sofisticada de iconos de terceros.

## Regla

> El pulido visual nunca debe introducir un proceso residente o una dependencia de otro escritorio si la misma experiencia puede resolverse con XFCE/XFWM/Picom y componentes ligeros bajo demanda.
