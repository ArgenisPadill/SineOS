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
/home/argenis/Obsidian/SineOS
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
/home/argenis/Obsidian/SineOS
```

Miyo debe indexar el Knowledge Vault y no el repositorio Git de SineOS.

Separación:

```text
/home/argenis/Workspace/SineOS
        ↓
Git / código / infraestructura / documentación técnica

/home/argenis/Obsidian/SineOS
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

Durante la instalación se detectó un problema con el CLI proporcionado mediante la AppImage.

El enlace esperado para ejecutar el CLI no funcionaba correctamente.

La solución utilizada consistió en extraer el CLI real de la AppImage y mantener una copia funcional en:

```text
~/.miyo/bin/miyo
```

La ejecución directa desde esta ubicación fue validada correctamente.

---

## 9. Incidente del CLI

### Síntoma

El CLI asociado a la instalación AppImage no podía utilizarse correctamente mediante el enlace esperado.

Esto impedía que herramientas externas utilizaran Miyo de manera confiable.

### Diagnóstico

La aplicación gráfica funcionaba, pero el mecanismo utilizado para exponer el CLI desde la AppImage producía un enlace no funcional.

El problema no correspondía al índice semántico ni al Knowledge Vault.

Se encontraba en la forma de acceso al ejecutable CLI.

### Solución

Se extrajo el CLI real contenido en la AppImage.

Posteriormente se copió el ejecutable funcional a:

```text
~/.miyo/bin/miyo
```

La ejecución directa del binario permitió realizar búsquedas semánticas correctamente.

### Resultado

```text
Miyo AppImage
      ↓
CLI extraído
      ↓
~/.miyo/bin/miyo
      ↓
búsqueda semántica
      ↓
Knowledge Vault
```

Estado:

```text
RESUELTO
```

---

## 10. Deuda técnica del CLI

La solución actual tiene una consecuencia importante.

El archivo:

```text
~/.miyo/bin/miyo
```

es una copia extraída del CLI.

Por lo tanto, actualizar:

```text
~/.local/opt/miyo/Miyo.AppImage
```

no garantiza que la copia del CLI se actualice automáticamente.

Después de una actualización de Miyo debe comprobarse la compatibilidad entre:

```text
Miyo.AppImage
```

y:

```text
~/.miyo/bin/miyo
```

Puede ser necesario volver a extraer el CLI.

Esta tarea todavía no está automatizada.

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

## 18. Prueba temporal de Miyo

Durante las pruebas iniciales se utilizó una nota temporal:

```text
Prueba Miyo.md.md
```

Su propósito es validar recuperación semántica.

Esta nota no forma parte de la estructura permanente del Knowledge Vault.

Debe conservarse únicamente hasta completar la batería semántica prevista.

Después deberá eliminarse y comprobarse que el watcher o mecanismo de indexación refleje correctamente la eliminación.

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

Comprobar primero:

```text
~/.miyo/bin/miyo
```

La instalación actual utiliza el CLI extraído de la AppImage.

### Una búsqueda no encuentra una nota reciente

Comprobar:

1. que la nota esté dentro del scope;
2. que Miyo esté ejecutándose;
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

Recordar que:

```text
~/.miyo/bin/miyo
```

es una copia extraída.

Comprobar si debe extraerse nuevamente el CLI correspondiente a la nueva AppImage.

---

## 23. Estado actual

Estado de la implementación:

| Componente | Estado |
|---|---|
| Miyo AppImage | Operativo |
| Knowledge Vault | Operativo |
| Scope del Vault | Configurado |
| Indexación semántica | Validada |
| Miyo CLI | Operativo |
| Workaround CLI | Aplicado |
| Copilot/OpenCode | Integrado |
| DeepSeek + Miyo | Validado |
| Gemini + Vault | Validado |
| Actualización automática del CLI | Pendiente |
| Batería semántica multinota | Pendiente |
| Eliminación de nota temporal | Pendiente |

---

## 24. Deuda técnica

Pendientes relacionados directamente con Miyo:

```text
[ ] Definir mecanismo de actualización de Miyo
[ ] Sincronizar automáticamente AppImage y CLI
[ ] Documentar procedimiento reproducible de reinstalación
[ ] Definir autostart si resulta necesario
[ ] Ejecutar benchmark semántico multinota
[ ] Eliminar Prueba Miyo.md.md después del benchmark
[ ] Verificar eliminación del documento en el índice
[ ] Incorporar pruebas de recuperación al mantenimiento de SineOS
```

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

El incidente inicial del CLI fue resuelto mediante la extracción del ejecutable real y su instalación en:

```text
~/.miyo/bin/miyo
```

La principal deuda técnica actual es mantener sincronizado ese CLI con futuras actualizaciones de la AppImage.

La siguiente etapa de validación será la batería semántica multinota.
