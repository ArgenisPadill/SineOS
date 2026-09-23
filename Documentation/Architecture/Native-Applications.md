# SineOS — Estándar de aplicaciones nativas

**Decisión congelada:** 23-09-2026  
**Estado:** Adoptado

## Origen de la decisión

La decisión nace de la experiencia obtenida con **SineOS NetworkPrivacy**.

La administración de DNSCrypt, NetworkManager y Proton VPN podía realizarse mediante comandos de terminal. Aunque técnicamente era posible, la operación cotidiana exigía recordar comandos, revisar estados y ejecutar cambios manualmente.

NetworkPrivacy demostró que una tarea administrativa recurrente puede transformarse en una utilidad pequeña, segura y práctica integrada al escritorio.

A partir de esta experiencia, SineOS adopta formalmente un patrón para futuras herramientas operativas.

## Principio

> Cuando una función necesaria de SineOS no dispone de una aplicación adecuada y su operación recurrente obliga al usuario a ejecutar comandos manuales, debe evaluarse primero la creación de una aplicación nativa sencilla antes de normalizar el uso cotidiano de la terminal.

La terminal continúa siendo una herramienta fundamental de administración y diagnóstico. Este principio no pretende eliminarla.

El objetivo es evitar que tareas repetitivas, sensibles o propensas a errores dependan innecesariamente de recordar comandos.

## Tecnología preferente

Para utilidades pequeñas integradas al escritorio Debian/XFCE, la implementación preferente es:

```text
Python 3
   +
GTK3 / PyGObject
   +
herramientas nativas del sistema
```

Cuando la función corresponda a red, la integración debe realizarse mediante las interfaces soportadas del sistema, por ejemplo:

```text
NetworkManager
    ↓
nmcli / D-Bus / Polkit
```

El uso de NetworkManager no es obligatorio para aplicaciones que no administren red.

La tecnología puede cambiar cuando exista una razón técnica documentada. Python + GTK3 es una preferencia pragmática, no una restricción absoluta.

## Cuándo aplicar este patrón

Debe considerarse una aplicación nativa cuando se cumplan una o varias de estas condiciones:

- la tarea se realiza con frecuencia;
- requiere ejecutar varios comandos en un orden específico;
- es fácil cometer errores manuales;
- modifica configuración sensible;
- requiere consultar varios estados antes de actuar;
- necesita confirmaciones o rollback;
- resulta más práctico acceder desde el menú del escritorio;
- puede beneficiar a un usuario que no necesite conocer los comandos internos.

Una operación de diagnóstico ocasional, un script de mantenimiento no interactivo o una automatización destinada exclusivamente a ejecución programada puede seguir siendo un script de terminal.

## Requisitos mínimos de una aplicación SineOS

Una aplicación nativa no se considera terminada únicamente porque su interfaz funcione.

Debe incluir, como mínimo:

### 1. Código fuente

Debe almacenarse en:

```text
Apps/<NombreAplicacion>/
```

La lógica de interfaz debe separarse de la lógica operativa cuando esto mejore seguridad, pruebas o mantenibilidad.

### 2. Instalador reproducible

Debe existir un script bajo:

```text
Scripts/<NombreAplicacion>/
```

El instalador debe, según corresponda:

- comprobar dependencias;
- informar claramente las dependencias faltantes;
- crear directorios locales necesarios;
- establecer permisos;
- registrar el lanzador;
- actualizar la base de datos de aplicaciones;
- proporcionar una operación de consulta de estado;
- permitir retirar la integración sin destruir datos del usuario.

Cuando sea seguro y apropiado, el instalador puede ofrecer instalación explícita de dependencias. No debe modificar el sistema silenciosamente.

### 3. Integración con el escritorio

Las aplicaciones destinadas a uso interactivo deben integrarse con el menú mediante un archivo:

```text
~/.local/share/applications/<aplicacion>.desktop
```

El lanzador debe definir al menos:

- nombre;
- descripción;
- comando de ejecución;
- icono;
- categoría;
- comportamiento de terminal;
- notificación de inicio cuando corresponda.

La aplicación debe poder iniciarse desde el escritorio sin requerir abrir una terminal.

### 4. Dependencias documentadas

Las dependencias deben quedar documentadas con sus nombres reales de paquete cuando sean conocidos.

Para aplicaciones Python + GTK3 en Debian, normalmente se deben considerar:

```text
python3
python3-gi
gir1.2-gtk-3.0
```

y las dependencias específicas de la función.

### 5. Manual de instalación

Cada aplicación debe incluir instrucciones reproducibles para:

1. requisitos previos;
2. instalación;
3. primera ejecución;
4. validación;
5. consulta de estado;
6. actualización;
7. desinstalación;
8. solución de problemas.

El procedimiento debe poder seguirse sin depender de recordar lo realizado durante el desarrollo original.

### 6. Documentación de operación

Debe existir un documento bajo:

```text
Documentation/Operations/<NombreAplicacion>.md
```

Debe explicar:

- qué problema resuelve;
- por qué fue creada;
- arquitectura;
- dependencias;
- archivos involucrados;
- datos persistentes;
- permisos;
- integración con servicios;
- funcionamiento normal;
- validaciones realizadas;
- limitaciones conocidas;
- recuperación o rollback cuando corresponda.

### 7. Justificación

Toda aplicación propia debe responder explícitamente:

```text
¿Por qué existe esta aplicación?
¿Por qué no se utiliza una herramienta existente?
¿Qué problema operativo elimina?
¿Qué riesgo o fricción reduce?
```

No se crearán aplicaciones únicamente por estética o duplicación innecesaria de software disponible.

### 8. Seguridad

Una aplicación SineOS debe seguir los mismos principios de seguridad del sistema:

- mínimo privilegio;
- interfaz sin root cuando sea viable;
- elevación únicamente mediante mecanismos controlados como Polkit;
- secretos fuera del código y de Git;
- estado local con permisos restrictivos cuando corresponda;
- validación antes y después de cambios;
- rollback cuando una operación sensible pueda fallar;
- ninguna modificación destructiva silenciosa.

### 9. Validación funcional

Antes de considerarse terminada debe probarse el flujo real, no solo la apertura de la ventana.

La validación debe comprobar:

```text
estado inicial
    ↓
acción
    ↓
cambio esperado
    ↓
validación
    ↓
restauración / rollback
```

cuando la naturaleza de la aplicación lo permita.

## Patrón de estructura

Una aplicación típica debe tender a una estructura como:

```text
SineOS/
├── Apps/
│   └── MiAplicacion/
│       ├── mi-aplicacion.py
│       └── modulo_operativo.py
│
├── Scripts/
│   └── MiAplicacion/
│       └── install-mi-aplicacion.sh
│
└── Documentation/
    └── Operations/
        └── MiAplicacion.md
```

No todos los proyectos requerirán exactamente dos módulos Python. La separación se adapta al tamaño real de la herramienta.

## Aplicación de referencia

**SineOS NetworkPrivacy** es la implementación de referencia inicial de este patrón.

Su estructura es:

```text
Apps/NetworkPrivacy/
├── sineos-network-privacy.py
└── network_policy.py

Scripts/NetworkPrivacy/
└── install-network-privacy.sh

Documentation/Operations/
└── NetworkPrivacy.md
```

NetworkPrivacy justificó esta decisión porque sustituyó una operación manual compuesta por múltiples comprobaciones y comandos por una interfaz gráfica integrada a XFCE, manteniendo la lógica real sobre NetworkManager y DNSCrypt.

## Criterio de éxito

El objetivo no es convertir SineOS en un entorno donde todo tenga una GUI.

El objetivo es:

> conservar la potencia de Linux y la terminal para administración profunda, pero convertir las operaciones recurrentes del propio sistema en herramientas claras, seguras y reproducibles cuando una interfaz aporte una mejora real de operación.

## Regla de evolución

Este estándar puede ampliarse conforme aparezcan nuevas aplicaciones.

No debe modificarse únicamente por preferencia estética. Los cambios deben responder a experiencia operativa, seguridad, mantenibilidad o compatibilidad y deben registrarse en el historial del proyecto.
