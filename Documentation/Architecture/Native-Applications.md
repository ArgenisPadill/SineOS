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

## Estándar de experiencia de usuario

La experiencia de NetworkPrivacy establece que una aplicación SineOS no debe limitarse a envolver comandos en botones. Debe **reducir la carga mental y operacional** del usuario.

> Una aplicación SineOS debe hacer evidente qué está ocurriendo, qué puede hacer el usuario y qué ocurrirá después de ejecutar una acción.

El usuario no debería necesitar conocer cómo funciona internamente el servicio para realizar una operación cotidiana de forma segura. Los detalles técnicos deben seguir disponibles, pero no dominar la experiencia normal.

### 1. Uso normal sin terminal

Una aplicación creada para sustituir una operación manual debe permitir completar su flujo normal sin abrir una terminal. La terminal queda para diagnóstico avanzado, recuperación excepcional, desarrollo y administración especializada.

Si después de instalar la aplicación el uso cotidiano todavía obliga a copiar comandos, la experiencia no se considera terminada.

### 2. Mínimo número de pasos

Las tareas frecuentes deben requerir el menor número razonable de acciones. Deben evitarse asistentes, ventanas, preguntas y campos técnicos innecesarios.

Las confirmaciones se reservan para acciones que interrumpan conectividad, afecten datos, modifiquen configuración sensible o tengan consecuencias difíciles de revertir.

### 3. Estado antes que controles

La interfaz debe responder primero: **¿qué está ocurriendo ahora?** y después: **¿qué puedo hacer?**

El estado actual debe ser visible sin obligar al usuario a interpretar logs o ejecutar comprobaciones adicionales. Cuando aplique, deben diferenciarse claramente estados como activo, inactivo, disponible, en espera, requiere atención, error o sin conexión.

No debe mostrarse un estado positivo si la aplicación no puede verificarlo razonablemente.

### 4. Acciones contextuales

La acción principal debe cambiar de acuerdo con el estado real. No deben mostrarse simultáneamente acciones incompatibles que obliguen al usuario a conocer detalles internos para decidir.

NetworkPrivacy fija el patrón de referencia: DNS de red → **Activar DNSCrypt**; DNSCrypt activo → **Restaurar DNS de la red**; Proton VPN activo → la modificación DNS queda bloqueada mientras la VPN controla esa función.

### 5. Lenguaje humano

Los textos principales deben describir efectos y estados en lenguaje comprensible: **Conexión protegida**, **VPN activa**, **Restaurar DNS de la red**, **No se pudo activar DNSCrypt**.

Puertos, parámetros, interfaces, servicios y comandos pueden mostrarse en detalles técnicos. La interfaz no debe ocultar la realidad técnica, pero tampoco exigir conocerla para operar correctamente.

### 6. Divulgación progresiva

La información debe organizarse en capas:

```text
Resumen
   ↓
estado y acción principal
   ↓
detalles técnicos opcionales
```

La pantalla principal debe resolver la necesidad cotidiana. Los datos de diagnóstico deben permanecer accesibles sin saturar la vista.

### 7. Prevención de errores

Siempre que sea posible se debe **prevenir antes que corregir**: deshabilitar acciones inválidas, detectar estados incompatibles, validar precondiciones, conservar estados necesarios para rollback y no continuar cuando falte información para una restauración segura.

### 8. Safe defaults

El comportamiento inicial debe ser conservador. Una aplicación no debe activar servicios sensibles, abrir puertos, borrar datos, reemplazar configuración válida o mantener privilegios elevados solo por comodidad.

Los cambios importantes deben ser explícitos y comprensibles.

### 9. Feedback inmediato y verificable

Después de una acción, la aplicación debe comprobar el estado real siempre que sea viable:

```text
acción
   ↓
validación
   ↓
resultado mostrado al usuario
```

Debe distinguirse entre operación completada, fallida, pendiente o no verificable.

### 10. Recuperación y rollback

Cuando una acción modifique configuración relevante debe evaluarse desde el diseño cómo conservar y restaurar el estado anterior. El rollback no debe ser una ocurrencia posterior a un fallo.

### 11. El usuario conserva el control

La aplicación debe ayudar sin apropiarse silenciosamente del sistema. Se evitan cambios ocultos, configuraciones irreversibles sin advertencia, procesos permanentes innecesarios y eliminación automática de configuraciones previas.

Cuando una decisión requiera contexto humano, el usuario conserva la decisión final.

### 12. Integración natural con el escritorio

Una aplicación interactiva debe sentirse parte de Debian/XFCE: aparecer en la categoría correcta del menú, usar un nombre comprensible, ejecutar sin terminal visible, respetar el tema GTK y reutilizar iconografía del sistema cuando sea suficiente.

Se debe evitar introducir Electron, un navegador embebido o una interfaz web local para una utilidad pequeña si una aplicación nativa resuelve mejor la tarea.

### 13. Legibilidad y jerarquía

La información debe priorizarse así: estado general → contexto actual → acción principal → estados secundarios → detalles técnicos.

Tipografía, espaciado y tamaño de controles deben favorecer lectura cómoda. No debe sacrificarse legibilidad únicamente para mostrar más información en una ventana.

### 14. Consistencia entre aplicaciones

Las aplicaciones SineOS deben compartir una lógica reconocible: nombres claros, estados visibles, acciones principales diferenciadas, confirmaciones coherentes, errores explicativos, detalles técnicos opcionales e instalación semejante.

No tienen que verse idénticas, pero sí sentirse parte del mismo sistema.

### 15. Practicidad sobre complejidad

Cada control debe justificar su presencia respondiendo: **¿ayuda al usuario a completar mejor la tarea?**

Una aplicación pequeña que resuelva correctamente una función es preferible a una interfaz compleja que intente administrar todo el sistema.

### 16. Prueba de uso cotidiano

Antes de declarar una aplicación terminada, el flujo principal debe poder realizarse sin consultar comandos, sin conocer archivos internos, sin interpretar logs, sin recordar parámetros técnicos y sin abrir una terminal.

La documentación sigue siendo obligatoria, pero no debe ser necesaria para comprender las acciones cotidianas de la interfaz.

### 17. Experiencia de instalación

La instalación también forma parte de la UX y debe tender a este flujo:

```text
obtener repositorio
    ↓
ejecutar instalador
    ↓
validar dependencias
    ↓
integrar aplicación
    ↓
encontrarla en el menú
```

El instalador debe explicar qué comprueba, qué falta, qué va a modificar, dónde queda la integración, cómo consultar el estado y cómo retirarla. Una dependencia faltante debe producir una instrucción clara y accionable, no un error críptico.

### 18. Criterio de experiencia terminada

La UX puede considerarse terminada cuando el propósito es evidente, el estado actual es comprensible, la acción principal es clara, las acciones inválidas están prevenidas, los cambios sensibles requieren confirmación, el resultado se valida y comunica, existe recuperación cuando corresponde, los detalles técnicos no dominan la interfaz, el uso normal no depende de terminal y la aplicación está integrada y documentada.

La estética importa para legibilidad, jerarquía y coherencia, pero nunca sustituye funcionalidad, seguridad ni claridad.

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
