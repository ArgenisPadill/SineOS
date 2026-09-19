# SineOS — Sistema académico de Obsidian

## Estado

**Validado funcionalmente: 19-09-2026**

Los siete templates académicos se consideran estables:

- `Materia.md`
- `Unidad.md`
- `Tarea.md`
- `Actividad.md`
- `Examen.md`
- `Proyecto-Integrador.md`
- `Etapa-Proyecto.md`

Ubicación en el Vault:

`01-Sistema/Templates/`

## Modelo académico

```text
Materia/
├── 00-Materia.md
├── 01-Planeacion/
├── 02-Unidades/
│   └── Unidad-N/
│       ├── Unidad-N.md
│       ├── Tareas/
│       └── Actividades/
├── 03-Evaluaciones/
├── 04-Proyecto-Integrador/
│   ├── 00-Proyecto-Integrador.md
│   └── Etapas/
└── 05-Recursos/
```

`03-Evaluaciones/` solo se crea cuando la materia utiliza examen o evaluación mixta.

`04-Proyecto-Integrador/` solo se crea cuando utiliza Proyecto Integrador o evaluación mixta.

## Relaciones

### Actividades académicas

```text
MAT
└── UNI
    ├── TAR
    └── ACT
```

Una Tarea o Actividad conserva tanto el ID de la Unidad como el ID de la Materia.

### Proyecto Integrador

```text
MAT
└── PRO
    └── ETA
        └── UNI
```

Cada Etapa pertenece a:

- una Materia;
- un Proyecto Integrador;
- exactamente una Unidad.

Regla fundamental:

`1 PRO + 1 UNI = máximo 1 ETA`

## Seguridad de los templates hijos

Los templates hijos deben ejecutarse desde una nota temporal nueva y vacía.

Flujo seguro:

1. Crear una nota nueva.
2. Mantener activa la nota vacía.
3. Ejecutar `Templater: Open Insert Template modal`.
4. Seleccionar el template correspondiente.
5. Seleccionar el padre válido.
6. Leer y validar metadatos y estructura física.
7. Validar los datos introducidos.
8. Comprobar duplicados.
9. Mover la nota temporal únicamente después de superar las validaciones.

Los templates hijos no deben mover ni modificar las notas padre.

Ante el aviso de Obsidian para actualizar enlaces internos, se utiliza **Siempre actualizar**.

## Materia

`Materia.md` constituye la raíz de una materia académica.

Genera un identificador `MAT` y solicita el contexto necesario:

- materia;
- carrera;
- grupo;
- año;
- semestre;
- universidad;
- nivel;
- modalidad;
- bloque cuando aplica;
- fecha de inicio;
- fecha de término;
- sistema de evaluación.

La materia crea dinámicamente el árbol académico requerido. No se precrean años, semestres, modalidades ni bloques.

Siempre crea:

- `01-Planeacion/`
- `02-Unidades/`
- `05-Recursos/`

Crea `03-Evaluaciones/` cuando el sistema de evaluación es Examen o Mixto.

Crea `04-Proyecto-Integrador/` cuando el sistema de evaluación es Proyecto Integrador o Mixto.

La nota principal se almacena como:

`00-Materia.md`

## Unidad

`Unidad.md` depende de una Materia válida.

Su relación fundamental es:

```yaml
tipo: unidad
id: "UNI-..."
materia-id: "MAT-..."
unidad: N
```

El número académico de la Unidad se almacena en el campo `unidad`.

Cada Unidad genera:

```text
Unidad-N/
├── Unidad-N.md
├── Actividades/
└── Tareas/
```

El template valida la existencia e integridad de la Materia antes de crear la Unidad.


## Tarea

`Tarea.md` depende de una Unidad válida.

Genera un identificador `TAR` y hereda automáticamente:

- `materia-id`;
- `unidad-id`;
- materia;
- número de Unidad;
- contexto académico correspondiente.

La Tarea se almacena dentro de:

`02-Unidades/Unidad-N/Tareas/`

El template solicita y valida:

- número de tarea;
- título;
- objetivo;
- consigna;
- fecha de entrega;
- valor.

Antes de mover la nota temporal comprueba la integridad de la Materia, la Unidad y la existencia de duplicados.

## Actividad

`Actividad.md` depende de una Unidad válida.

Genera un identificador `ACT` y hereda:

- `materia-id`;
- `unidad-id`;
- materia;
- número de Unidad;
- contexto académico.

La Actividad se almacena dentro de:

`02-Unidades/Unidad-N/Actividades/`

El template solicita:

- número de actividad;
- título;
- objetivo;
- modalidad;
- integrantes;
- duración;
- material;
- valor.

El material se almacena en el cuerpo de la nota y no en YAML.

El template protege las notas estructurales y únicamente puede ejecutarse de forma segura desde una nota temporal vacía.

## Examen

`Examen.md` genera identificadores `EXA`.

Un Examen pertenece directamente a una Materia, pero puede cubrir una o varias Unidades.

Modelo:

```yaml
tipo: examen
id: "EXA-..."
materia-id: "MAT-..."
unidades-id:
  - "UNI-..."
  - "UNI-..."
```

No se asume una correspondencia fija entre Parcial y Unidad. El usuario selecciona explícitamente las Unidades cubiertas por el examen.

### Exámenes permitidos por modalidad

**Escolarizado**

- Parcial 1
- Parcial 2
- Final

**Vespertino**

- Parcial 1
- Final

**Sabatino**

- Final

Las materias con evaluación `Mixto` siguen las mismas restricciones de su modalidad.

Las materias cuya evaluación es exclusivamente `Proyecto integrador` quedan excluidas de la creación de exámenes.

## Proyecto Integrador

`Proyecto-Integrador.md` genera un identificador `PRO`.

Solo puede utilizarse en materias cuyo sistema de evaluación sea:

- Proyecto integrador;
- Mixto.

El Proyecto puede ser:

- Individual;
- Equipo.

En modalidad Equipo se requieren como mínimo dos integrantes.

La estructura utilizada es:

```text
04-Proyecto-Integrador/
├── 00-Proyecto-Integrador.md
└── Etapas/
```

El Proyecto define:

- título;
- objetivo;
- descripción;
- producto final;
- modalidad;
- integrantes;
- fecha de inicio;
- fecha de término;
- valor total.

El Proyecto no crea Etapas automáticamente.

No se almacena un campo persistente `numero-etapas`.

Tampoco se almacenan como fuente de verdad valores dinámicos de puntos distribuidos o pendientes. Estos se calculan a partir de las Etapas existentes.

## Etapa de Proyecto

`Etapa-Proyecto.md` genera un identificador `ETA`.

Cada Etapa está relacionada simultáneamente con:

- una Materia `MAT`;
- un Proyecto `PRO`;
- una Unidad `UNI`.

Contrato principal:

```yaml
tipo: etapa-proyecto
id: "ETA-YYYYMMDD-XXXX"
estado: pendiente
materia-id: "MAT-..."
materia: "..."
proyecto-id: "PRO-..."
proyecto: "..."
unidad-id: "UNI-..."
unidad: N
numero: N
titulo: "..."
fecha-entrega: "DD-MM-AAAA"
valor: 10
creado: "DD-MM-AAAA"
```

`unidad` representa el número de la Unidad académica.

`numero` representa el número secuencial de la Etapa.

Son conceptos independientes.

El número de Etapa se determina automáticamente mediante:

`max(ETA.numero existentes) + 1`

Una misma combinación Proyecto + Unidad solo puede tener una Etapa:

`1 PRO + 1 UNI = máximo 1 ETA`

## Reglas de calificación de Etapas

No existe un número fijo de Etapas por Proyecto.

La suma de los valores de todas las Etapas debe cumplir:

`Σ ETA.valor <= PRO.valor`

Antes de crear una nueva Etapa se calcula:

`disponible = PRO.valor - Σ ETA.valor existentes`

Y debe cumplirse:

`ETA.valor <= disponible`

Si el Proyecto alcanza su valor total, no pueden crearse nuevas Etapas evaluables.

Aunque todavía existan puntos disponibles, tampoco puede crearse otra Etapa si todas las Unidades disponibles ya tienen una ETA asociada al mismo Proyecto.

## Reglas de fechas

La fecha de entrega de una Etapa debe encontrarse dentro del intervalo definido por el Proyecto:

`PRO.fecha-inicio <= ETA.fecha-entrega <= PRO.fecha-fin`

No se obliga a que la fecha de entrega se encuentre dentro del intervalo de la Unidad.

Esto permite que una entrega correspondiente a una Unidad pueda realizarse después de su cierre formal, siempre que continúe dentro del periodo del Proyecto.

## Integridad y validaciones

Antes de crear una Etapa se comprueba:

- existencia de un Proyecto válido;
- existencia de la Materia padre;
- integridad de `MAT.id`;
- integridad de `PRO.materia-id`;
- existencia de Unidades pertenecientes a la misma Materia;
- relación `UNI.materia-id == PRO.materia-id == MAT.id`;
- disponibilidad de puntos;
- ausencia de una ETA previa para la combinación PRO + UNI;
- validez de las Etapas existentes;
- fecha de entrega dentro del intervalo del Proyecto;
- ausencia de IDs duplicados;
- ausencia de números de Etapa duplicados.

Ante una ETA existente corrupta o inconsistente, el template utiliza un comportamiento **fail-closed** y evita continuar silenciosamente.

## Incidencia encontrada durante la validación

Durante la primera prueba funcional de `Etapa-Proyecto.md`, el sistema informó:

`No hay PRO válido con valor disponible y Unidad sin ETA.`

La inspección confirmó que la Materia, el Proyecto, la Unidad y sus rutas físicas eran correctos.

El problema estaba en dos referencias del template:

```javascript
fmUnidad.numero
fmUnidadActual.numero
```

Sin embargo, el contrato establecido por `Unidad.md` utiliza el campo:

```javascript
unidad
```

Por lo tanto, las referencias correctas son:

```javascript
fmUnidad.unidad
fmUnidadActual.unidad
```

Después de corregir ambas referencias, la selección de Unidades funcionó correctamente.

SHA-256 de la versión funcionalmente validada de `Etapa-Proyecto.md`:

```text
75bfeb327fdc5ee04a54f55eb0fb66de409b6559794399ade51bebb8ac5a5218
```

## Prueba funcional del Proyecto Integrador

Proyecto utilizado:

```text
PRO-20260919-3B4N
Valor total: 40
```

### Etapa 1

```text
ID: ETA-20260919-PU4M
Unidad: 1
Número de Etapa: 1
Valor: 10
Título: Definición de requerimientos
```

Resultado:

- creación correcta;
- relaciones MAT/PRO/UNI correctas;
- ruta física correcta;
- segundo intento sobre la misma Unidad bloqueado correctamente.

### Etapa 2

```text
ID: ETA-20260919-JMZG
Unidad: 2
Número de Etapa: 2
Valor: 15
Título: Diseño de la arquitectura del sistema
```

Después de la Etapa 1, el sistema calculó correctamente:

`40 - 10 = 30 puntos disponibles`

Después de la Etapa 2:

`40 - 10 - 15 = 15 puntos disponibles`

### Etapa 3

Se creó una tercera Unidad para comprobar el límite final del Proyecto.

Con 15 puntos disponibles se intentó asignar:

`16`

El template rechazó correctamente el valor por exceder el disponible.

Posteriormente se asignaron:

`15`

La Etapa fue creada correctamente con:

```text
ID: ETA-20260919-MBY8
Número de Etapa: 3
Valor: 15
```

El título introducido durante esta prueba fue accidental y corresponde únicamente a datos de prueba; no representa un defecto del template.

## Resultado de la batería funcional

Distribución final:

```text
Etapa 1: 10
Etapa 2: 15
Etapa 3: 15
----------------
Total:   40 / 40
```

Se validó correctamente:

- numeración secuencial automática;
- relación Proyecto → Unidad;
- relación Materia → Proyecto → Etapa → Unidad;
- exclusión de una Unidad después de recibir una ETA;
- cálculo acumulativo de calificación;
- rechazo de valores superiores al disponible;
- aceptación exacta del valor restante;
- bloqueo de nuevas Etapas cuando el disponible llega a cero;
- protección de las notas padre;
- movimiento de la nota temporal únicamente después de las validaciones.

## Estado final de los templates

```text
Materia               OK
Unidad                OK
Tarea                 OK
Actividad              OK
Examen                 OK
Proyecto Integrador    OK
Etapa Proyecto         OK
```

Los siete templates académicos quedan funcionalmente cerrados.

No deben modificarse salvo que durante su utilización real se identifique un defecto reproducible.
