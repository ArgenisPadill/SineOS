# SDE — Especificación de respaldo y restauración Alpha 0.1

**Fecha:** 07-10-2026  
**Estado:** congelado / obligatorio para Alpha 0.1  
**Issue maestro:** https://github.com/ArgenisPadill/SineOS/issues/1

## Objetivo

El respaldo pre-SDE debe ser:

- fácil de entender;
- fácil de replicar;
- fácil de auditar;
- restaurable con un solo comando;
- verificable antes de modificar el sistema;
- resistente a interrupciones;
- suficientemente simple para Alpha 0.1.

No se utilizarán snapshots sofisticados, bases de datos de estado complejas ni formatos opacos en esta etapa.

> Si una persona no puede entender el respaldo mirando sus carpetas y manifiestos, el diseño es demasiado complejo para Alpha 0.1.

---

# 1. Ubicación

Ruta base:

`~/.local/state/sineos-desktop/recovery/pre-sde/`

Este respaldo es local y existe para rollback inmediato durante la migración.

No sustituye la política normal de respaldos externos de SineOS.

---

# 2. Cifrado y permisos

El respaldo pre-SDE será **sin cifrado** para minimizar dependencias y riesgos durante recovery.

Protecciones:

- directorio raíz con permisos equivalentes a `0700`;
- archivos sensibles con permisos equivalentes a `0600`;
- no guardar contraseñas, tokens, llaves privadas ni secretos;
- si una configuración contiene secretos, debe tratarse mediante una regla específica y no copiarse ciegamente.

El respaldo externo normal conserva su propia política de cifrado.

---

# 3. Inmutabilidad

Una vez creado y validado, el respaldo pre-SDE queda **inmutable**.

Estados separados:

```text
pre-sde/            estado original previo a SDE
checkpoints/        estados temporales antes de cambios importantes
last-known-good/    último estado SDE validado como sano
```

El respaldo pre-SDE no se reutiliza para guardar cambios posteriores.

---

# 4. Estructura

Estructura mínima:

```text
pre-sde/
├── manifest.json
├── README.md
├── checksums.sha256
├── xfce/
├── lightdm/
├── picom/
├── tlp/
├── autostart/
├── displays/
└── associations/
```

Se pueden añadir componentes cuando sean necesarios, manteniendo el mismo modelo simple.

---

# 5. Fuente de verdad

## manifest.json

Fuente de verdad técnica.

Por cada elemento respaldado debe registrar únicamente lo necesario para restaurarlo:

- componente;
- ruta original;
- ruta dentro del respaldo;
- tipo de propiedad;
- SHA-256;
- permisos;
- propietario;
- grupo;
- método de restauración;
- orden/prioridad de restauración;
- si es obligatorio u opcional.

Metadatos globales:

- fecha y hora;
- versión de Debian;
- kernel;
- versión de XFCE;
- versión de LightDM;
- versión/commit de SDE;
- versión del esquema del manifiesto.

## README.md

Resumen humano.

Debe indicar:

- cuándo se creó;
- desde qué sistema;
- qué componentes contiene;
- si la validación pasó;
- cómo ejecutar validación;
- cómo ejecutar dry-run;
- cómo restaurar.

## checksums.sha256

Listado estándar SHA-256 de los archivos respaldados.

---

# 6. Hashes

SHA-256 es el estándar de integridad para Alpha 0.1.

Antes de considerar válido el respaldo:

- todos los archivos obligatorios deben existir;
- todos los hashes deben coincidir;
- el manifiesto debe poder leerse;
- las rutas originales deben estar registradas;
- los métodos de restauración deben ser válidos.

---

# 7. Propiedad de archivos

SDE distingue entre:

## Archivo completo propiedad de SDE

SDE puede reemplazar/restaurar el archivo completo cuando su hash coincide con la versión que SDE instaló.

## Archivo compartido

SDE administra únicamente una parte concreta.

Prioridad de implementación:

1. usar un archivo propio en `conf.d` o mecanismo equivalente;
2. usar un bloque delimitado dentro de un archivo compartido;
3. modificar un archivo completo solo cuando no exista una alternativa segura.

Siempre que exista soporte nativo para `conf.d`, debe preferirse.

---

# 8. Modelo de tres estados

Para detectar cambios manuales se guardan tres referencias:

1. **original** — estado antes de SDE;
2. **aplicado** — estado generado por SDE;
3. **actual** — estado al momento del rollback.

Reglas:

- si actual = aplicado → rollback automático;
- si el usuario cambió una parte no administrada por SDE → conservar ese cambio;
- si el usuario modificó la misma sección que SDE debe revertir → conflicto;
- antes de resolver un conflicto, conservar copia del estado actual;
- nunca borrar silenciosamente cambios manuales;
- si no existe resolución segura, restaurar únicamente lo imprescindible y registrar lo pendiente.

---

# 9. Copias reales y exportaciones

Alpha 0.1 utiliza principalmente **copias reales de archivos**.

Se permiten exportaciones nativas solo cuando aporten una restauración claramente más fiable.

Ejemplos:

- XFConf puede tener exportación nativa;
- panel XFCE puede utilizar perfil/exportación cuando convenga;
- archivos de configuración pequeños se copian directamente.

No se copian paquetes `.deb` únicamente por existir.

Se registran versiones de paquetes y componentes necesarios.

---

# 10. Validación previa obligatoria

Antes de modificar SDE, deben pasar dos gates.

## Gate A — backup válido

Comando conceptual:

`sineos-desktop backup verify`

Comprueba:

- estructura;
- manifiesto;
- archivos obligatorios;
- SHA-256;
- permisos registrados;
- rutas;
- métodos de restauración.

Si falla una pieza obligatoria:

**SDE no se instala ni modifica el escritorio.**

## Gate B — restore dry-run válido

Comando conceptual:

`sineos-desktop restore pre-sde --dry-run`

No modifica nada.

Debe comprobar:

- que cada componente tiene origen y destino;
- que existe un método de restauración;
- que el orden es válido;
- que los permisos necesarios están disponibles;
- que no existen rutas imposibles o estados incompatibles.

Si el dry-run falla:

**SDE no se instala.**

---

# 11. Restauración con un solo comando

Comando objetivo:

`sineos-desktop restore pre-sde`

La restauración debe ser entendible y reproducible sin tener que ejecutar manualmente una colección de scripts.

---

# 12. Orden de restauración

La prioridad es recuperar funcionalidad antes que apariencia.

## Etapa 1 — sesión y base crítica

- LightDM;
- locker;
- configuración necesaria para iniciar sesión.

## Etapa 2 — XFCE funcional

- XFCE;
- panel;
- atajos;
- autostart;
- asociaciones.

## Etapa 3 — integraciones

- displays;
- TLP;
- demás integraciones controladas.

## Etapa 4 — capa visual

- Picom;
- tema;
- iconos;
- cursor;
- wallpaper.

Una falla visual no debe impedir recuperar un escritorio usable.

---

# 13. Restauración reanudable

La restauración debe poder continuar después de:

- apagón;
- reinicio accidental;
- cierre inesperado;
- fallo parcial recuperable.

Archivo de progreso:

`restore-state.json`

Debe registrar como mínimo:

- ID de restauración;
- respaldo utilizado;
- etapa actual;
- componentes completados;
- componente en curso;
- última validación exitosa;
- estado general.

Un componente solo se marca como **restaurado** después de pasar su validación.

Al reiniciar:

- SDE detecta una restauración incompleta;
- ofrece continuar desde el último punto seguro;
- no empieza a ciegas desde cero;
- no vuelve a ejecutar componentes confirmados salvo que una validación indique que es necesario.

---

# 14. Cierre del restore-state

## Restauración exitosa

Cuando toda la restauración termina y la validación final pasa:

1. archivar el estado de restauración dentro del reporte de recuperación;
2. retirar `restore-state.json` del estado activo;
3. generar reporte final;
4. marcar el sistema como restaurado;
5. permitir funcionamiento normal.

## Restauración fallida o incompleta

Si falla:

- conservar `restore-state.json`;
- registrar el error;
- permitir reanudar;
- permitir diagnóstico;
- entrar a Modo seguro si no puede recuperarse un escritorio normal.

---

# 15. Validación por componente

Después de restaurar cada componente debe existir una comprobación mínima.

Ejemplos:

- archivo restaurado con hash esperado;
- servicio/configuración sintácticamente válida;
- XFCE puede leer su configuración;
- LightDM mantiene configuración utilizable;
- panel puede cargarse;
- Picom no bloquea el escritorio;
- TLP acepta su configuración.

La validación exacta se implementa por adaptador/componente.

---

# 16. Idempotencia

Las operaciones de respaldo y restauración deben ser idempotentes cuando sea razonable.

Repetir restore no debe:

- duplicar entradas;
- duplicar autostarts;
- duplicar paneles;
- agregar varias veces bloques SDE;
- sobrescribir cambios del usuario que ya fueron reconocidos como conflicto.

---

# 17. Reporte de recuperación

Cada restauración genera un reporte independiente bajo:

`~/.local/state/sineos-desktop/reports/recovery/`

Debe incluir:

- fecha/hora;
- backup usado;
- versión SDE;
- componentes restaurados;
- componentes omitidos;
- conflictos;
- errores;
- validaciones;
- si se reanudó después de una interrupción;
- resultado final.

Los reportes siguen la política general de retención de 6 meses.

---

# 18. Regla de simplicidad

Alpha 0.1 no implementará:

- snapshots complejos;
- deduplicación avanzada;
- bases de datos de recovery;
- almacenamiento distribuido;
- formatos binarios propios;
- múltiples capas de compresión/cifrado;
- dependencias externas innecesarias.

La prioridad es:

**copiar → describir → verificar → simular → restaurar → validar.**

---

# 19. Gate final de esta especificación

El sistema de backup/restore de Alpha 0.1 queda aprobado únicamente cuando pueda demostrarse en el hardware físico de referencia:

1. creación de backup;
2. SHA-256 correcto;
3. manifest.json legible;
4. README legible;
5. verify aprobado;
6. dry-run aprobado;
7. restore completo;
8. interrupción intencional del restore;
9. reanudación desde último punto seguro;
10. validación final;
11. XFCE funcional;
12. reporte generado.

## Regla final

> El recovery de Alpha 0.1 debe ser más simple que el sistema que intenta recuperar.
