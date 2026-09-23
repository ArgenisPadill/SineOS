# SineOS — Open WebUI

## 1. Propósito

Este documento describe la implementación y operación de Open WebUI dentro de SineOS.

Open WebUI proporciona una interfaz web local para interactuar con modelos servidos por Ollama.

Su función es ofrecer una capa de interfaz independiente del runtime de modelos.

Separación de responsabilidades:

```text
Open WebUI = interfaz
Ollama     = runtime de modelos
Qwen       = modelos locales
```

Open WebUI no constituye:

- el Knowledge Vault;
- la memoria permanente;
- el índice semántico;
- el runtime de inferencia;
- la fuente de verdad de SineOS.

---

## 2. Arquitectura

El flujo principal es:

```text
Navegador
   ↓
127.0.0.1:3000
   ↓
Open WebUI
   ↓
Podman rootless
   ↓
host.containers.internal:11434
   ↓
Ollama
   ↓
Modelo local
```

Open WebUI se ejecuta dentro de un contenedor.

Ollama se ejecuta directamente en el host.

---

## 3. Ubicación del stack

La definición versionada se encuentra en:

```text
Containers/stacks/open-webui/compose.yaml
```

Dentro del repositorio:

```text
${SINEOS_REPO}
```

El archivo `compose.yaml` forma parte de Git.

Los datos persistentes generados por Open WebUI no deben tratarse como código fuente.

---

## 4. Runtime

Open WebUI utiliza:

```text
Podman rootless
```

sobre Debian 13.

La ejecución rootless permite operar el servicio sin ejecutar el contenedor como una carga administrativa privilegiada del host.

El entorno de contenedores de SineOS utiliza:

```text
Podman 5.4.2
cgroup v2
netavark
pasta
```

---

## 5. Definición actual

La configuración actual del servicio utiliza:

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: sineos-open-webui

    restart: unless-stopped

    network_mode: pasta

    ports:
      - "127.0.0.1:3000:8080"

    environment:
      OLLAMA_BASE_URL: http://host.containers.internal:11434

    volumes:
      - ../../volumes/open-webui/data:/app/backend/data
```

Esta configuración representa el estado funcional actual.

No debe interpretarse como hardening final.

---

## 6. Imagen

Actualmente se utiliza:

```text
ghcr.io/open-webui/open-webui:main
```

La etiqueta:

```text
main
```

es móvil.

Esto significa que una descarga futura puede obtener una versión diferente aun cuando el archivo `compose.yaml` no haya cambiado.

---

## 7. Deuda de reproducibilidad

Utilizar:

```text
:main
```

reduce la reproducibilidad de la infraestructura.

Una futura mejora debe sustituir esta referencia por:

- una versión explícita; o
- un digest validado.

Objetivo:

```text
misma configuración
        +
misma imagen
        =
comportamiento reproducible
```

Estado:

```text
PENDIENTE
```

---

## 8. Nombre del contenedor

El contenedor utiliza:

```text
sineos-open-webui
```

Este nombre facilita identificarlo dentro del conjunto de servicios de SineOS.

La nomenclatura ayuda a evitar confundirlo con contenedores ajenos al proyecto.

---

## 9. Política de arranque

La política operativa es iniciar y detener Open WebUI manualmente desde Podman Desktop. El Compose todavía contiene `restart: unless-stopped`, por lo que existe una divergencia que debe corregirse mediante recreación controlada preservando el volumen. No se planea Quadlet mientras siga vigente el arranque manual.

---

## 10. Network mode

La configuración utiliza:

```yaml
network_mode: pasta
```

`pasta` forma parte de la estrategia de networking rootless utilizada por Podman.

Esta configuración permite operar el contenedor sin depender de una red privilegiada del host.

---

## 11. Exposición web

El puerto se publica mediante:

```yaml
ports:
  - "127.0.0.1:3000:8080"
```

Esto significa:

```text
host 127.0.0.1:3000
        ↓
contenedor :8080
```

La interfaz web queda vinculada explícitamente a loopback.

---

## 12. Acceso desde navegador

La interfaz se utiliza mediante:

```text
http://127.0.0.1:3000
```

Al estar vinculada a `127.0.0.1`, la intención actual es que Open WebUI sea una interfaz local.

No debe cambiarse a:

```text
0.0.0.0:3000
```

sin evaluar previamente las implicaciones de seguridad.

---

## 13. Open WebUI y Ollama

Open WebUI necesita acceder a Ollama para consultar los modelos locales.

La variable utilizada es:

```yaml
OLLAMA_BASE_URL: http://host.containers.internal:11434
```

El contenedor no utiliza:

```text
localhost:11434
```

porque dentro del contenedor `localhost` se refiere al propio contenedor.

---

## 14. host.containers.internal

Podman proporciona:

```text
host.containers.internal
```

como mecanismo para alcanzar el host desde determinados entornos de contenedores.

En SineOS se utiliza para:

```text
Open WebUI
      ↓
host.containers.internal
      ↓
Ollama
```

Esto permite mantener Ollama fuera del contenedor de Open WebUI.

---

## 15. Dependencia con Ollama

Para que Open WebUI muestre y utilice modelos locales deben funcionar varias capas:

```text
Ollama
   ↓
API 11434
   ↓
conectividad host/contenedor
   ↓
Open WebUI
```

Un fallo en Open WebUI no significa automáticamente que Ollama esté fallando.

Del mismo modo, un contenedor Open WebUI activo no garantiza que Ollama sea accesible.

---

## 16. Persistencia

Open WebUI utiliza:

```yaml
volumes:
  - ../../volumes/open-webui/data:/app/backend/data
```

La información persistente de la aplicación se almacena fuera de la capa efímera del contenedor.

Conceptualmente:

```text
Open WebUI container
        ↓
/app/backend/data
        ↓
Containers/volumes/open-webui/data
```

Esto permite recrear el contenedor sin depender de su filesystem interno.

---

## 17. Separación entre infraestructura y datos

Git debe conservar:

```text
compose.yaml
documentación
configuración reproducible
```

Los datos runtime deben mantenerse fuera del historial Git cuando corresponda.

Principio:

> Git conserva cómo reconstruir el servicio, no todo el estado generado por el servicio.

---

## 18. Validación del compose

La definición actual fue validada mediante el proveedor Compose utilizado por Podman.

La validación confirmó que:

```text
compose.yaml
```

es sintácticamente aceptado.

Esto no significa que el contenedor se encuentre necesariamente ejecutándose en todo momento.

---

## 19. Estado del contenedor

Durante la revisión documental previa al commit de Open WebUI se comprobó:

```text
podman ps --filter name=sineos-open-webui
```

y no había un contenedor activo en ese momento.

Por tanto deben distinguirse dos afirmaciones:

```text
configuración validada
```

y:

```text
servicio actualmente ejecutándose
```

No son equivalentes.

---

## 20. Validación funcional histórica

Open WebUI fue utilizado previamente de forma funcional con Ollama.

La integración:

```text
Open WebUI
   ↓
Ollama
```

fue comprobada durante la construcción del stack de IA.

Sin embargo, después de cambios relevantes debe repetirse la validación operativa.

---

## 21. Secret key

Open WebUI puede requerir secretos persistentes para determinados aspectos de su operación.

La configuración actual todavía no establece una estrategia definitiva para un secret persistente administrado por SineOS.

Estado:

```text
PENDIENTE
```

No debe introducirse un secreto real directamente en:

```text
compose.yaml
```

si ese archivo será versionado.

---

## 22. Gestión de secretos

La futura solución debe respetar el principio:

```text
configuración
    ↓
Git

secretos
    ↓
fuera de Git
```

La estrategia puede evolucionar conforme se formalice la política general de secretos de SineOS.

No debe documentarse una credencial real.

---

## 23. Seguridad de la interfaz

Open WebUI está publicado actualmente en:

```text
127.0.0.1:3000
```

Esto reduce la exposición directa de la interfaz respecto de una publicación en todas las interfaces.

Aun así, deben mantenerse buenas prácticas para:

- cuentas;
- sesiones;
- secretos;
- actualizaciones;
- datos persistentes;
- imágenes de contenedor.

---

## 24. Diferencia de exposición con Ollama

Existe una diferencia importante:

```text
Open WebUI
127.0.0.1:3000
```

frente a la configuración actual de Ollama:

```text
0.0.0.0:11434
```

Por tanto, aunque Open WebUI esté limitado a loopback, eso no resuelve por sí mismo la exposición de Ollama.

La seguridad debe evaluarse por componente.

---

## 25. nftables

nftables está operativo con INPUT `drop`. Open WebUI está limitado a `127.0.0.1:3000`. Open WebUI alcanza Ollama por `host.containers.internal:11434` con `pasta`; queda pendiente validar el bloqueo de Ollama desde otro dispositivo y revisar nftables con Podman/netavark.

---

## 26. Actualización de Open WebUI

Antes de actualizar Open WebUI debe comprobarse:

```text
versión actual
release objetivo
cambios incompatibles
persistencia
configuración
integración con Ollama
```

Mientras se utilice:

```text
:main
```

la imagen puede cambiar sin que el archivo Compose indique explícitamente qué versión se ejecutará.

Esta deuda debe corregirse.

---

## 27. Estrategia futura de imagen

La estrategia deseada es utilizar una referencia reproducible.

Ejemplo conceptual:

```text
ghcr.io/open-webui/open-webui:<version>
```

o:

```text
imagen@sha256:<digest>
```

La versión concreta debe seleccionarse y validarse cuando se realice el hardening.

No debe inventarse un número de versión únicamente para completar la documentación.

---

## 28. Backup

Debe evaluarse qué información dentro de:

```text
Containers/volumes/open-webui/data
```

requiere backup.

La prioridad de backup debe basarse en la importancia real de los datos.

Open WebUI no debe tener mayor prioridad que fuentes primarias como:

```text
Knowledge Vault
PostgreSQL
```

si su estado puede reconstruirse.

---

## 29. Migración

Durante una futura migración de equipo, Open WebUI debe poder reconstruirse a partir de:

```text
repositorio SineOS
        ↓
compose.yaml
        ↓
imagen validada
        ↓
datos persistentes necesarios
```

Esto forma parte del objetivo general de portabilidad de SineOS.

---

## 30. Diagnóstico por capas

Si la interfaz no funciona, utilizar:

```text
Navegador
   ↓
127.0.0.1:3000
   ↓
Podman
   ↓
contenedor Open WebUI
   ↓
logs
   ↓
host.containers.internal
   ↓
Ollama :11434
   ↓
modelo
```

No modificar todas las capas simultáneamente.

---

## 31. Troubleshooting

### No abre `127.0.0.1:3000`

Comprobar:

```text
contenedor activo
puerto publicado
logs
compose
```

### Open WebUI abre pero no muestra modelos

Comprobar primero Ollama directamente.

Después comprobar:

```text
OLLAMA_BASE_URL
host.containers.internal
11434
conectividad desde el contenedor
```

### El contenedor inicia pero pierde configuración

Comprobar el mount:

```text
../../volumes/open-webui/data:/app/backend/data
```

### Una actualización cambia el comportamiento

Recordar que actualmente se utiliza:

```text
:main
```

Comprobar qué imagen se descargó realmente.

---

## 32. Comprobaciones después de cambios

Después de modificar el stack comprobar:

```text
[ ] compose.yaml es válido
[ ] El contenedor puede crearse
[ ] El contenedor inicia
[ ] 127.0.0.1:3000 responde
[ ] El volumen persistente está montado
[ ] Ollama responde
[ ] Open WebUI puede alcanzar Ollama
[ ] Los modelos aparecen
[ ] Una consulta puede ejecutarse
[ ] Los logs no muestran errores críticos
[ ] No existen secretos reales en Git
```

---

## 33. Relación con Miyo

Open WebUI no constituye actualmente la capa principal de recuperación semántica de SineOS.

Miyo mantiene esa responsabilidad.

Separación:

```text
Open WebUI
    interfaz de chat

Miyo
    recuperación semántica

Obsidian
    conocimiento

Ollama
    inferencia local
```

Estas funciones no deben mezclarse conceptualmente.

---

## 34. Relación con la arquitectura de IA

Dentro de la arquitectura completa:

```text
                 Obsidian
                    ↓
                   Miyo
                    ↓
             agente / herramientas
                    ↓
        Ollama / Gemini / DeepSeek
```

Open WebUI proporciona una interfaz adicional para interactuar especialmente con la capa local.

No actúa como router central de toda la arquitectura.

---

## 35. Deuda técnica

Pendientes conocidos:

```text
[ ] Sustituir `:main` por versión o digest fijo
[ ] Validar la imagen seleccionada
[ ] Definir secret persistente
[ ] Mantener secretos fuera de Git
[ ] Evaluar backup de datos de Open WebUI
[x] nftables operativo; revisión Podman/netavark pendiente
[x] Quadlet descartado mientras el arranque sea manual
[ ] Documentar actualización controlada
```

---

## 36. Estado actual

| Elemento | Estado |
|---|---|
| Compose | Validado |
| Podman rootless | Operativo |
| `network_mode: pasta` | Configurado |
| Bind `127.0.0.1:3000` | Configurado |
| Persistencia | Configurada |
| Integración con Ollama | Validada previamente |
| Contenedor activo permanentemente | No asumido |
| Imagen fija | Pendiente |
| Secret persistente | Pendiente |
| Hardening final | Pendiente |

---

## 37. Principios operativos

### Interfaz y runtime son distintos

Open WebUI no debe confundirse con Ollama.

### Loopback por defecto

La interfaz no debe exponerse externamente sin una razón y una revisión de seguridad.

### Datos fuera del contenedor

El estado que deba persistir debe almacenarse fuera de la capa efímera.

### Imágenes reproducibles

Las etiquetas móviles deben sustituirse por referencias controladas cuando el servicio se estabilice.

### Secretos fuera de Git

Ninguna credencial real debe formar parte del Compose versionado.

### Diagnóstico por capas

Antes de modificar el contenedor debe determinarse si el fallo pertenece a Open WebUI, networking, Ollama o al modelo.

---

## 38. Estado

Open WebUI dispone de una configuración funcional y versionada dentro de SineOS.

La arquitectura actual es:

```text
Navegador
   ↓
127.0.0.1:3000
   ↓
Open WebUI
   ↓
Podman rootless / pasta
   ↓
host.containers.internal:11434
   ↓
Ollama
```

La configuración actual prioriza acceso local y persistencia.

Las principales tareas pendientes son:

```text
fijar imagen
definir secret persistente
hardening
revisar estrategia de servicio
```

Hasta completar esas tareas, la configuración debe considerarse funcional pero no final.
