# SineOS Knowledge Vault

## Propósito

El Knowledge Vault de SineOS constituye la base de conocimiento permanente del entorno.

El Vault utiliza Obsidian y se mantiene deliberadamente separado del repositorio Git operativo de SineOS.

- Repositorio SineOS: `/home/argenis/Workspace/SineOS`
- Knowledge Vault: `/home/argenis/Obsidian/SineOS`

El repositorio almacena código, configuración, scripts e infraestructura.

El Vault almacena conocimiento, procedimientos, decisiones, documentación personal, académica y profesional.

## Arquitectura principal

```text
SineOS/
├── 00-Inbox/
├── 01-Sistema/
├── 02-Infraestructura/
├── 03-IA/
├── 04-Proyectos/
├── 05-Procedimientos/
├── 06-Incidencias/
├── 07-Conocimiento/
├── 08-Decisiones/
├── 09-Referencias/
├── 10-Universidad/
├── 11-Trabajo/
└── 99-Archivo/
```

Los directorios técnicos utilizados por Obsidian y sus herramientas permanecen independientes de esta clasificación semántica.

## Universidad de Xalapa

La estructura académica sigue la jerarquía:

```text
UX
└── Nivel
    └── Año
        └── Semestre
            └── Modalidad
                └── Bloque (cuando aplica)
                    └── Materia
```

Los árboles académicos no se crean anticipadamente. `Materia.md` genera dinámicamente la estructura requerida al crear una materia.

### Modalidades de Licenciatura

- Escolarizado: una materia por semestre, sin bloque.
- Vespertino: dos bloques por semestre.
- Sabatino: cuatro bloques por semestre.

Los semestres utilizan `Semestre-1` y `Semestre-2`.

## Sistema de IA

La arquitectura sigue el principio:

> Local first → free cloud when useful → paid DeepSeek only when it adds value.

Componentes principales:

- Obsidian: fuente permanente de verdad.
- Miyo: índice y búsqueda semántica del Vault.
- Ollama/Qwen: procesamiento local, privado y offline.
- Gemini 3.8 Flash: modelo cloud principal para trabajo agentic, documentos y contexto amplio.
- DeepSeek: backend de razonamiento y código cuando aporta valor adicional.
- Codex: futuro agente especializado de programación para el repositorio SineOS.
- NotebookLM: futura herramienta independiente para investigación y material académico.

Groq fue probado y descartado por problemas de integración relacionados con la compactación de contexto.

## Convenciones

Las fechas visibles del Vault utilizan `DD-MM-AAAA`.

Las notas nuevas utilizan `creado`. No se mantiene automáticamente un campo `actualizado`.

Una nota representa su versión vigente para evitar que el índice semántico recupere copias obsoletas.

## Identificadores estables

```text
MAT-YYYYMMDD-XXXX
UNI-YYYYMMDD-XXXX
TAR-YYYYMMDD-XXXX
ACT-YYYYMMDD-XXXX
EXA-YYYYMMDD-XXXX
PRO-YYYYMMDD-XXXX
ETA-YYYYMMDD-XXXX
```

El sufijo utiliza:

`ABCDEFGHJKLMNPQRSTUVWXYZ23456789`

Se excluyen `I`, `O`, `0` y `1` para reducir ambigüedad visual.

## Separación de responsabilidades

El repositorio Git contiene código, configuraciones, scripts, infraestructura, automatización y documentación técnica del proyecto.

El Knowledge Vault contiene conocimiento, procedimientos, decisiones, incidencias, documentación académica y profesional, referencias y notas de trabajo.

**El Vault no forma parte del repositorio Git de SineOS.**

## Estado

Arquitectura del Knowledge Vault definida.

Sistema académico basado en Templater validado funcionalmente el **19-09-2026**.
