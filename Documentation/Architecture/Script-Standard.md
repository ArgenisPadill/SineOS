# SineOS — Estándar de scripts y automatización

**Decisión congelada:** 23-09-2026  
**Estado:** Adoptado

## Propósito

Los scripts forman parte de la infraestructura de SineOS.

No deben tratarse como fragmentos temporales sin contexto cuando contienen conocimiento necesario para reconstruir, operar, diagnosticar, migrar o recuperar el sistema.

A partir de esta decisión, todo script relevante debe clasificarse, documentarse y conservarse de acuerdo con su función y ciclo de vida.

## Principio

> Un comando repetido manualmente es candidato a script. Un script que sostiene una función de SineOS es infraestructura y debe versionarse, documentarse y validarse.

No todo script generado durante una sesión merece permanecer para siempre. El objetivo es conservar conocimiento operativo útil, no acumular archivos.

## Clasificación

### 1. Script pilar

Es parte estructural de SineOS. Debe conservarse mientras el componente exista.

Características habituales:
- permite reconstruir una configuración;
- instala o integra un componente;
- automatiza una función estable;
- evita una secuencia compleja de pasos manuales;
- contiene lógica que sería costoso reconstruir;
- forma parte de la operación normal del sistema.

Ejemplos actuales:
- `Scripts/Desktop/sineos-xfce-macos.sh`
- `Scripts/NetworkPrivacy/install-network-privacy.sh`

### 2. Script operativo recurrente

Se ejecuta periódicamente o cuando se necesita comprobar u operar el sistema.

Ejemplos:
- auditorías;
- health checks;
- monitoreo;
- mantenimiento;
- sincronización;
- backup;
- restauración.

Debe ser seguro para el patrón de uso previsto e idempotente cuando tenga sentido.

Ejemplos actuales:
- `Scripts/Audit/sineos-audit.sh`
- `Scripts/Monitoring/check-open-webui.sh`
- `Scripts/Monitoring/check-postgresql.sh`

### 3. Script de instalación o integración

Existe para instalar, registrar o conectar un componente con el sistema.

Debe documentar requisitos, dependencias, archivos creados, permisos, cambios realizados, validación y desinstalación o reversión cuando corresponda.

### 4. Script de migración

Se utiliza para transformar un estado conocido de SineOS a otro.

Puede ejecutarse una sola vez, pero merece conservarse cuando documenta una migración relevante, permite repetirla en otro equipo, explica una transformación importante o puede ser necesaria durante recuperación.

Debe indicar claramente:

```text
Estado: migración
Origen:
Destino:
Fecha:
Reejecutable: sí/no
Riesgos:
Rollback:
```

### 5. Script de una sola ejecución

Un script usado una vez no se conserva automáticamente.

Debe conservarse solamente si tiene valor futuro como evidencia técnica, procedimiento de reparación, migración reproducible, recuperación o investigación de una incidencia relevante.

Si su contenido ya quedó reemplazado por una implementación estable y no aporta conocimiento adicional, puede eliminarse; Git conserva su historial.

### 6. Script experimental

Pruebas rápidas, diagnósticos ad hoc o experimentos no deben presentarse como componentes soportados.

Mientras sean experimentales deben identificarse como tales, no formar parte de procedimientos oficiales y promoverse a una categoría estable solo después de validación.

## Ubicación

La estructura debe seguir la función real:

```text
Scripts/
├── Audit/
├── Desktop/
├── Monitoring/
├── NetworkPrivacy/
├── Backup/          # cuando exista implementación real
├── Recovery/        # cuando exista implementación real
└── Migrations/      # cuando exista una migración que merezca conservarse
```

No se crean directorios vacíos como scaffolding.

## Requisitos mínimos de un script estable

Todo script considerado pilar, recurrente o de instalación debe documentar como mínimo:
- nombre;
- propósito;
- estado;
- plataforma objetivo;
- dependencias;
- privilegios requeridos;
- entradas;
- salidas;
- archivos o servicios que modifica;
- si es seguro volver a ejecutarlo;
- validación posterior;
- riesgos;
- recuperación o rollback cuando aplique.

Cuando el propio archivo sea pequeño, esta información puede estar en su encabezado. La documentación completa debe vivir en el documento operativo correspondiente o en el catálogo de scripts.

## Encabezado recomendado

```bash
#!/usr/bin/env bash

# SineOS
# Nombre:
# Propósito:
# Categoría:
# Estado:
# Plataforma:
# Reejecutable:
# Privilegios:
# Documentación:
```

## Seguridad

Un script SineOS debe aplicar los mismos principios que una aplicación:
- mínimo privilegio;
- no ejecutar como root si no es necesario;
- no incrustar secretos;
- no imprimir secretos;
- no borrar datos silenciosamente;
- comprobar precondiciones;
- fallar de forma comprensible;
- validar el resultado;
- conservar rollback cuando sea razonable;
- evitar cambios ajenos a su propósito.

Los scripts de auditoría deben ser de solo lectura salvo que indiquen explícitamente lo contrario.

## Idempotencia

Cuando una tarea pueda ejecutarse varias veces, debe diseñarse para que una segunda ejecución no destruya ni duplique configuración.

Si un script no es idempotente, debe declararlo.

## Dry-run

Las operaciones sensibles deberían ofrecer un modo de inspección o validación previa cuando resulte práctico.

No se exige `--dry-run` a todos los scripts, pero debe considerarse para migraciones, borrado, cambios masivos, recuperación, permisos, red y almacenamiento.

## Salida

La salida debe ser útil para una persona. Se recomienda distinguir `OK`, `INFO`, `WARN` y `ERROR`.

Los errores deben explicar la causa y, cuando sea posible, la siguiente acción.

## Relación con aplicaciones nativas

Un script puede evolucionar a aplicación cuando la operación se vuelve frecuente e interactiva.

La arquitectura preferida puede ser:

```text
interfaz gráfica
      ↓
lógica operativa
      ↓
herramientas del sistema
```

La GUI no debe esconder una automatización frágil; la lógica debe seguir siendo verificable.

## Documentación

Todo script estable debe aparecer en `Scripts/README.md` y, cuando forma parte de un componente mayor, en su documentación bajo `Documentation/Operations/`.

El catálogo debe indicar clasificación, estado, propósito, frecuencia, riesgo y documentación relacionada.

## Regla para scripts históricos

Cuando se descubra un script antiguo fuera del repositorio, antes de publicarlo se debe decidir:

1. ¿Sigue siendo válido?
2. ¿Contiene secretos, rutas privadas o identificadores?
3. ¿Su función ya está cubierta por otra herramienta?
4. ¿Es reproducible?
5. ¿Tiene valor operativo, de recuperación o histórico?

Solo después de esa revisión se incorpora.

No se publican automáticamente scripts antiguos solo por conservarlos.

## Criterio de terminado

Un script se considera integrado correctamente en SineOS cuando:
- está en la ubicación adecuada;
- su función es clara;
- su categoría está definida;
- está versionado;
- no contiene información sensible;
- sus dependencias son conocidas;
- se sabe si puede volver a ejecutarse;
- se ha validado;
- existe documentación suficiente;
- existe recuperación cuando el riesgo lo requiere.

## Aplicaciones y scripts

SineOS adopta dos principios complementarios:

> La terminal es excelente para construir, diagnosticar y administrar.

> Las tareas repetitivas deben automatizarse y, cuando una interacción gráfica mejore realmente la operación, esa automatización puede evolucionar a una aplicación nativa.

De esta forma SineOS conserva la potencia de Linux sin convertir el uso cotidiano en una colección de comandos que haya que recordar.