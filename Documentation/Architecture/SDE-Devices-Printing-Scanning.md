# SDE — Impresión y escaneo

**Fecha de decisión:** 07-10-2026  
**Estado:** planeación congelada / obligatorio para SDE 1.0  
**Issue maestro:** https://github.com/ArgenisPadill/SineOS/issues/1

## Principio

SineOS debe facilitar impresión y escaneo sin ocultar Linux ni automatizar de forma riesgosa. La instalación será **guiada**, no silenciosa.

# Impresoras

## Detección e instalación guiada

Al detectar una impresora por red o USB, SineOS muestra una lista de dispositivos encontrados y guía la instalación.

Para impresoras de red debe mostrar, cuando estén disponibles:
- nombre detectado;
- fabricante y modelo;
- IPv4;
- IPv6;
- dirección MAC;
- protocolo;
- estado de compatibilidad.

Si la MAC no puede obtenerse de forma fiable, se muestra “No disponible”.

El usuario participa en:
- elección del dispositivo;
- nombre asignado;
- impresora predeterminada;
- ubicación opcional;
- confirmación de driver o firmware adicional.

Se prioriza impresión driverless/IPP cuando el dispositivo la soporte.

## Hoja de prueba SineOS

Al finalizar la instalación, SineOS pregunta si desea imprimir una hoja de prueba.

Debe ser **una sola hoja** y contener:
- identidad o logotipo SineOS;
- pingüino en ASCII;
- fabricante/empresa;
- modelo;
- nombre asignado;
- puerto o tipo de conexión;
- IP cuando aplique;
- controlador;
- tamaño de papel;
- niveles de tinta, tóner u otros consumibles cuando sean reportados;
- prueba completa de color;
- negro;
- escala de grises;
- líneas finas;
- texto a distintos tamaños;
- patrones útiles para revisar alineación, densidad y calidad.

La hoja puede servir para comprobar calibración visual. La calibración real solo se ejecuta mediante capacidades seguras declaradas por el dispositivo.

## Mantenimiento de impresión

Si la hoja de prueba revela problemas, SineOS ofrece **Corregir calidad de impresión**.

Puede ejecutar, cuando la impresora lo soporte:
- limpieza;
- limpieza profunda;
- alineación;
- calibración;
- limpieza de cabezales;
- mantenimiento de rodillos;
- otras rutinas publicadas por el dispositivo.

SineOS puede llegar al nivel máximo seguro soportado por la impresora, pero nunca:
- repite rutinas agresivas indefinidamente;
- ejecuta comandos no declarados por el dispositivo;
- ignora consumo elevado de tinta/tóner;
- arriesga daño físico por intentar “forzar” mantenimiento.

Las acciones intensas requieren confirmación y explicación de impacto.

## Reporte de diagnóstico

Si el mantenimiento no resuelve el problema, SineOS genera un reporte digital; **no lo imprime**.

Se guarda en una ubicación elegida por el usuario o en la ruta interna de reportes cuando se trate de diagnóstico SineOS.

## Consumibles

- **10 % o menos:** aviso de consumible bajo.
- El aviso indica exactamente cuál consumible está bajo.
- **1 % o menos en cualquier consumible:** se bloquean nuevas impresiones.
- El bloqueo aplica aunque los demás colores estén bien.
- Se mantiene hasta que todos los consumibles estén por encima del 1 %.
- Al reemplazar el cartucho/tóner, SineOS actualiza niveles y retira el bloqueo automáticamente.

## Offline y cola

- Una impresora offline recibe hasta **3 intentos automáticos de reconexión**.
- Si falla, se avisa.
- Si hay trabajos pendientes, el usuario decide si conservarlos en cola o eliminarlos.
- Si existe atasco, tapa abierta, sin papel u otro error físico, SineOS solo informa el estado; no muestra una guía de reparación.
- Cuando la impresora vuelve a estar lista, SineOS espera confirmación del usuario antes de reanudar la cola.
- La cola continúa desde donde se quedó cuando técnicamente sea posible.

## Limpieza por inactividad

Una impresora sin uso durante **3 meses** se elimina automáticamente de la configuración SineOS, incluyendo su registro y configuración asociada.

# Escáneres

## Instalación

- Instalación guiada, igual que impresoras.
- Al finalizar se ofrece un escaneo de prueba.
- Un escáner offline recibe hasta **3 intentos automáticos de reconexión**.
- Si lleva **3 meses sin uso**, se elimina automáticamente de la configuración.

## Ruta de escaneo

Ruta predeterminada:

`~/Documentos/Escaneos/`

Antes de escanear, el usuario debe indicar:
- nombre del archivo;
- formato;
- resolución/DPI;
- color o escala de grises;
- tamaño de papel;
- alimentador o cama plana;
- dúplex cuando exista;
- demás capacidades reales reportadas por el hardware.

## Formatos

SineOS debe permitir, cuando sea técnicamente posible:
- imagen;
- PDF;
- PDF con texto buscable mediante OCR.

Para OCR:
- detectar automáticamente el idioma;
- intentar detectar múltiples idiomas presentes;
- usar los modelos disponibles correspondientes.

## Una o varias páginas

Antes de escanear se pregunta si será:
- una hoja;
- varias hojas.

Si son varias:
1. se escanea una página;
2. se pregunta si desea escanear otra;
3. se repite hasta que el usuario indique que terminó;
4. se genera un solo PDF respetando el orden de captura.

## Revisión antes de guardar

Al terminar puede aparecer el botón **Revisar antes de guardar**.

Desde ahí el usuario puede:
- rotar;
- recortar;
- reordenar;
- eliminar páginas.

SineOS no corrige automáticamente la orientación; la decisión pertenece al usuario.

## Regla final

> Impresión y escaneo deben ser guiados, verificables y recuperables, sin convertir tareas normales en una secuencia de asistentes innecesarios.
