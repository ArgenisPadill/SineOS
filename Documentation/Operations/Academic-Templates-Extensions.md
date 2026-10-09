# Extensiones académicas de Obsidian — Evaluación y Plan de clase

> **Fecha de documentación:** 09-10-2026.  
> **Ámbito:** SineOS / Knowledge Vault / Universidad de Xalapa.  
> **Estado:** plantillas generadas y entregadas; sintaxis revisada y pruebas simuladas disponibles. **No equivale a validación de ejecución en el Obsidian local**. La instalación/uso real debe certificarse desde el Vault.  
> **Política:** incorporación aditiva; no reemplazar ni alterar los siete templates originales, validados el 19-09-2026.

## 1. Inventario y fuentes de verdad

La base académica original sigue documentada en [Academic-Templates.md](Academic-Templates.md). Los siete templates históricos son `Materia.md`, `Unidad.md`, `Tarea.md`, `Actividad.md`, `Examen.md`, `Proyecto-Integrador.md` y `Etapa-Proyecto.md`.

Ampliaciones preparadas el 09-10-2026:

| Plantilla del Vault | Tipo de nota generada | Identificador | Ubicación del resultado | Estado de evidencia |
| --- | --- | --- | --- | --- |
| `Evaluacion.md` | `evaluacion` | `EVA-YYYYMMDD-XXXX` | `<Materia>/03-Evaluaciones/Evaluacion-Parcial-1.md`, `Evaluacion-Parcial-2.md` o `Evaluacion-Final.md` | Sintaxis comprobada; ejecución real pendiente de certificación |
| `Plan de clase.md` | `plan-de-clase` | `PLC-YYYYMMDD-XXXX` | `<Materia>/01-Planeacion/Plan de clase.md` | Sintaxis y pruebas simuladas comprobadas; ejecución real pendiente de certificación |

**Ubicación de los archivos ejecutables en Obsidian:** `01-Sistema/Templates/`, **dentro del Vault**, no dentro del checkout Git. Los documentos académicos reales permanecen en `${SINEOS_VAULT}`, separado de `${SINEOS_REPO}`. GitHub registra **contratos y procedimientos**, no sincroniza automáticamente el Vault ni sustituye su respaldo independiente. No asumir que el contenido o la versión del Vault coincide con la entrega de una conversación sin comparar archivos.

Referencias de integridad de las **versiones entregadas** (no son hashes verificados en el host del usuario):

- `Evaluacion.md`: SHA-256 `68722321de42e45c61090a3bf6e537cabb0d3e1e26d056ccfef8922c5d7de590`.
- `Plan de clase.md`: SHA-256 `c39c02fa5463a9f5dcd6d09f3b379f6fa4c8ed885ebe664386d2e09d5ea2a0f7`.

## 2. Ejecutar desde Ctrl + P, como los templates originales

**Requisito:** complemento comunitario **Templater** habilitado; el complemento nativo **Templates** no interpreta bloques `<%* ... %>` de Templater.

1. Guardar cada archivo `.md` en `01-Sistema/Templates/` de Obsidian.
2. En **Configuración → Templater**, comprobar **Template folder location** = `01-Sistema/Templates`.
3. En **Templater → Template Hotkeys**, añadir individualmente `Evaluacion.md` y `Plan de clase.md`. Esta opción registra comandos individuales para la paleta; no es obligatorio asignar atajos de teclado adicionales.
4. Abrir una **nota Markdown nueva y completamente vacía** con `Ctrl + N`.
5. Abrir la paleta de comandos con `Ctrl + P` y buscar el comando de **Templater** asociado a la plantilla deseada. El texto exacto puede variar según la versión instalada; elegir el que **inserta/ejecuta esa plantilla**.
6. Responder sus selectores/prompts: seleccionan una `00-Materia.md` válida, validan los datos y mueven solamente la nota temporal al directorio de la materia.
7. Comprobar los metadatos y vínculos del documento nuevo. No ejecutar sobre una materia, unidad, examen ni plan existente.

**Alternativa si el comando individual no está registrado:** `Ctrl + P → Templater: Open Insert Template modal`, seleccionar el archivo. Este comando genérico funciona sin Template Hotkey; **no es** el flujo directo preferido.

**No usar** `Templates: Insert template` para estas plantillas.

### Configuración de recuperación

Si los comandos no aparecen:

- confirmar que Templater está habilitado y que el directorio configurado coincide con el real;
- comprobar nombre exacto y extensión de las plantillas;
- comprobar que cada archivo figure en **Template Hotkeys**;
- cerrar/reabrir la paleta de comandos o recargar Obsidian;
- ejecutar sobre una nota nueva vacía, no directamente sobre el archivo plantilla.

## 3. Contrato de `Evaluacion.md`

### Relaciones y propiedades

Genera una nota `tipo: evaluacion` con identificador `EVA`, asociada directamente a **una Materia `MAT`** y a **una o más Unidades `UNI`** de esa Materia.

Propiedades centrales:

```yaml
tipo: evaluacion
id: "EVA-YYYYMMDD-XXXX"
estado: borrador
materia-id: "MAT-YYYYMMDD-XXXX"
materia: "..."
metodo: "examen" # o "exposicion"
momento: "parcial" # o "final"
numero: 1 # 2 o null si es final
titulo: "..."
unidades-id:
  - "UNI-YYYYMMDD-XXXX"
unidades:
  - 1
fecha-aplicacion: "DD-MM-AAAA"
duracion: "..."
valor: "..."
numero-reactivos: null # entero positivo si es examen
tipo-reactivos: ""
modalidad-exposicion: null # "individual" o "equipo"
integrantes: null # 1 o >=2 para exposición
creado: "DD-MM-AAAA"
```

`valor` es una cadena descriptiva (ej. `30 puntos` o `25%`), **no un cálculo automático de ponderaciones**.

### Restricciones

- Solo presenta materias `00-Materia.md` con `evaluacion: examen` o `evaluacion: mixto`, modalidad válida y carpeta `03-Evaluaciones/` existente.
- Periodos: **Escolarizado** = Parcial 1, Parcial 2 y Final; **Vespertino** = Parcial 1 y Final; **Sabatino** = Final. No genera extraordinarios.
- Pregunta qué Unidades válidas de la Materia cubrirá; exige al menos una y verifica `UNI.materia-id = MAT.id`.
- Elige `metodo: examen` o `metodo: exposicion`.
- Examen: exige número positivo de reactivos y tipo de reactivos; prepara apartados para instrucciones, reactivos, respuestas y criterios.
- Exposición: permite individual o equipo (mínimo dos integrantes en equipo); prepara consigna, evidencias y rúbrica **editable** de ejemplo 30/30/20/10/10, cuyo 100% corresponde al valor de la evaluación y **no** a toda la calificación de la asignatura.
- Valida la fecha de aplicación `DD-MM-AAAA` como fecha real.
- Detecta ocupación del periodo por nombre o metadatos, tanto en archivos heredados `Examen-*.md`/`EXA` como en nuevos `Evaluacion-*.md`/`EVA`. Evita IDs ya presentes y rehúsa sobrescribir.
- Solo mueve la nota **después** de verificar integridad, datos y destino.

### Compatibilidad con `Examen.md` heredado

**Importante: compatibilidad en un solo sentido.** `Evaluacion.md` reconoce los exámenes `EXA` anteriores, pero el viejo `Examen.md` no fue modificado para reconocer archivos `EVA`. Si ambos siguen accesibles en Template Hotkeys, invocar el comando antiguo después del nuevo podría generar un mismo periodo dos veces.

**Procedimiento recomendado:** para evaluaciones futuras utilizar `Evaluacion.md`, reservar `Examen.md` para consulta de notas previas y **retirar su comando de Template Hotkeys** si se adopta la nueva plantilla como única vía. Mantener intactos el archivo y las notas históricas. Una compatibilidad bidireccional requeriría una modificación futura revisada y probada, no realizada en esta entrega.

## 4. Contrato de `Plan de clase.md`

### Dependencia de Materia y destino

Genera **un plan por Materia**, a partir de una `00-Materia.md` existente con `MAT` válido y carpeta `01-Planeacion/`. El archivo final es exactamente:

```text
<Materia>/01-Planeacion/Plan de clase.md
```

No crea ni modifica Materias o Unidades. Impide crear un segundo plan para el mismo `materia-id` o sobrescribir la ruta exacta.

Propiedades centrales:

```yaml
tipo: plan-de-clase
id: "PLC-YYYYMMDD-XXXX"
estado: borrador
universidad: "Universidad de Xalapa"
docente: "Argenis Alain Gustavo Padilla Córdoba"
materia-id: "MAT-YYYYMMDD-XXXX"
materia: "..."
licenciatura: "..."
semestre: "..."
grupo: "..."
periodo: "2026-2027" # sugerencia editable
modalidad: "escolarizado"
turno: "Matutino"
bloque: ""
horas-semestre: 60
unidades: 4
semanas-por-unidad: 4
unidades-id: [] # solo las Unidades ya existentes
materias-anteriores: []
materias-posteriores: []
fecha-creacion: "DD-MM-AAAA"
```

Recupera universidad, materia, carrera/licenciatura, semestre, grupo, modalidad y bloque desde el YAML de Materia cuando estén disponibles. Pregunta lo faltante y los parámetros variables. Las **horas-semestre** deben ser positivas; número de Unidades y semanas por Unidad deben ser enteros de rango controlado. Para modalidad Escolarizado solicita turno (Matutino/Vespertino/Sabatino); Vespertino y Sabatino derivan directamente su turno.

### Secciones que genera

1. Encabezado **Universidad de Xalapa — Plan de clase**, datos generales y vínculo a Materia.
2. Objetivo general de la materia y perfil de egreso como **textos de apoyo por completar**.
3. Apartado por Unidad con título, fechas, horas, objetivo y vínculo, si existe `Unidad-N.md` válida.
4. Tabla semanal con **numeración continua entre unidades**, contenidos, conducción docente, trabajo independiente, recursos y evidencias.
5. Evaluación por momentos: Escolarizado (dos parciales y final), Vespertino (parcial y final), Sabatino (final), más renglones para extraordinarios 1 y 2.
6. Referencias por Unidad.
7. Lista de verificación de horas, fechas, semanas, actividades, porcentajes y bibliografía.
8. Observaciones y seguimiento docente.

La plantilla **permite planear antes de registrar todas las Unidades**, completando títulos y campos con marcadores para edición posterior. Los vínculos y el arreglo `unidades-id` se capturan **al momento de crear el plan**; agregar o editar Unidades después **no sincroniza automáticamente** la nota ya generada. No volver a ejecutar para «actualizar»: editar el plan existente.

### Límites importantes

- La distribución inicial **50% examen / 10% actividades / 40% proyecto integrador** es solo el **ejemplo recibido**, editable y marcado dentro de la nota. Debe ajustarse al programa de cada materia. No asumir que todas cuentan con proyecto integrador.
- Los extraordinarios del formato son **renglones documentales**, no exámenes creados ni ventanas de calendario certificadas.
- Las fechas de cada Unidad y las horas no se inventan; se heredan cuando existen o quedan pendientes. La suma de horas, calendario y bibliografía requieren **verificación docente manual**.
- La asignación homogénea de semanas por Unidad es un **esqueleto inicial**: ajustar manualmente si los periodos tienen duraciones diferentes.
- No genera cronograma institucional ni actualiza automáticamente Tareas, Actividades o Evaluaciones.

## 5. Requisitos transversales de seguridad

- **Nota temporal nueva y vacía.** No ejecutar sobre notas existentes.
- **Integridad padre-hijo.** ID de Materia y relaciones `MAT/UNI` antes de mover.
- **Sin sobrescrituras.** Validación de duplicados previa y final.
- **Sin mutaciones de padres.** `tp.file.move()` solo debe actuar sobre la nota temporal.
- **Sin datos sensibles en GitHub.** No publicar notas de estudiantes, calificaciones, secretos, rutas privadas completas ni contenidos confidenciales del Vault.
- **El Vault permanece independiente de GitHub.** La documentación versionada no es backup ni evidencia de restauración de estas notas; usar el mecanismo de respaldo del Knowledge Vault definido por SineOS.
- Ante incompatibilidades, **fallar de forma segura** y conservar el original; no «reparar» los siete templates históricos sin defecto reproducible y pruebas.

## 6. Evidencias y matriz de validación

### Evidencia disponible para las entregas de 09-10-2026

| Verificación | Evaluacion.md | Plan de clase.md |
| --- | --- | --- |
| Sintaxis JavaScript en bloque Templater | Comprobada fuera del host | Comprobada fuera del host |
| Pruebas simuladas de modalidades | Sin evidencia consolidada en esta auditoría | Escolarizado, Vespertino y Sabatino: satisfactorias |
| Bloqueo de duplicados | Previsto en código; pendiente certificación in situ | Simulado satisfactoriamente |
| Bloqueo de nota no vacía | Previsto en código; pendiente certificación in situ | Simulado satisfactoriamente |
| Creación real mediante `Ctrl+P` y Template Hotkeys | **Pendiente de validar en Obsidian** | **Pendiente de validar en Obsidian** |
| Recuperación/restore real de estos artefactos | No evaluado | No evaluado |

### Prueba de aceptación pendiente en el Vault

1. Confirmar el hash de cada archivo entregado (si se usó exactamente esa versión) y el registro en Template Hotkeys.
2. Ejecutar desde nota nueva; seleccionar una Materia real y una o varias Unidades válidas.
3. Crear una Evaluación de prueba; verificar `EVA`, YAML, vínculo a `MAT/UNI` y destino correcto.
4. Repetir el mismo momento; comprobar bloqueo sin modificar padres.
5. En una Materia de prueba sin plan, generar `Plan de clase`; comprobar `PLC`, ruta única, semanas y columnas.
6. Intentar un segundo plan y ejecutar sobre nota no vacía; comprobar ambos bloqueos.
7. Confirmar que **ninguno de los siete templates previos** fue modificado.
8. Registrar la fecha, versión exacta, evidencias y resultado; recién entonces actualizar el estado a «validado en Obsidian».

No ejecutar pruebas destructivas sobre materias reales con información vigente: crear una Materia de laboratorio o utilizar un Vault de prueba respaldado.

## 7. Evolución posterior, sin afectar prioridades maestras

- Decidir si `Evaluacion.md` reemplazará operativamente el comando de `Examen.md` o si se implementará compatibilidad bidireccional.
- Incorporar validación de pruebas reales e instalabilidad reproducible para los dos nuevos templates.
- Considerar más adelante rúbricas configurables y planeaciones con duraciones variables por Unidad; **no están implementadas**.
- Mantener sin cambios los gates de Seguridad → SDE y el inventario anterior de deuda y pendientes. La mejora académica es **aditiva**, no redefine ese roadmap.
