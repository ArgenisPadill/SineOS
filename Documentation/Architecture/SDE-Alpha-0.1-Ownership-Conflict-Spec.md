# SDE — Propiedad de archivos y resolución de conflictos Alpha 0.1

**Fecha:** 07-10-2026  
**Estado:** congelado / obligatorio para Alpha 0.1  
**Issue maestro:** https://github.com/ArgenisPadill/SineOS/issues/1

## Objetivo

SDE debe saber exactamente qué creó, qué modificó y qué únicamente observa.

El propósito es garantizar que:

- rollback solo revierta cambios de SDE;
- uninstall no borre configuración ajena;
- cambios manuales del usuario no se pierdan;
- los conflictos puedan detectarse y aislarse;
- recovery siga siendo simple de entender y auditar.

> SineOS nunca debe borrar ni restaurar un elemento que no esté registrado explícitamente como administrado por SDE.

---

# 1. Registro de propiedad

Ruta:

`~/.local/state/sineos-desktop/state/ownership.json`

Este archivo es la fuente de verdad de propiedad operativa de SDE.

Debe ser:

- legible;
- versionado;
- pequeño;
- fácil de respaldar;
- fácil de inspeccionar;
- suficiente para rollback y uninstall.

---

# 2. Tipos de propiedad

Alpha 0.1 utiliza únicamente tres tipos.

## owned

SDE creó y controla el archivo completo.

Ejemplos:
- archivos propios bajo `~/.config/sineos-desktop/`;
- configuración generada exclusivamente por SDE;
- assets o plantillas propias.

SDE puede reemplazar o borrar estos archivos cuando su estado coincide con lo registrado.

## managed-block

SDE controla únicamente una sección dentro de un archivo compartido.

Debe usarse solo cuando no exista un mecanismo mejor como `conf.d`.

El bloque debe estar claramente delimitado.

Ejemplo conceptual:

```text
# BEGIN SINEOS MANAGED BLOCK
...
# END SINEOS MANAGED BLOCK
```

SDE nunca debe considerar propiedad suya el resto del archivo.

## observed

SDE consulta o valida el recurso, pero no lo administra.

Ejemplos:
- rutas del sistema;
- archivos de terceros usados para diagnóstico;
- configuración que SDE necesita conocer pero no debe modificar.

Un elemento `observed` nunca se borra ni restaura durante rollback/uninstall.

---

# 3. Prioridad de integración

Cuando SDE necesita configurar un componente:

1. preferir archivo propio en `conf.d` o mecanismo equivalente;
2. después, usar archivo propio cargado por el componente;
3. solo si no existe alternativa, usar `managed-block`;
4. modificar un archivo completo compartido únicamente como último recurso.

La meta es minimizar edición de archivos ajenos.

---

# 4. Campos mínimos por entrada

Cada entrada de `ownership.json` debe registrar, como mínimo:

- `component`;
- `path`;
- `owner_type`;
- `previous_hash`;
- `applied_hash`;
- `restore_method`;
- `sde_version`;
- `schema_version`.

Cuando sea útil para archivos/bloques pequeños:

- `applied_copy`.

No se agregan campos por anticipación si no aportan a rollback, uninstall o auditoría.

---

# 5. Estados utilizados para comparación

SDE trabaja con tres estados:

1. **previous** — estado anterior a SDE;
2. **applied** — estado que SDE dejó después de aplicar el cambio;
3. **current** — estado encontrado al momento del rollback/uninstall.

`current_hash` se calcula en tiempo de ejecución y no necesita almacenarse permanentemente.

---

# 6. Regla de comparación

## Caso A — sin cambios del usuario

Si:

`current == applied`

SDE puede revertir automáticamente.

## Caso B — cambio fuera del área administrada

Si el usuario cambió una parte que no pertenece al bloque/archivo administrado por SDE:

- conservar el cambio del usuario;
- revertir únicamente la parte propiedad de SDE;
- continuar con rollback.

## Caso C — cambio dentro del área administrada

Si el usuario modificó exactamente el archivo o bloque que SDE necesita revertir:

- no sobrescribir a ciegas;
- crear copia del estado actual;
- marcar conflicto;
- detener únicamente ese componente;
- continuar con otros componentes si es seguro.

---

# 7. Copia de seguridad antes de resolver conflictos

Antes de tocar un conflicto:

- conservar la versión actual;
- registrar ruta y hash;
- asociarla al reporte de rollback/recovery;
- nunca eliminar silenciosamente la personalización existente.

---

# 8. Severidad de conflictos

## Conflicto menor

Ejemplos:
- tema;
- iconos;
- wallpaper;
- Picom;
- preferencias visuales.

Comportamiento:
- registrar conflicto;
- omitir/revertir parcialmente;
- continuar restauración.

## Conflicto importante

Ejemplos:
- panel;
- autostart;
- displays;
- asociaciones esenciales.

Comportamiento:
- intentar restauración segura;
- si no es posible, aislar componente;
- continuar únicamente si XFCE sigue siendo utilizable.

## Conflicto crítico

Ejemplos:
- LightDM;
- locker;
- configuración necesaria para iniciar sesión;
- componentes de recovery.

Comportamiento:
- detener esa fase;
- proteger estado actual;
- generar reporte;
- entrar a Modo seguro si no puede garantizarse un escritorio recuperable.

---

# 9. Uninstall

La desinstalación usa el mismo registro de propiedad.

Reglas:

- `owned` → puede retirarse si coincide con el estado aplicado o si existe resolución segura;
- `managed-block` → retirar solo el bloque de SDE;
- `observed` → nunca tocar;
- cualquier cambio manual detectado se preserva;
- si existe conflicto, conservar estado actual y reportar.

Uninstall no debe equivaler a “borrar toda la configuración de XFCE”.

---

# 10. Idempotencia

El registro de propiedad debe impedir:

- duplicar bloques SDE;
- registrar varias veces el mismo recurso;
- sobrescribir hashes sin razón;
- perder referencia al estado anterior;
- convertir un recurso observado en administrado sin migración explícita.

---

# 11. Integración con backup/restore

`ownership.json` debe respaldarse junto al estado de recovery.

La especificación de backup/restore vive en:

`Documentation/Architecture/SDE-Alpha-0.1-Backup-Restore-Spec.md`

Ambos sistemas deben coordinarse:

- backup conserva estado previo;
- ownership registra lo que SDE aplica;
- rollback compara previous/applied/current;
- restore recupera componentes;
- reportes registran conflictos y resultado final.

---

# 12. Integración con Last Known Good

Un estado no se promueve a Last Known Good si:

- ownership contiene conflictos críticos no resueltos;
- faltan hashes obligatorios;
- existen recursos administrados sin método de restore;
- la validación final falla.

---

# 13. Formato simple

Alpha 0.1 no usará:

- base de datos de ownership;
- daemon dedicado;
- servicio residente;
- motor complejo de merge;
- formato binario propietario.

El baseline es un JSON pequeño + archivos/copias auxiliares cuando sea necesario.

---

# 14. Gate de aceptación

Esta parte de Alpha 0.1 se aprueba cuando pueda demostrarse:

1. creación de `ownership.json`;
2. registro correcto de un archivo `owned`;
3. registro correcto de un `managed-block`;
4. registro correcto de un recurso `observed`;
5. detección de estado sin cambios;
6. rollback automático seguro;
7. detección de cambio ajeno a SDE;
8. preservación de ese cambio;
9. detección de conflicto dentro de área administrada;
10. copia del estado actual antes de resolver;
11. continuación de rollback tras conflicto menor;
12. detención segura ante conflicto crítico;
13. uninstall sin borrar configuración ajena.

## Regla final

> SDE solo revierte lo que puede demostrar que le pertenece.
