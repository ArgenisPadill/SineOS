# SineOS — Miyo

## 1. Propósito

Este documento describe el papel, instalación y operación de Miyo dentro de SineOS.

Miyo constituye la capa de recuperación semántica del Knowledge Vault de Obsidian.

Su función principal es permitir que agentes y modelos de lenguaje encuentren conocimiento relevante dentro del Vault sin depender exclusivamente de coincidencias exactas de palabras.

Principio:

> Obsidian conserva el conocimiento. Miyo permite encontrarlo semánticamente.

Miyo no sustituye a Obsidian ni constituye la fuente de verdad de SineOS.

---

## 2. Arquitectura

El flujo conceptual es:

```text
Usuario
   ↓
Agente
   ↓
miyo-search
   ↓
Miyo CLI
   ↓
Servicio Miyo
   ↓
Índice semántico
   ↓
Knowledge Vault
   ↓
Notas relevantes
```

Los resultados recuperados pueden utilizarse posteriormente como contexto para un modelo de lenguaje.

Flujo validado con DeepSeek:

```text
DeepSeek
   ↓
Copilot / OpenCode
   ↓
miyo-search
   ↓
Miyo CLI
   ↓
Servicio Miyo
   ↓
Índice semántico
   ↓
Vault de Obsidian
```

---

## 3. Knowledge Vault

El Vault utilizado por Miyo es:

```text
${SINEOS_VAULT}
```

Este directorio constituye la fuente de conocimiento permanente del sistema.

Miyo debe tratar el Vault como una fuente externa de conocimiento y no modificar arbitrariamente su estructura.

La arquitectura del Vault está documentada en:

```text
Documentation/Architecture/Knowledge-Vault.md
```

---

## 4. Versión validada

Versión utilizada durante la construcción inicial de SineOS:

```text
Miyo 0.2.27
```

Esta versión fue validada funcionalmente con el Knowledge Vault.

Una actualización futura debe comprobar nuevamente:

- inicio de la aplicación;
- acceso al Vault;
- funcionamiento del servicio;
- funcionamiento del CLI;
- búsqueda semántica;
- integración con agentes.

---

## 5. AppImage

Miyo se utiliza mediante AppImage.

Ubicación:

```text
~/.local/opt/miyo/Miyo.AppImage
```

Esta ubicación permite mantener aplicaciones locales del usuario fuera de los directorios del sistema.

La AppImage constituye la aplicación principal de Miyo.

---

## 6. Scope de indexación

El scope configurado es:

```text
${SINEOS_VAULT}
```

Miyo debe indexar el Knowledge Vault y no el repositorio Git de SineOS.

Separación:

```text
${SINEOS_REPO}
        ↓
Git / código / infraestructura / documentación técnica

${SINEOS_VAULT}
        ↓
Knowledge Vault / conocimiento / memoria
```

Esta separación es deliberada.

---

## 7. Búsqueda semántica

La búsqueda semántica fue validada correctamente desde CLI.

Esto permite recuperar notas relevantes incluso cuando la consulta no utiliza exactamente las mismas palabras almacenadas en el documento.

Conceptualmente:

```text
consulta
   ↓
embedding / representación semántica
   ↓
índice Miyo
   ↓
notas relacionadas por significado
```

Esto diferencia la búsqueda semántica de una búsqueda tradicional basada únicamente en texto exacto.

---

## 8. Miyo CLI

Miyo Desktop incluye un CLI para consultar el índice semántico desde terminal y para permitir su integración con otras herramientas.

En Linux, Miyo administra el acceso al CLI mediante:

```text
~/.miyo/bin/miyo
```

Esta ruta es un enlace simbólico administrado por Miyo Desktop hacia el ejecutable incluido en el montaje activo de la AppImage.

El CLI fue validado mediante:

```bash
~/.miyo/bin/miyo --help
~/.miyo/bin/miyo files
~/.miyo/bin/miyo search "consulta"
```

---

## 9. Servicio local

El CLI funciona como cliente del servicio local administrado por Miyo Desktop.

```text
Miyo Desktop
      ↓
Servicio local
127.0.0.1:8742
      ↓
Miyo CLI
      ↓
Índice semántico
      ↓
Knowledge Vault
```

Durante la validación se comprobó que el servicio escucha en `127.0.0.1:8742`.

El CLI necesita que Miyo Desktop y su servicio estén ejecutándose para consultar el índice. Si el servicio no está disponible puede aparecer:

```text
Cannot connect to Miyo service at http://127.0.0.1:8742
```

Este mensaje indica que el servicio local no está disponible; no implica por sí mismo corrupción del Vault ni del índice.

---

## 10. Gestión del CLI

Miyo Desktop administra automáticamente:

```text
~/.miyo/bin/miyo
```

El enlace puede apuntar a una ruta temporal similar a:

```text
/tmp/.mount_Miyo.XXXXXX/resources/bin/service/miyo/miyo
```

Esto forma parte del funcionamiento de la AppImage mientras Miyo Desktop está ejecutándose.

No debe sustituirse permanentemente este enlace por una copia manual del ejecutable.

Después de una actualización debe comprobarse que la AppImage inicia, el servicio local está disponible, el CLI responde y el índice continúa accesible.

La gestión del enlace del CLI corresponde a Miyo Desktop.

---

## 11. Integración con Copilot / OpenCode

Miyo se utiliza como herramienta de recuperación para agentes.

El agente puede solicitar una búsqueda semántica antes de responder una pregunta relacionada con información almacenada en el Vault.

Flujo:

```text
Pregunta
   ↓
Copilot / OpenCode
   ↓
miyo-search
   ↓
Miyo
   ↓
Vault
   ↓
contexto recuperado
   ↓
LLM
   ↓
respuesta
```

Esto permite separar:

```text
memoria permanente → Obsidian
recuperación        → Miyo
orquestación        → agente
razonamiento        → LLM
```

---

## 12. Integración validada con DeepSeek

La integración completa fue probada utilizando DeepSeek.

Flujo validado:

```text
DeepSeek
   ↓
Copilot / OpenCode
   ↓
miyo-search
   ↓
Miyo CLI
   ↓
Servicio Miyo
   ↓
Índice semántico
   ↓
Vault
```

La prueba confirmó que el modelo puede utilizar información recuperada desde el Knowledge Vault mediante la capa de herramientas.

Esto constituye una pieza fundamental del concepto de segundo cerebro de SineOS.

---

## 13. Integración con Gemini

Gemini 3.8 Flash fue validado como modelo cloud principal para trabajo agentic.

Puede utilizar el conocimiento recuperado mediante las herramientas asociadas al Vault.

Gemini no sustituye a Miyo.

Responsabilidades:

```text
Miyo
    encuentra conocimiento

Gemini
    interpreta y razona sobre el contexto recuperado
```

---

## 14. Modelos locales

Los modelos locales utilizados mediante Ollama pueden trabajar con información recuperada desde el Vault.

Sin embargo, durante las pruebas los modelos locales pequeños de aproximadamente 2B–3B parámetros mostraron limitaciones cuando se combinaban con:

- prompts agentic grandes;
- múltiples herramientas;
- contextos extensos;
- ciclos complejos de llamadas.

Por esta razón Miyo puede utilizarse con modelos locales, pero el hecho de que la recuperación funcione no implica que el modelo local tenga capacidad suficiente para ejecutar cualquier workflow agentic.

---

## 15. Miyo y privacidad

Miyo permite mantener localmente:

- Vault;
- índice;
- búsqueda semántica;
- recuperación de conocimiento.

Esto ayuda a reducir la necesidad de enviar colecciones completas de notas a proveedores externos.

Cuando se utilice un modelo cloud, debe proporcionarse únicamente el contexto necesario para resolver la tarea.

Principio:

> Recuperar localmente y compartir únicamente el contexto necesario.

---

## 16. Miyo no es la memoria

Miyo no debe considerarse la memoria primaria de SineOS.

La memoria permanente está formada por archivos legibles y transportables almacenados en Obsidian.

```text
Obsidian
   ↓
fuente de verdad

Miyo
   ↓
índice derivado
```

Esto significa que el índice de Miyo debe poder reconstruirse.

La pérdida del índice no debe equivaler a la pérdida del conocimiento.

---

## 17. Portabilidad

La arquitectura está diseñada para permitir una futura migración de equipo.

Los elementos importantes son:

```text
Knowledge Vault
Miyo AppImage
configuración necesaria
procedimiento de instalación
procedimiento de indexación
```

El índice debe considerarse reconstruible.

La prioridad de backup corresponde al Vault, no al índice derivado.

---

## 18. Limpieza y validación del índice

Las notas temporales utilizadas durante las pruebas iniciales y las estructuras académicas creadas exclusivamente para validar los templates fueron eliminadas del Knowledge Vault.

Después de la limpieza se verificó el índice mediante:

```bash
~/.miyo/bin/miyo files
```

Resultado validado:

```text
Showing 25 of 25 file(s)
```

Los documentos de prueba eliminados ya no aparecen en el índice. Esto confirma que el watcher de Miyo reflejó correctamente las eliminaciones realizadas en el Vault.

---

## 19. Próxima batería semántica

La siguiente validación importante debe utilizar al menos dos notas relacionadas.

La prueba debe comprobar:

### Recuperación conceptual

Encontrar información sin utilizar necesariamente las palabras exactas presentes en las notas.

### Síntesis entre notas

Recuperar información procedente de dos documentos y construir una respuesta coherente.

### Recuperación de decisiones

Consultar una decisión anterior almacenada en el Vault.

### Consulta técnica previa a una acción

Antes de proponer una acción administrativa sobre SineOS, recuperar documentación relevante del sistema.

### Separación memoria/modelo

Comprobar que la respuesta dependa del contenido recuperado y no únicamente del conocimiento general del modelo.

---

## 20. Validación recomendada después de actualizar Miyo

Después de cualquier actualización significativa debe verificarse:

```text
[ ] La AppImage inicia
[ ] El Vault está configurado
[ ] El scope es correcto
[ ] El servicio funciona
[ ] El CLI funciona
[ ] El CLI corresponde a la versión instalada
[ ] La búsqueda semántica devuelve resultados
[ ] Las notas nuevas son indexadas
[ ] Las notas eliminadas desaparecen del índice
[ ] Copilot/OpenCode puede utilizar miyo-search
[ ] Un modelo cloud puede consumir el contexto recuperado
```

---

## 21. Seguridad

No deben almacenarse en este documento:

- API keys;
- tokens;
- contraseñas;
- secretos de proveedores.

Miyo debe tener acceso únicamente a los directorios necesarios para cumplir su función.

El Knowledge Vault puede contener información privada y debe tratarse como información local sensible.

---

## 22. Troubleshooting

### La aplicación funciona pero el CLI no

Comprobar primero que Miyo Desktop esté ejecutándose y que exista el servicio local:

```bash
ss -ltnp | grep ':8742'
~/.miyo/bin/miyo --help
~/.miyo/bin/miyo files
```

Si `~/.miyo/bin/miyo` es un enlace simbólico hacia `/tmp/.mount_Miyo.*`, esto es compatible con el funcionamiento observado de la AppImage mientras Miyo Desktop está activo.

### El CLI no puede conectarse

Si aparece `Cannot connect to Miyo service at http://127.0.0.1:8742`, comprobar que Miyo Desktop esté ejecutándose y que el servicio escuche en `127.0.0.1:8742`.

### Una búsqueda no encuentra una nota reciente

Comprobar:

1. que la nota esté dentro del scope;
2. que Miyo Desktop esté ejecutándose;
3. que el índice haya procesado el cambio;
4. que la consulta tenga relación semántica suficiente con el contenido.

### El agente no encuentra información que Miyo sí encuentra

Separar el diagnóstico:

```text
Miyo CLI
   ↓
miyo-search
   ↓
agente
   ↓
modelo
```

Probar cada capa independientemente evita atribuir al índice un problema perteneciente al agente o al modelo.

### Miyo se actualizó y el CLI dejó de funcionar

Comprobar que la nueva AppImage inicia, que el servicio local está disponible, que `~/.miyo/bin/miyo` existe, que el CLI responde y que el índice continúa accesible.

No extraer ni mantener manualmente una copia independiente del CLI como procedimiento normal.

---

## 23. Estado actual

| Componente | Estado |
|---|---|
| Miyo AppImage | Operativo |
| Knowledge Vault | Operativo y limpio |
| Scope del Vault | Configurado |
| Indexación semántica | Validada |
| Watcher de cambios | Validado |
| Eliminación del índice | Validada |
| Servicio local | Operativo en 127.0.0.1:8742 |
| Miyo CLI | Operativo |
| Gestión del CLI | Administrada por Miyo Desktop |
| Copilot/OpenCode | Integrado |
| DeepSeek + Miyo | Validado |
| Gemini + Vault | Validado |
| Batería semántica multinota | Pendiente |

---

## 24. Deuda técnica

Pendientes relacionados directamente con Miyo:

```text
[ ] Documentar procedimiento reproducible de reinstalación
[ ] Definir autostart si resulta necesario
[ ] Ejecutar benchmark semántico multinota
[ ] Incorporar pruebas de recuperación al mantenimiento de SineOS
```

La sincronización manual entre AppImage y CLI no se considera una deuda técnica, ya que Miyo Desktop administra el enlace utilizado para acceder al CLI.

---

## 25. Principios operativos

### El Vault es prioritario

La información permanente pertenece a Obsidian.

### El índice es reconstruible

Miyo debe poder regenerar su representación semántica a partir del Vault.

### La búsqueda debe probarse independientemente

Antes de culpar al modelo, comprobar Miyo directamente desde CLI.

### Los agentes no son la memoria

Copilot/OpenCode coordinan herramientas, pero no sustituyen al Vault.

### Evitar dependencia innecesaria

El diseño debe permitir reemplazar en el futuro Miyo o un modelo sin tener que reconstruir el conocimiento almacenado.

---

## 26. Estado

Miyo se encuentra operativo como capa de recuperación semántica del Knowledge Vault de SineOS.

La arquitectura validada es:

```text
Obsidian
   ↓
Miyo
   ↓
Copilot / OpenCode
   ↓
LLM
```

El Knowledge Vault fue limpiado de las notas utilizadas exclusivamente durante las pruebas y Miyo reflejó correctamente esas eliminaciones en su índice.

El CLI funciona mediante el enlace administrado por Miyo Desktop y utiliza el servicio local de Miyo para consultar el índice semántico.

La siguiente etapa de validación será la batería semántica multinota.
