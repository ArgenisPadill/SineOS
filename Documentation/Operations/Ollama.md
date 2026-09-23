# SineOS — Ollama

## 1. Propósito

Este documento describe la implementación y operación de Ollama dentro de SineOS.

Ollama constituye el runtime principal para ejecutar modelos de lenguaje localmente.

Su función dentro de la arquitectura de IA es proporcionar:

- inferencia local;
- privacidad;
- funcionamiento offline;
- independencia parcial de proveedores cloud;
- ejecución de tareas sencillas sin costo por consulta.

Principio:

> La mejor IA no es el modelo más pesado, sino la que soporta el equipo de cómputo.

Ollama no pretende sustituir todos los modelos cloud.

Forma parte de una arquitectura híbrida:

```text
Local first
    ↓
Free cloud when useful
    ↓
Paid cloud when it adds value
```

---

## 2. Arquitectura

El flujo básico es:

```text
Aplicación / agente
       ↓
Ollama API
       ↓
Ollama
       ↓
Modelo local
       ↓
CPU / hardware
```

Dentro de SineOS puede participar en flujos como:

```text
Obsidian
   ↓
Miyo
   ↓
Copilot / OpenCode
   ↓
Ollama
   ↓
Qwen
```

Ollama ejecuta el modelo.

No constituye:

- memoria permanente;
- índice semántico;
- Knowledge Vault;
- repositorio de código.

---

## 3. Versión validada

Versión utilizada durante la construcción actual de SineOS:

```text
Ollama 0.34.0
```

Esta versión fue instalada utilizando el mecanismo oficial de Ollama.

La instalación se encuentra fuera de Podman.

Ollama se ejecuta directamente en el host Debian.

---

## 4. Sistema operativo

Entorno validado:

```text
Debian 13 Trixie
XFCE 4.20
Linux 6.12
x86_64
```

Hardware principal:

```text
Gateway GWTN141-10BK
Intel Core i5-1135G7
4 cores / 8 threads
16 GB LPDDR4
Intel Iris Xe
```

Estas características condicionan qué modelos son razonables para ejecución local.

---

## 5. Filosofía de selección de modelos

SineOS no selecciona modelos únicamente por tamaño o posición en benchmarks.

Los criterios incluyen:

- RAM disponible;
- CPU;
- GPU;
- velocidad;
- consumo;
- estabilidad;
- contexto;
- calidad;
- tipo de tarea.

El objetivo es obtener una relación útil entre:

```text
calidad
rendimiento
recursos
privacidad
costo
```

---

## 6. Servicio systemd

Ollama se ejecuta mediante un servicio systemd de usuario.

Esto permite integrar el runtime con la sesión del usuario y mantener su operación separada de los servicios privilegiados del sistema.

Conceptualmente:

```text
usuario
   ↓
systemd --user
   ↓
ollama
   ↓
API local
```

El servicio fue validado funcionalmente.

---

## 7. Configuración de red

Se configuró un override de systemd con:

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

Esto permite que Ollama escuche en:

```text
0.0.0.0:11434
```

La razón principal fue permitir comunicación desde otros componentes locales, incluidos contenedores rootless.

---

## 8. Puerto 11434

Ollama utiliza:

```text
11434/tcp
```

para su API.

Con la configuración actual:

```text
OLLAMA_HOST=0.0.0.0:11434
```

el servicio no queda limitado exclusivamente a:

```text
127.0.0.1
```

Por ello esta configuración tiene implicaciones de seguridad.

---

## 9. Estado de seguridad de red

nftables está operativo con INPUT `drop`. Ollama conserva `*:11434` porque Open WebUI con Podman rootless/`pasta` necesita alcanzar el host mediante `host.containers.internal`. La conectividad desde el contenedor fue validada. Falta una prueba desde otro dispositivo de la LAN y revisar la convivencia nftables/netavark.

---

## 10. Comunicación con contenedores

Uno de los consumidores de Ollama es Open WebUI.

Open WebUI se ejecuta mediante Podman rootless.

El contenedor utiliza:

```text
host.containers.internal
```

para alcanzar servicios del host.

La URL configurada para Open WebUI es:

```text
http://host.containers.internal:11434
```

Flujo:

```text
Open WebUI
   ↓
contenedor Podman
   ↓
host.containers.internal
   ↓
11434
   ↓
Ollama
```

Esta integración fue utilizada funcionalmente.

---

## 11. Modelos seleccionados

Los modelos locales seleccionados para el hardware actual son:

```text
qwen3.5:2b
qwen2.5-coder:3b-instruct
```

Cada modelo cumple una función diferente.

---

## 12. Qwen 3.5 2B

Modelo:

```text
qwen3.5:2b
```

Uso previsto:

- chat local;
- consultas sencillas;
- tareas privadas;
- operaciones offline;
- transformaciones simples;
- pruebas de integración.

Su tamaño permite una ejecución razonable dentro de las limitaciones del hardware disponible.

---

## 13. Qwen 2.5 Coder 3B Instruct

Modelo:

```text
qwen2.5-coder:3b-instruct
```

Uso previsto:

- código sencillo;
- explicación de fragmentos;
- pequeñas transformaciones;
- consultas técnicas locales;
- experimentación con programación offline.

No debe asumirse que un modelo pequeño especializado en código puede sustituir un modelo cloud avanzado para tareas complejas de ingeniería.

---

## 14. Limitaciones de modelos pequeños

Durante las pruebas se observó que modelos locales de aproximadamente:

```text
2B–3B parámetros
```

pueden responder correctamente a consultas sencillas.

Sin embargo, presentan limitaciones cuando se combinan con:

- prompts agentic extensos;
- muchas instrucciones;
- múltiples herramientas;
- grandes cantidades de contexto;
- llamadas repetidas;
- workflows complejos.

Por esta razón:

```text
modelo local
```

no equivale automáticamente a:

```text
agente local completo
```

---

## 15. Copilot / OpenCode

Ollama fue probado como backend para Copilot/OpenCode.

Las consultas simples pueden funcionar correctamente.

Sin embargo, el overhead producido por:

```text
prompt del agente
herramientas
contexto
instrucciones
```

puede superar la capacidad práctica de los modelos pequeños seleccionados.

Por ello SineOS utiliza modelos cloud cuando la tarea agentic lo requiere.

---

## 16. Arquitectura híbrida

La limitación de los modelos locales llevó a consolidar la arquitectura:

```text
                tarea
                  ↓
          evaluar complejidad
                  ↓
       ┌──────────┼──────────┐
       ↓          ↓          ↓
    Ollama     Gemini    DeepSeek
     local      cloud      cloud
```

Ollama se utiliza cuando el modelo local es suficiente.

Gemini y DeepSeek complementan, no invalidan, la capa local.

---

## 17. llmfit

Para evaluar modelos compatibles con el hardware se instaló:

```text
llmfit 1.1.15
```

Ubicación:

```text
~/.local/bin/llmfit
```

llmfit ayuda a evitar seleccionar modelos únicamente por popularidad.

La decisión debe considerar los recursos reales del equipo.

---

## 18. PATH pendiente

Existe una deuda de configuración relacionada con:

```text
~/.local/bin
```

La ubicación de `llmfit` todavía debe incorporarse permanentemente al `PATH` utilizado por Zsh si no se encuentra disponible automáticamente en futuras sesiones.

Estado:

```text
PENDIENTE
```

---

## 19. Prueba de GPU

El equipo utiliza:

```text
Intel Iris Xe
```

como GPU integrada.

Durante las pruebas se evaluó el uso de Vulkan para acelerar Ollama.

El resultado observado fue inferior al rendimiento obtenido utilizando CPU.

Por esta razón se eliminó el override utilizado para forzar la GPU.

---

## 20. Decisión CPU/GPU

Para el hardware actual:

```text
CPU > Vulkan sobre Iris Xe
```

en las pruebas realizadas con Ollama.

La configuración se mantuvo utilizando el comportamiento que proporcionó mejor rendimiento práctico.

Esta decisión no debe generalizarse a otros equipos.

Si SineOS migra a hardware con una GPU diferente, debe repetirse el benchmark.

---

## 21. Portabilidad de la decisión

La decisión sobre CPU/GPU pertenece al hardware actual:

```text
Gateway GWTN141-10BK
Intel Core i5-1135G7
Intel Iris Xe
16 GB RAM
```

Una futura computadora puede producir resultados completamente distintos.

Por ello:

```text
configuración actual
        ≠
regla permanente
```

La arquitectura debe permitir volver a evaluar el backend de inferencia.

---

## 22. Uso offline

Una de las principales ventajas de Ollama es permitir tareas sin conexión a servicios cloud.

Esto resulta útil para:

- privacidad;
- contingencias;
- experimentación;
- tareas sencillas;
- trabajo sin Internet.

Sin embargo, una tarea offline debe mantenerse dentro de la capacidad real del modelo local.

---

## 23. Privacidad

Ollama permite que el procesamiento del modelo ocurra localmente.

Esto es especialmente útil cuando:

- el contenido es privado;
- no es necesario utilizar un proveedor cloud;
- el modelo local puede resolver adecuadamente la tarea.

Principio:

> No enviar a la nube lo que puede resolverse localmente cuando existe una razón de privacidad.

Esto no significa que toda tarea deba ejecutarse localmente.

---

## 24. Relación con Miyo

Miyo y Ollama cumplen responsabilidades distintas.

```text
Miyo
   ↓
encuentra conocimiento

Ollama
   ↓
ejecuta el modelo
```

Una consulta puede combinar ambos:

```text
pregunta
   ↓
Miyo
   ↓
contexto relevante
   ↓
Ollama
   ↓
respuesta
```

El índice semántico y el modelo no deben confundirse.

---

## 25. Relación con Obsidian

Obsidian constituye la fuente permanente de conocimiento.

Ollama no debe utilizarse como sustituto del Vault.

Separación:

```text
Obsidian = memoria
Miyo     = recuperación
Ollama   = inferencia
```

Esta separación facilita sustituir un modelo sin perder conocimiento.

---

## 26. Relación con Open WebUI

Open WebUI proporciona una interfaz web para interactuar con Ollama.

Arquitectura:

```text
Navegador
   ↓
127.0.0.1:3000
   ↓
Open WebUI
   ↓
host.containers.internal:11434
   ↓
Ollama
   ↓
modelo
```

Open WebUI y Ollama son componentes independientes.

Un fallo de Open WebUI no implica necesariamente un fallo de Ollama.

---

## 27. Diagnóstico por capas

Cuando una aplicación no puede utilizar un modelo local, debe diagnosticarse por capas:

```text
modelo
   ↓
Ollama
   ↓
API 11434
   ↓
red
   ↓
aplicación cliente
```

Ejemplo:

Si Open WebUI no muestra modelos, primero debe comprobarse que Ollama funciona directamente antes de modificar el contenedor.

---

## 28. Comprobaciones operativas

Las comprobaciones habituales deben responder preguntas como:

```text
¿Está activo el servicio?
¿Está escuchando el puerto?
¿Ollama responde?
¿Está instalado el modelo?
¿El modelo puede ejecutar una consulta?
¿El cliente puede alcanzar Ollama?
```

Cada capa debe validarse independientemente.

---

## 29. Modelos instalados

La lista de modelos disponibles puede cambiar con el tiempo.

La documentación arquitectónica registra los modelos seleccionados, pero el estado real debe obtenerse desde Ollama.

Los modelos actualmente seleccionados son:

```text
qwen3.5:2b
qwen2.5-coder:3b-instruct
```

No debe asumirse que una lista documental sustituye la comprobación del runtime.

---

## 30. Descarga de modelos

Los modelos son artefactos locales de tamaño considerable.

No deben almacenarse dentro del repositorio Git.

Git debe conservar:

```text
documentación
configuración
scripts
decisiones
```

Los pesos de modelos deben ser recuperables nuevamente desde su proveedor correspondiente.

---

## 31. Backup

Los modelos descargados no tienen la misma prioridad de backup que el Knowledge Vault o los datos de PostgreSQL.

Prioridad conceptual:

```text
datos irreemplazables
        ↓
Vault / bases de datos

configuración reproducible
        ↓
Git

artefactos descargables
        ↓
modelos
```

Si un modelo puede descargarse nuevamente, no necesariamente debe formar parte de un backup crítico.

---

## 32. Migración de equipo

Durante una futura migración no debe ser obligatorio copiar todos los pesos de Ollama.

El proceso puede ser:

```text
instalar Debian
   ↓
instalar Ollama
   ↓
restaurar configuración
   ↓
descargar modelos seleccionados
   ↓
validar rendimiento
```

Después debe repetirse la evaluación de hardware.

---

## 33. Actualización de Ollama

Una actualización de Ollama debe validar:

```text
[ ] Servicio inicia
[ ] API responde
[ ] Modelos existentes son reconocidos
[ ] Inferencia funciona
[ ] Open WebUI puede conectarse
[ ] Copilot/OpenCode puede conectarse
[ ] Rendimiento no presenta regresión significativa
```

Las actualizaciones no deben asumirse correctas únicamente porque el paquete se instaló.

---

## 34. Actualización de modelos

Actualizar o sustituir un modelo debe tratarse como una decisión independiente de actualizar Ollama.

Debe evaluarse:

- memoria;
- velocidad;
- calidad;
- contexto;
- estabilidad;
- comportamiento con herramientas.

Un modelo más nuevo no es automáticamente mejor para el hardware actual.

---

## 35. Benchmark

Los benchmarks útiles para SineOS deben medir comportamiento real.

Ejemplos:

```text
tiempo de carga
tokens por segundo
RAM utilizada
calidad de respuesta
seguimiento de instrucciones
capacidad con herramientas
latencia total
```

El objetivo no es obtener el número más alto posible, sino identificar qué configuración resulta práctica.

---

## 36. Troubleshooting

### Ollama no responde

Comprobar:

```text
servicio systemd user
proceso
puerto 11434
logs
```

### El modelo no aparece

Comprobar la lista real de modelos instalados.

### El modelo es demasiado lento

Comprobar:

```text
CPU
RAM
swap
tamaño del modelo
contexto
procesos concurrentes
```

### Vulkan es más lento

La configuración actual ya observó este comportamiento con Intel Iris Xe.

No volver a forzar GPU sin realizar un benchmark que justifique el cambio.

### Open WebUI no alcanza Ollama

Separar el diagnóstico:

```text
Ollama
   ↓
11434
   ↓
host.containers.internal
   ↓
contenedor
```

No modificar Ollama hasta comprobar qué capa está fallando.

---

## 37. Seguridad

Pendientes relevantes:

```text
[ ] Definir política nftables
[ ] Revisar exposición de 11434
[ ] Limitar clientes autorizados
[ ] Revisar configuración después de cambios de red
```

La configuración actual fue diseñada primero para conseguir conectividad funcional entre componentes.

El hardening de red sigue pendiente.

---

## 38. Estado actual

| Componente | Estado |
|---|---|
| Ollama 0.34.0 | Operativo |
| systemd user service | Operativo |
| API 11434 | Operativa |
| `OLLAMA_HOST=0.0.0.0:11434` | Configurado |
| qwen3.5:2b | Validado |
| qwen2.5-coder:3b-instruct | Validado |
| CPU | Validada |
| Vulkan / Iris Xe | Probado y descartado |
| Open WebUI → Ollama | Validado |
| Modelos locales con tareas simples | Validados |
| Agentic complejo con 2B–3B | Limitado |
| nftables | Operativo |
| Hardening de 11434 | Parcial: prueba externa pendiente |
| PATH permanente para llmfit | Pendiente |

---

## 39. Deuda técnica

Pendientes relacionados con Ollama:

```text
[x] Implementar política nftables
[ ] Revisar exposición de Ollama en 11434
[ ] Formalizar acceso desde contenedores
[ ] Hacer permanente ~/.local/bin en Zsh
[ ] Mantener benchmark de modelos
[ ] Evaluar nuevos modelos solo cuando aporten valor
[ ] Repetir benchmark CPU/GPU después de una migración de hardware
```

---

## 40. Principios operativos

### Local cuando tenga sentido

No utilizar cloud si la tarea puede resolverse adecuadamente de forma local y existe una ventaja concreta.

### Cloud cuando aporte capacidad

No forzar un modelo pequeño a resolver una tarea para la que claramente no tiene capacidad.

### Hardware primero

La selección del modelo debe respetar los recursos reales.

### Medir antes de optimizar

CPU/GPU debe decidirse mediante pruebas y no mediante suposiciones.

### Separar memoria de inferencia

Ollama ejecuta modelos; no constituye la memoria permanente de SineOS.

### Mantener reemplazabilidad

La arquitectura debe permitir sustituir Ollama o un modelo sin reconstruir el Knowledge Vault.

---

## 41. Estado

Ollama se encuentra operativo como runtime local de Inteligencia Artificial de SineOS.

La implementación actual puede representarse como:

```text
Debian 13
   ↓
systemd user
   ↓
Ollama 0.34.0
   ↓
11434
   ↓
Qwen
```

Los modelos locales seleccionados son:

```text
qwen3.5:2b
qwen2.5-coder:3b-instruct
```

La ejecución mediante CPU ofrece actualmente un mejor resultado práctico que el backend Vulkan probado sobre Intel Iris Xe.

La deuda restante es validar externamente el bloqueo de 11434 y revisar nftables con el networking rootless de Podman.
