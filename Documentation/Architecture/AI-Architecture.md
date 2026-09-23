# SineOS — Arquitectura de Inteligencia Artificial

## 1. Propósito

Este documento define la arquitectura de Inteligencia Artificial utilizada por SineOS.

El objetivo no es ejecutar el modelo más grande posible, sino construir un sistema de IA útil, sostenible y compatible con los recursos reales del equipo.

Principio fundamental:

> La mejor IA no es el modelo más pesado, sino la que soporta el equipo de cómputo.

SineOS utiliza una arquitectura híbrida que combina modelos locales, servicios gratuitos en la nube y servicios de pago únicamente cuando aportan una ventaja real.

---

## 2. Principio de operación

La estrategia general de SineOS es:

> Local first → free cloud when useful → paid DeepSeek only when it adds value.

Esto establece tres niveles de ejecución:

1. IA local.
2. IA cloud gratuita.
3. IA cloud de pago.

La selección depende de:

- privacidad;
- complejidad;
- contexto requerido;
- capacidad del hardware;
- costo;
- latencia;
- calidad esperada;
- necesidad de herramientas o razonamiento avanzado.

---

## 3. Arquitectura general

```text
                 ┌──────────────────────┐
                 │       Obsidian       │
                 │  Fuente de verdad    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │        Miyo          │
                 │ Índice semántico     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Copilot / OpenCode   │
                 │ Agente / herramientas│
                 └──────────┬───────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
         ┌─────────┐   ┌─────────┐   ┌──────────┐
         │ Ollama  │   │ Gemini  │   │ DeepSeek │
         │ Local   │   │ Cloud   │   │ Cloud    │
         └─────────┘   └─────────┘   └──────────┘
```

Cada componente tiene una responsabilidad específica.

---

## 4. Obsidian

Obsidian funciona como la fuente permanente de conocimiento de SineOS.

El Vault principal se encuentra en:

```text
${SINEOS_VAULT}
```

El Vault almacena:

- conocimiento técnico;
- documentación personal;
- procedimientos;
- incidencias;
- decisiones;
- proyectos;
- información universitaria;
- información profesional;
- referencias.

Obsidian no debe confundirse con el repositorio Git de SineOS.

### Separación de responsabilidades

```text
GitHub / SineOS
    código
    infraestructura
    scripts
    configuraciones
    documentación técnica

Obsidian / SineOS
    conocimiento
    procedimientos
    contexto
    decisiones
    segundo cerebro
```

El Vault no forma parte del repositorio Git.

---

## 5. Miyo

Miyo proporciona la capa de búsqueda semántica sobre el Vault.

Su función es permitir que los agentes encuentren información relevante aunque la consulta no utilice exactamente las mismas palabras que aparecen en las notas.

Flujo conceptual:

```text
Consulta
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
Vault de Obsidian
```

La búsqueda semántica local fue validada correctamente.

Miyo permite convertir el Vault en memoria consultable por los agentes sin convertir al modelo de lenguaje en la fuente de verdad.

---

## 6. Copilot / OpenCode

Copilot para Obsidian y OpenCode funcionan como capa de interacción entre:

- usuario;
- Vault;
- Miyo;
- herramientas;
- modelos de lenguaje.

La función del agente no es almacenar permanentemente el conocimiento.

Su responsabilidad es:

1. recibir la solicitud;
2. consultar información relevante;
3. utilizar herramientas cuando sea necesario;
4. seleccionar o utilizar el modelo correspondiente;
5. construir la respuesta.

El conocimiento permanente continúa almacenado en Obsidian.

---

## 7. IA local

La ejecución local utiliza Ollama.

Ventajas:

- privacidad;
- funcionamiento offline;
- costo de inferencia nulo;
- control local;
- independencia de proveedores externos.

Limitaciones:

- 16 GB de RAM;
- GPU integrada Intel Iris Xe;
- ausencia de GPU dedicada;
- rendimiento limitado con modelos grandes;
- menor capacidad de razonamiento que modelos cloud avanzados.

Por estas razones, SineOS no intenta ejecutar modelos excesivamente grandes.

---

## 8. Ollama

Ollama funciona como runtime de modelos locales.

Versión validada durante la construcción del sistema:

```text
Ollama 0.34.0
```

Se ejecuta mediante un servicio systemd de usuario.

Configuración utilizada:

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

Esto permite que otros componentes locales, incluidos contenedores rootless, puedan acceder al servicio.

### Deuda de seguridad

La exposición de Ollama en:

```text
*:11434
```

debe revisarse junto con la futura política de firewall/nftables.

No debe interpretarse como configuración de seguridad final.

---

## 9. Modelos locales

Los modelos seleccionados para SineOS son:

### Qwen 3.5 2B

```text
qwen3.5:2b
```

Uso previsto:

- consultas simples;
- procesamiento local;
- tareas privadas;
- funcionamiento offline;
- operaciones que no justifican una llamada cloud.

### Qwen 2.5 Coder 3B Instruct

```text
qwen2.5-coder:3b-instruct
```

Uso previsto:

- código sencillo;
- explicación de código;
- pequeñas transformaciones;
- tareas técnicas locales.

Los modelos de aproximadamente 2B–3B parámetros demostraron limitaciones cuando se utilizan con prompts agentic grandes y múltiples herramientas.

Por ello no constituyen el motor principal para tareas agentic complejas.

---

## 10. CPU y GPU

Durante las pruebas se evaluó la ejecución utilizando Vulkan sobre la GPU integrada Intel Iris Xe.

El rendimiento observado fue inferior al obtenido mediante CPU.

Por esta razón se eliminó el override de GPU y se mantuvo la ejecución local utilizando la configuración que proporciona mejor comportamiento en este hardware.

Esta decisión es específica del hardware actual y puede revisarse durante una futura migración.

---

## 11. llmfit

`llmfit` fue utilizado para evaluar qué modelos son razonables para el hardware disponible.

Versión utilizada:

```text
llmfit 1.1.15
```

Ubicación:

```text
~/.local/bin/llmfit
```

Existe una tarea pendiente para asegurar permanentemente:

```text
~/.local/bin
```

dentro del `PATH` de Zsh.

---

## 12. Gemini

Gemini 3.8 Flash funciona como el modelo cloud gratuito principal dentro de la arquitectura actual.

Uso previsto:

- tareas agentic;
- contextos grandes;
- análisis de documentos;
- tareas multimodales;
- consultas que superan razonablemente la capacidad de los modelos locales.

Gemini complementa la ejecución local en lugar de sustituirla completamente.

---

## 13. DeepSeek

DeepSeek constituye el backend cloud de pago para tareas donde una mayor capacidad aporta valor suficiente para justificar el costo.

Uso previsto:

- razonamiento más complejo;
- programación;
- tareas agentic;
- problemas técnicos que exceden la capacidad local;
- situaciones donde Gemini no proporciona el resultado requerido.

La integración fue validada mediante el flujo:

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

Este flujo confirmó que un modelo externo puede consultar el conocimiento almacenado localmente mediante la capa semántica de SineOS.

---

## 14. Groq

Groq fue evaluado como proveedor adicional.

Durante las pruebas con Copilot/OpenCode se produjo un ciclo relacionado con la compactación del contexto utilizando dos modelos distintos del proveedor.

Debido a este comportamiento y a que Gemini y DeepSeek cubren actualmente las necesidades del sistema, Groq fue descartado de la arquitectura operativa.

No debe agregarse nuevamente sin una razón técnica concreta y una nueva validación.

---

## 15. OpenRouter

OpenRouter Free fue considerado como posible proveedor adicional.

Actualmente no forma parte de la arquitectura.

La combinación:

```text
Ollama + Gemini + DeepSeek
```

cubre las necesidades actuales sin agregar otra capa de complejidad.

Principio:

> No agregar proveedores únicamente porque estén disponibles.

---

## 16. OpenAI API

La API de OpenAI no forma parte de la arquitectura actual.

El acceso a ChatGPT y el consumo de la API son servicios independientes desde el punto de vista de facturación y operación.

Por esta razón no se planifica utilizar OpenAI API únicamente por disponer de acceso a ChatGPT.

---

## 17. Codex

Codex está contemplado como herramienta futura especializada en programación.

Su función sería trabajar principalmente con:

- repositorio SineOS;
- código;
- scripts;
- infraestructura;
- mantenimiento técnico.

Debe permanecer separado conceptualmente del sistema de memoria.

Codex no sustituye:

- Obsidian;
- Miyo;
- el Vault.

---

## 18. NotebookLM

NotebookLM está contemplado como herramienta futura para investigación y docencia.

Uso previsto:

- PDFs;
- artículos;
- documentación;
- material académico;
- preparación de clases;
- análisis de fuentes.

NotebookLM no será la fuente permanente de verdad de SineOS.

La información que deba conservarse deberá integrarse posteriormente al Vault cuando corresponda.

---

## 19. Routing de IA

El routing debe seguir una estrategia pragmática.

### Nivel 1 — Local

Utilizar Ollama cuando:

- la información sea sensible;
- la tarea sea sencilla;
- se requiera funcionamiento offline;
- el modelo local tenga capacidad suficiente.

### Nivel 2 — Cloud gratuito

Utilizar Gemini cuando:

- se necesite mayor contexto;
- exista una tarea agentic;
- se analicen documentos;
- se requiera capacidad multimodal;
- la ejecución local sea insuficiente.

### Nivel 3 — Cloud de pago

Utilizar DeepSeek cuando:

- la tarea requiera razonamiento adicional;
- sea un problema complejo de programación;
- Gemini no resulte suficiente;
- la mejora esperada justifique el costo.

El routing no debe basarse únicamente en cuál modelo obtiene mejores benchmarks generales.

Debe considerar el problema concreto y los recursos disponibles.

---

## 20. Privacidad

La arquitectura busca mantener localmente la mayor cantidad razonable de información.

Principios:

- el Vault permanece local;
- Miyo realiza la indexación semántica;
- las credenciales no deben almacenarse en Git;
- las API keys no deben incluirse en documentación;
- una tarea sensible debe favorecer ejecución local cuando sea viable;
- los modelos cloud deben recibir únicamente el contexto necesario.

La integración de servicios externos no convierte automáticamente al proveedor externo en repositorio permanente del conocimiento de SineOS.

---

## 21. Estado de componentes

| Componente | Estado |
|---|---|
| Obsidian | Operativo |
| Knowledge Vault | Operativo |
| Miyo | Operativo |
| Miyo CLI | Operativo |
| Ollama | Operativo |
| Qwen 3.5 2B | Validado |
| Qwen 2.5 Coder 3B | Validado |
| Copilot para Obsidian | Operativo |
| Gemini 3.8 Flash | Validado |
| DeepSeek | Validado |
| Groq | Descartado |
| OpenRouter | No incorporado |
| OpenAI API | No incorporado |
| Codex | Futuro |
| NotebookLM | Futuro |

---

## 22. Principios de diseño

### Adecuación al hardware

El modelo debe adaptarse al equipo y no al contrario.

### Privacidad por diseño

Las tareas que puedan resolverse localmente deben favorecer procesamiento local cuando exista una razón de privacidad.

### Economía

Los servicios de pago deben utilizarse cuando aporten una ventaja concreta.

### Simplicidad

Agregar más proveedores no implica una arquitectura mejor.

### Separación de responsabilidades

```text
Obsidian = conocimiento
Miyo = recuperación semántica
Agente = orquestación
LLM = razonamiento/generación
Git = código e infraestructura
```

### Reproducibilidad

Las decisiones relevantes deben quedar documentadas para facilitar mantenimiento y futuras migraciones.

---

## 23. Próximas validaciones

La siguiente prueba significativa del sistema será una prueba semántica utilizando varias notas relacionadas.

El objetivo será validar:

1. recuperación sin coincidencia exacta de palabras;
2. síntesis entre dos o más notas;
3. recuperación de decisiones anteriores;
4. consulta de documentación técnica antes de ejecutar acciones;
5. comportamiento del routing según complejidad y privacidad.

---

## 24. Estado

Arquitectura de IA de SineOS definida.

La arquitectura operativa actual queda establecida como:

```text
Obsidian + Miyo
       ↓
Copilot / OpenCode
       ↓
Ollama / Gemini / DeepSeek
```

con el principio:

> Local first → free cloud when useful → paid DeepSeek only when it adds value.

Los componentes futuros o descartados no deben incorporarse al flujo operativo sin una nueva decisión técnica documentada.
