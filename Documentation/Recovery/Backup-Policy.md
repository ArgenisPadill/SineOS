# SineOS — Política general de backups

**Estado:** Adoptada  
**Fecha:** 23-09-2026

## Propósito

Definir qué información de SineOS debe respaldarse, con qué prioridad, frecuencia, retención, verificación y criterios de recuperación.

Esta política es la base para los procedimientos específicos de PostgreSQL, Knowledge Vault, secretos, aplicaciones y Disaster Recovery.

También define el **ciclo trimestral certificado de mantenimiento de SineOS**, compuesto por:

```text
auditoría profunda de salud
        +
respaldo externo validado
        +
registro versionado
        +
sincronización confirmada con GitHub
```

## Principios

### 1. Un snapshot no es un backup

Los snapshots Btrfs/Snapper viven en el mismo almacenamiento que los datos originales.

Se utilizan para:

- rollback rápido;
- recuperación ante cambios locales;
- congelar un estado coherente antes de generar un backup.

No sustituyen una copia almacenada en otro medio.

### 2. Un backup debe poder restaurarse

La existencia de archivos no demuestra que exista recuperación.

Todo componente crítico debe disponer de:

- creación de backup;
- comprobación de integridad;
- procedimiento de restore;
- prueba periódica de restauración.

### 3. Copias separadas del equipo principal

Estado objetivo:

```text
datos de trabajo
      +
backup cifrado en medio físico separado
      +
copia cifrada off-site cuando sea viable
```

Una copia ubicada únicamente en el mismo SSD de la laptop es una copia temporal, no un backup suficiente frente a fallo físico, robo o pérdida total del equipo.

### 4. Cifrado por defecto

Los backups que contengan datos privados o secretos deben almacenarse cifrados.

Las credenciales de acceso al repositorio de backup:

- permanecen fuera de Git;
- no se imprimen en reportes;
- deben tener recuperación independiente;
- deben tratarse según la política de secretos.

## GitHub como respaldo de configuración

GitHub cumple dos funciones simultáneas dentro de SineOS:

1. repositorio vivo donde la configuración, scripts, aplicaciones y documentación evolucionan;
2. copia remota de la **configuración reproducible** del sistema.

GitHub no sustituye los backups de datos privados o runtime. No debe almacenar bases de datos, volúmenes de contenedores, secretos, el Knowledge Vault privado ni dumps sensibles.

La reconstrucción conceptual queda:

```text
GitHub
   ↓
configuración + código + documentación
   +
Disco externo
   ↓
datos + estado + artefactos de recuperación
```

Por ello una recuperación completa necesita ambas fuentes.

## Ciclo trimestral certificado

Cada tres meses SineOS debe ejecutar un ciclo completo de mantenimiento:

```text
1. auditoría profunda de salud
2. resolución o revisión de hallazgos críticos
3. respaldo externo
4. comprobación de integridad
5. restauración de prueba
6. registro en Git
7. sincronización con GitHub
8. validación del commit remoto
```

La aplicación nativa de mantenimiento conserva el estado pendiente mientras este flujo no se complete.

La notificación visual puede ser cerrada por el escritorio, pero eso **no marca el ciclo como completado**. El estado persistente seguirá pendiente y el servicio volverá a recordarlo hasta validar la sincronización Git.

## Motor de backup

SineOS adopta **Restic** como motor preferente para backups de archivos y artefactos exportados.

Motivos:

- cifrado integrado;
- deduplicación;
- snapshots/versiones;
- verificación de repositorio;
- restauración selectiva;
- soporte para repositorios locales y remotos;
- paquete disponible en Debian 13.

No se inicializa un repositorio hasta seleccionar y validar el destino físico.

Btrfs/Snapper permanece como mecanismo complementario de rollback local.

## Clasificación de datos

### Nivel A — Crítico / difícil de reconstruir

| Componente | Tratamiento |
|---|---|
| Knowledge Vault | backup independiente obligatorio |
| PostgreSQL | backup lógico + restore probado |
| secretos necesarios para recuperación | backup cifrado y controlado |
| configuración local no reproducible | incluir cuando sea necesaria para reconstrucción |

Objetivo deseable si posteriormente se implementan copias intermedias:

```text
RPO aspiracional: 24 horas
RPO garantizado por el esquema certificado actual: hasta 3 meses
```

El valor de 24 horas no se considera una garantía vigente mientras no exista una frecuencia intermedia automatizada y validada.

### Nivel B — Importante / reconstruible con pérdida de estado

| Componente | Tratamiento |
|---|---|
| Open WebUI data | backup periódico |
| Uptime Kuma data | backup periódico |
| Stirling PDF configuración/datos relevantes | backup según necesidad |
| configuración XFCE no totalmente versionada | backup mientras no sea 100 % reproducible |

Objetivo deseable si posteriormente se implementan copias intermedias:

```text
RPO aspiracional: 7 días
RPO garantizado por el esquema certificado actual: hasta 3 meses
```

El valor de 7 días no se considera una garantía vigente mientras no exista una frecuencia intermedia automatizada y validada.

### Nivel C — Reproducible o descargable

Normalmente no requiere backup de datos pesados:

- imágenes de contenedor;
- cachés;
- paquetes APT;
- modelos Ollama descargables;
- temporales;
- logs no requeridos para auditoría;
- artefactos reconstruibles desde Git.

El repositorio Git de SineOS ya conserva la definición reproducible de infraestructura.

## Frecuencia

### Respaldo externo certificado

La regla operativa principal de SineOS es:

```text
cada 3 meses
```

Cada corte trimestral debe incluir los componentes definidos por la política y la auditoría profunda del sistema.

Esto implica que, si no existen copias intermedias, el RPO real del respaldo externo puede llegar a tres meses. La aplicación debe mostrar esta realidad y no presentar el esquema como protección diaria.

### Copias extraordinarias

También se realiza un respaldo antes de:

- migraciones;
- cambios destructivos;
- operaciones de recuperación;
- actualizaciones de alto riesgo;
- cambios relevantes de almacenamiento.

Pueden existir copias intermedias más frecuentes, pero no sustituyen el corte trimestral certificado.

### Nivel C

Los artefactos completamente reproducibles o descargables no se respaldan por defecto salvo necesidad concreta.

## Destino externo obligatorio

Los respaldos oficiales de SineOS se almacenan en un **disco físicamente externo**.

La ruta no se codifica en scripts. Se define mediante:

```text
SINEOS_BACKUP_ROOT
```

La ruta configurada debe apuntar a una carpeta cuyo nombre sea:

```text
SineOsBackups
```

Ejemplo conceptual:

```text
<disco-externo>/SineOsBackups/
```

El flujo debe rechazar como respaldo oficial una ruta ubicada en el mismo filesystem físico principal del equipo.

## Identificador de cada respaldo

Cada ejecución utiliza el formato:

```text
SineOsBackups-DDMMAA-HHMM
```

Este identificador se emplea como:

- tag del snapshot Restic;
- nombre lógico del evento;
- referencia en el manifiesto;
- referencia en la bitácora GitHub.

Restic conserva internamente su propio snapshot ID; SineOS conserva además este nombre humano.

## Retención objetivo

Para Nivel A:

```text
7 diarios
4 semanales
6 mensuales
```

Para Nivel B:

```text
4 semanales
3 mensuales
```

La retención podrá ajustarse después de medir crecimiento real del repositorio.

No se aplica borrado/prune automático hasta validar primero creación, listado, restauración y verificación.

## PostgreSQL

El directorio de datos vivo no será el mecanismo primario de backup.

La estrategia principal será:

```text
PostgreSQL
   ↓
dump lógico consistente
   ↓
archivo de backup
   ↓
Restic
   ↓
repositorio cifrado
```

TD-003 debe definir y probar:

- formato del dump;
- backup;
- restore en entorno controlado;
- validación de tablas/datos;
- limpieza/retención.

## Knowledge Vault

El Vault es una fuente primaria de verdad y debe tener backup independiente del repositorio Git de SineOS.

TD-004 debe identificar su ruta real y validar:

- backup completo;
- exclusiones seguras;
- restauración a ruta temporal;
- integridad de notas y adjuntos;
- recuperación de estructura Obsidian.

## Secretos

Los secretos que sean necesarios para recuperar un servicio pueden formar parte de un backup únicamente dentro de un repositorio cifrado.

No se guardan en Git.

Ejemplos:

- PostgreSQL `.env`;
- Open WebUI `.env`;
- configuración privada bajo `~/.config/sineos/`.

La contraseña/clave que desbloquea el repositorio Restic no debe existir únicamente dentro del mismo repositorio.

## Open WebUI

El volumen persistente puede respaldarse, pero tiene menor prioridad que Vault y PostgreSQL.

Los archivos temporales creados bajo:

```text
~/.local/state/sineos/backups/
```

son copias de intervención y no sustituyen el repositorio de backup definitivo.

El backup manual actual de Open WebUI debe conservarse temporalmente hasta que exista un backup Restic validado o hasta que se decida explícitamente su eliminación.

## Snapshots Btrfs / Snapper

Uso permitido:

- antes de actualizaciones importantes;
- antes de cambios de sistema;
- rollback local;
- punto coherente para operaciones de backup cuando aporte valor.

Uso no permitido como única protección:

- fallo del SSD;
- robo;
- pérdida física;
- ransomware con acceso al mismo filesystem;
- corrupción del dispositivo.

## Verificación

### Cada ejecución

Un backup no se aprueba por el simple hecho de que Restic termine sin error.

Debe comprobarse:

- código de salida;
- existencia del snapshot;
- tag SineOS correcto;
- ausencia de errores de lectura;
- tamaño/archivos razonables;
- `restic check`;
- restauración real a una ubicación temporal;
- comprobación del contenido restaurado;
- validaciones específicas del componente.

Si no existe evidencia suficiente de que SineOS y sus componentes pueden recuperarse, el respaldo se considera **NO VALIDADO**.

### Periódicamente

Restic debe ejecutar comprobación de integridad del repositorio.

Objetivo inicial:

```text
restic check: mensual
```

### Restauración

La prueba de restore es obligatoria.

Objetivo:

```text
restore selectivo: mensual
restore de componentes críticos: al implementar cada componente y durante DR
```

Una restauración de prueba debe realizarse a una ruta temporal y nunca sobrescribir datos productivos durante la validación.

## Aislamiento

Al menos una copia debe residir fuera del almacenamiento interno principal.

Cuando exista una copia remota/off-site:

- debe estar cifrada antes de abandonar el equipo;
- no debe depender de la confidencialidad del proveedor;
- sus credenciales deben estar separadas de los datos respaldados.

## Bitácora versionada en GitHub

Cada respaldo aprobado se registra en:

```text
Documentation/Recovery/Backup-Log/
```

con el nombre:

```text
Respaldo-<COMMIT_DEL_EVENTO>.md
```

La regla completa está documentada en `Backup-Log/README.md`.

Debido a que el hash de Git depende del contenido del commit, el archivo no puede llamarse con el hash del mismo commit que lo contiene. SineOS utiliza dos commits:

```text
COMMIT A
registro del evento de respaldo
        ↓
obtener hash A
        ↓
Respaldo-<hash-A>.md
        ↓
COMMIT B
bitácora y sincronización
        ↓
push
        ↓
HEAD local = origin/main = main remoto
```

El ciclo solo queda cerrado después de comprobar el **COMMIT B sincronizado**.

El hash de COMMIT B no se escribe dentro del archivo creado por ese mismo commit. Se obtiene después de crear B, se conserva en el estado local privado y la sincronización remota se demuestra comprobando:

```text
HEAD local = origin/main = main remoto
```

`Documentation/Recovery/Backup-Status.md` conserva la fecha, tag, commit del evento y estado de sincronización del último respaldo validado.

## Recordatorio trimestral y aplicación nativa

SineOS implementará una aplicación nativa de mantenimiento siguiendo el estándar de `Native-Applications.md`.

Funciones mínimas:

- mostrar fecha del último chequeo de salud;
- mostrar fecha del último respaldo externo;
- indicar próximo vencimiento trimestral;
- ejecutar o lanzar la auditoría;
- ejecutar el flujo de respaldo cuando el disco esté disponible;
- mostrar validaciones;
- comprobar sincronización con GitHub;
- mantener estado pendiente hasta validación por commit.

El componente residente se implementa como servicio/timer de usuario, evitando un proceso activo permanente cuando no sea necesario.

## Automatización

La automatización se incorpora solo después de validar manualmente:

```text
backup
→ list
→ check
→ restore
→ comparación
```

No se programa un timer de backups no probados.

## Reportes

Los logs y reportes de backup deben guardarse bajo:

```text
~/.local/state/sineos/backup/
```

con permisos privados cuando puedan contener rutas o metadatos sensibles.

Los reportes no deben contener contraseñas ni claves.

## Fallos

Un backup con errores parciales no debe registrarse como exitoso.

Si falla:

1. conservar el último backup válido;
2. no ejecutar prune destructivo;
3. registrar el error;
4. identificar si el origen o destino está afectado;
5. corregir;
6. repetir;
7. validar restore cuando el fallo pueda afectar integridad.

## Disaster Recovery

TD-016 utilizará esta política para demostrar recuperación desde una situación donde el sistema principal no pueda utilizarse.

La prueba de DR debe asumir que:

- los snapshots locales pueden no existir;
- el SSD original puede estar perdido;
- Git aporta infraestructura y documentación;
- los backups aportan estado y datos privados.

## Definition of Done de un componente respaldado

Un componente solo puede declararse cubierto por backup cuando:

```text
[ ] datos incluidos definidos
[ ] exclusiones definidas
[ ] destino separado validado
[ ] backup ejecutado
[ ] integridad comprobada
[ ] restore a ubicación temporal ejecutado
[ ] resultado comparado
[ ] credenciales de recuperación disponibles
[ ] documentación actualizada
```

## Estado actual

A 24-09-2026:

```text
Política general                     VALIDADA
Restic                               IMPLEMENTADO / VALIDADO
Destino físico de backup             InfoDGRC / VALIDADO
Knowledge Vault                      INCLUIDO / RESTORE VALIDADO / TD-004
PostgreSQL backup + restore          TD-003 CERRADO
Disaster Recovery                    TD-016
Open WebUI                           RESTORE FUNCIONAL VALIDADO
Uptime Kuma                          RESTORE FUNCIONAL VALIDADO
Stirling PDF                         RESTORE FUNCIONAL VALIDADO
Snapshots Btrfs/Snapper              ROLLBACK, NO BACKUP
```

## Próximos pasos

1. integrar el flujo validado en SineOS Mantenimiento mediante TD-023;
2. ejecutar la prueba completa de Disaster Recovery de TD-016;
3. revisar el cierre formal de TD-004 para el Knowledge Vault;
4. medir el crecimiento del repositorio antes de aplicar prune;
5. evaluar una copia cifrada off-site cuando sea viable.
