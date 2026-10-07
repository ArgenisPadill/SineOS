# SineOS Desktop Experience — Política de empaquetado, recuperación, certificación y versiones

**Fecha de decisión:** 07-10-2026  
**Estado:** planeación congelada / implementación pendiente  
**Issue maestro:** https://github.com/ArgenisPadill/SineOS/issues/1  
**Plataforma objetivo:** Debian 13 (Trixie) + XFCE 4.20 + X11 + LightDM

## Principio

SineOS Desktop Experience (SDE) se trata como un subsistema operativo de SineOS, no como una personalización cosmética.

Toda función de SDE debe tener:
- un paquete responsable definido;
- una ruta de instalación;
- una ruta de validación;
- un modo de falla conocido;
- una ruta de reversión;
- una ruta de recuperación;
- un estado de soporte documentado.

Las mejoras visuales solo se aceptan cuando conservan XFCE como respaldo funcional.

---

# Arquitectura de paquetes

SDE se dividirá en paquetes Debian pequeños en lugar de depender de un instalador monolítico.

## 1. sineos-desktop

Metapaquete de la experiencia SDE soportada.

Responsabilidades:
- depender de los paquetes requeridos por SDE;
- proporcionar un punto único de entrada para instalar, actualizar o quitar SDE;
- no contener lógica frágil de ejecución propia.

Relación prevista:
- **Depends:** `sineos-desktop-core`, `sineos-desktop-visual`, `sineos-desktop-assets`, `sineos-desktop-recovery`;
- **Recommends:** `sineos-desktop-tools`;
- **Suggests:** módulos opcionales como grabación avanzada, pantalla inalámbrica y Overview experimental cuando corresponda.

## 2. sineos-desktop-core

Integración crítica del escritorio.

Contiene o administra:
- esquema de configuración de SDE;
- CLI;
- integración con XFCE;
- lógica para aplicar paneles y disposiciones;
- política y fallback de Global Menu;
- integración del backend de pantallas;
- generación de configuración;
- cálculo de Safe Areas;
- marco de migraciones;
- interfaces de estado y salud.

Debe seguir siendo utilizable sin herramientas visuales opcionales.

## 3. sineos-desktop-visual

Capa de integración visual.

Contiene o administra:
- configuración de Picom;
- decoración XFWM;
- CSS de GTK;
- plantillas de integración Qt;
- definiciones de Docklike y Genmon;
- definiciones visuales de Rofi usadas por SDE;
- SineOS Materials;
- políticas de Motion, Focus y Reduced Motion;
- definiciones visuales de OSD.

Una falla de esta capa no debe impedir que XFCE inicie.

## 4. sineos-desktop-assets

Recursos independientes de la arquitectura.

Contiene:
- recursos del logotipo SineOS;
- fondos de pantalla;
- fuentes SVG del cursor y recursos XCursor compilados;
- iconos específicos de SineOS;
- capas de tema;
- fuentes SVG reutilizables.

No se deben duplicar fuentes ya distribuidas por Debian cuando una dependencia de paquete sea suficiente.

## 5. sineos-desktop-tools

Metapaquete o paquete de integración para herramientas de usuario.

Las herramientas predeterminadas pueden incluir:
- Flameshot;
- vokoscreenNG;
- Gromit-MPX;
- scripts auxiliares de captura y pantallas.

Las herramientas avanzadas o no esenciales deben mantenerse como **Recommends** o **Suggests** cuando corresponda.

Ejemplos de herramientas opcionales:
- OBS;
- backend de pantalla inalámbrica;
- implementación candidata o experimental de Overview.

## 6. sineos-desktop-recovery

Paquete mínimo de recuperación. Este paquete es crítico y debe tener la menor cantidad posible de dependencias.

Contiene:
- configuración XFCE de respaldo conocida como funcional;
- lógica de respaldo y restauración;
- verificaciones de salud de SDE;
- comando de modo seguro;
- comando de rollback;
- comando de reparación;
- metadatos locales de recuperación.

No debe depender de Picom, Rofi, Docklike, OBS, pantalla inalámbrica ni otros componentes visuales opcionales.

El paquete de recuperación permanece instalado mientras SDE esté instalado.

---

# Política de dependencias Debian

Las relaciones entre paquetes se usarán de forma intencional:

- **Depends:** SDE no puede proporcionar su función definida sin esa dependencia.
- **Recommends:** forma parte de la experiencia normal soportada, pero SDE sigue siendo operativo sin ella.
- **Suggests:** mejora opcional.

Referencia:
- Debian Policy, relaciones entre paquetes: https://www.debian.org/doc/debian-policy/ch-relationships.html

Los paquetes y scripts de mantenimiento deben ser idempotentes. Ejecutar nuevamente una instalación o recuperación debe converger al estado esperado, no duplicar ni corromper configuración.

Referencia:
- Debian Policy, idempotencia de scripts de mantenimiento: https://www.debian.org/doc/debian-policy/ch-maintainerscripts.html

---

# Modelo de recuperación

La experiencia de recuperación conserva intencionalmente el patrón probado de SineOS:

> Clonar desde GitHub un estado conocido de SineOS y ejecutar un script de recuperación.

Sin embargo, la recuperación no debe depender exclusivamente de Internet ni de la rama móvil `main`.

## Ruta A — recuperación local

Es la opción preferida cuando está disponible.

Interfaz conceptual:

```bash
sineos-desktop safe-mode
sineos-desktop health
sineos-desktop repair
sineos-desktop rollback
```

El paquete de recuperación conserva suficiente información local para:
- detener o deshabilitar una sesión de Picom defectuosa;
- restaurar el compositor de XFWM;
- restaurar un perfil de panel conocido como funcional;
- deshabilitar entradas de autoinicio de SDE dañadas;
- restaurar el último estado SDE certificado;
- restaurar el respaldo de XFCE previo a SDE;
- informar qué cambios realizó.

Esta ruta debe funcionar sin conexión de red.

## Ruta B — recuperación desde GitHub

Se usa desde una TTY o terminal funcional cuando la recuperación local está dañada o no está disponible.

Flujo conceptual:

```bash
git clone --branch <release-o-tag-certificado> <repositorio-SineOS>
cd SineOS
sudo ./<bootstrap-de-recuperacion>.sh
```

El nombre final del archivo será un detalle de implementación, pero el script deberá admitir operaciones equivalentes a:

```text
diagnose
repair
restore-last-good
restore-pre-sde
verify
```

Reglas:
- nunca recuperar producción desde un checkout sin fijar de `main`;
- usar un tag de release o commit explícitamente certificado;
- mostrar el commit o tag que se utilizará antes de modificar el sistema;
- verificar archivos requeridos y checksums cuando corresponda;
- crear un respaldo nuevo antes de reparar cuando el sistema de archivos lo permita;
- mostrar toda acción destructiva;
- ser seguro al ejecutarse más de una vez;
- funcionar desde TTY sin requerir sesión gráfica.

## Ruta C — recuperación externa u offline

Para una falla completa de red o indisponibilidad del repositorio, SDE debe permitir recuperación desde:
- un bundle de release almacenado localmente;
- una copia USB de la release certificada;
- un paquete de recuperación SDE descargado previamente.

Esto evita convertir GitHub en un punto único de falla para recuperación.

## Niveles de recuperación

### Nivel 0 — Diagnóstico
Inspección de solo lectura.

### Nivel 1 — Reparar sesión visual
Restaurar compositor, panel y autoinicio sin sobrescribir datos del usuario.

### Nivel 2 — Restaurar último estado SDE conocido como funcional
Usar el último respaldo local certificado de SDE.

### Nivel 3 — Restaurar XFCE previo a SDE
Regresar al baseline funcional de XFCE respaldado antes de instalar SDE.

### Nivel 4 — Reconstruir desde release certificada en GitHub
Reconstruir SDE desde un tag, release o commit fijado y certificado.

---

# Contrato de respaldo

Antes de una instalación, migración o reparación que modifique el estado del escritorio, SDE debe registrar:
- versión de SDE;
- commit de Git o versión de paquete;
- respaldo de configuración XFCE;
- perfil del panel;
- estado de Picom;
- versión del esquema de configuración SDE;
- versiones instaladas de los paquetes SDE;
- fecha y hora;
- metadatos locales de pantalla separados de las preferencias portables.

Los respaldos de recuperación no deben incluir secretos de manera innecesaria.

---

# Ciclo de versiones

SDE utilizará cuatro etapas de ingeniería.

## Alpha

Propósito:
- arquitectura;
- división de paquetes;
- instalador;
- recuperación;
- integración visual básica.

Reglas:
- puede contener funciones incompletas;
- puede cambiar el esquema de configuración;
- no se declara segura para uso diario;
- ya debe contar con recuperación.

Patrón sugerido de tag:
`sde-v0.1.0-alpha.1`

Versión Debian sugerida:
`0.1.0~alpha1-1`

## Beta

Propósito:
- candidato funcionalmente completo para uso diario controlado;
- integración visual y de comportamiento mayormente congelada;
- todavía pueden existir errores de compatibilidad.

Requisitos de entrada:
- instalación idempotente;
- desinstalación funcional;
- recuperación local funcional;
- recuperación desde GitHub funcional;
- multimonitor básico funcional;
- sin problemas críticos conocidos que impliquen pérdida de datos o configuración.

Rango sugerido:
`sde-v0.5.x-beta.N`

## Candidato a versión estable (RC)

Propósito:
- comportamiento esperado de la versión 1.0;
- no agregar funciones nuevas salvo que sean necesarias para resolver un bloqueo de release.

Requisitos de entrada:
- matriz de hardware sustancialmente cubierta con evidencia disponible;
- presupuesto de RAM/CPU/GPU medido;
- hibernación/reanudación certificadas en el hardware de referencia;
- hot-plug HDMI certificado;
- rollback y reinstalación limpia certificados;
- documentación suficiente para recuperar el sistema sin depender de esta conversación.

Rango sugerido:
`sde-v0.9.x-rc.N`

## Estable

Primera versión estable:
`sde-v1.0.0`

Estable significa:
- instalación reproducible;
- recuperación soportada;
- hardware de referencia certificado;
- compatibilidad restante documentada con honestidad;
- dependencias documentadas;
- presupuesto de recursos definido;
- sin fallas bloqueantes;
- ruta de migración hacia la siguiente versión soportada.

Ninguna función se promueve a estable solamente porque visualmente parezca terminada.

## Orden de versiones Debian

Se usará la convención de tilde de Debian para que las versiones previas ordenen antes de la versión final.

Ejemplos:
- `1.0.0~alpha1-1`
- `1.0.0~beta1-1`
- `1.0.0~rc1-1`
- `1.0.0-1`

Debian Policy define que `~` ordena antes que la versión definitiva.

Referencia:
- https://www.debian.org/doc/debian-policy/ch-controlfields.html

---

# Modelo de certificación

La certificación de SDE se basa en capacidades y evidencia, no en lenguaje de marketing.

## C0 — Arranque y fallback

Requiere:
- login;
- logout;
- reinicio;
- XFCE inicia;
- compositor de respaldo funciona;
- SDE puede deshabilitarse sin perder acceso al escritorio.

## C1 — Experiencia de escritorio

Requiere:
- panel;
- dock;
- fallback de Global Menu;
- fallback de Rofi;
- baseline GTK/Qt;
- OSD;
- manejo CSD/SSD;
- comportamiento de Snap/Overview aplicable a la versión probada.

## C2 — Pantallas

Requiere:
- pantalla interna;
- hot-plug HDMI;
- duplicar;
- extender;
- solo pantalla interna;
- prueba con proyector cuando exista hardware disponible;
- cambio de resolución;
- recuperación de ventanas perdidas.

La pantalla inalámbrica se certifica por separado y no bloquea la certificación de pantallas cableadas.

## C3 — Rendimiento

Medir:
- diferencia de RAM en reposo;
- diferencia de CPU en reposo;
- carga GPU del compositor;
- tiempo de login;
- impacto en video fullscreen;
- impacto con dos monitores cuando exista hardware;
- impacto de captura y grabación.

Una prueba no aprueba solamente porque el sistema siga respondiendo: debe cumplir el presupuesto definido de SDE.

## C4 — Hibernación, reanudación y resiliencia

Requiere:
- hibernación;
- reanudación;
- recuperación del estado de pantallas;
- recuperación del compositor;
- recuperación del panel;
- recuperación normal de UI de red/audio;
- sin overlays huérfanos ni geometría de pantallas obsoleta.

## C5 — Recuperación y replicación

Requiere:
- segunda ejecución de instalación segura e idempotente;
- modo seguro local funcional;
- rollback local funcional;
- recuperación desde GitHub funcional;
- recuperación offline funcional cuando exista el bundle correspondiente;
- desinstalación que restaure un XFCE funcional;
- capacidad documentada de reconstruir la versión certificada de SDE.

---

# Estados de soporte de hardware

Una configuración puede clasificarse como:

## Certificado
Probada físicamente con la suite completa aplicable.

## Verificado por comunidad
Probada físicamente por otra persona mediante la suite oficial y con evidencia suficiente.

Este estado es opcional y solo se utilizará si en el futuro existe participación externa real.

## Compatible
Se espera compatibilidad por Debian/XFCE/upstream o por pruebas parciales, pero no existe certificación física completa de SDE.

## Experimental
La función o ruta de hardware está bajo validación y puede tener limitaciones conocidas.

## No soportado
Se sabe que no cumple los requisitos de SDE o queda fuera del alcance del proyecto.

El estado debe indicar cuando sea relevante:
- GPU, proveedor y ruta de driver;
- resolución o topología de pantallas;
- versión de SDE;
- versión de Debian;
- fecha de validación.

SDE 1.0 no exige tener múltiples equipos ni máquinas virtuales. La certificación completa se realiza sobre el hardware físico disponible; el resto se documenta con un estado honesto.

---

# Reglas que bloquean una versión estable

Una versión no puede avanzar a estable si existe:
- falla de login;
- falla del panel sin recuperación;
- falla del compositor sin recuperación;
- rollback roto;
- desinstalación rota;
- regresión que deje ventanas inaccesibles después de hot-plug HDMI normal;
- problema crítico CSD/SSD que vuelva inutilizable una aplicación común;
- consumo por encima del presupuesto acordado sin excepción documentada;
- migración de configuración que pueda destruir el último estado funcional;
- dependencia de una rama Git sin fijar;
- dependencia obligatoria no documentada.

---

# CI y artefactos de release

Objetivos de planeación:
- lint de scripts;
- validar metadatos de paquetes;
- construir artefactos `.deb`;
- validar esquema y plantillas de configuración;
- comprobar idempotencia donde pueda automatizarse sin máquinas virtuales;
- publicar checksums;
- adjuntar notas de versión;
- adjuntar manifiesto de paquetes;
- registrar versiones de dependencias upstream;
- conservar el script de bootstrap de recuperación con cada release.

Una release debe poder reconstruirse desde el estado del repositorio más las fuentes upstream documentadas.

---

# Convención de nombres

Proyecto:
**SineOS Desktop Experience (SDE)**

Paquetes:
- `sineos-desktop`
- `sineos-desktop-core`
- `sineos-desktop-visual`
- `sineos-desktop-assets`
- `sineos-desktop-tools`
- `sineos-desktop-recovery`

Los módulos opcionales pueden usar:
- `sineos-desktop-<funcion>`

Etapas de release:
**Alpha → Beta → RC → Estable**

Estos nombres describen madurez de ingeniería, no calidad visual.

---

# Regla final

> Una versión de SineOS Desktop Experience no está certificada porque se instale correctamente. Está certificada cuando además puede fallar de forma segura, recuperarse de manera predecible y reconstruirse a partir de entradas documentadas.
