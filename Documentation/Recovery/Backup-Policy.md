# SineOS — Política general de backups

**Estado:** Adoptada  
**Fecha:** 23-09-2026

## Propósito

Definir qué información de SineOS debe respaldarse, con qué prioridad, frecuencia, retención, verificación y criterios de recuperación.

Esta política es la base para los procedimientos específicos de PostgreSQL, Knowledge Vault, secretos, aplicaciones y Disaster Recovery.

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

Objetivo de pérdida máxima de datos:

```text
RPO objetivo: 24 horas
```

### Nivel B — Importante / reconstruible con pérdida de estado

| Componente | Tratamiento |
|---|---|
| Open WebUI data | backup periódico |
| Uptime Kuma data | backup periódico |
| Stirling PDF configuración/datos relevantes | backup según necesidad |
| configuración XFCE no totalmente versionada | backup mientras no sea 100 % reproducible |

Objetivo:

```text
RPO objetivo: 7 días
```

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

## Frecuencia base

### Nivel A

```text
diario
+
antes de operaciones de alto riesgo
+
después de cambios críticos cuando corresponda
```

### Nivel B

```text
semanal
+
antes de cambios destructivos o migraciones
```

### Nivel C

No se respalda por defecto salvo necesidad concreta.

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

Comprobar:

- código de salida;
- que se creó snapshot de backup;
- ausencia de errores de lectura;
- tamaño/archivos razonables.

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

A 23-09-2026:

```text
Política general                     VALIDADA DOCUMENTALMENTE
Restic                               SELECCIONADO / NO IMPLEMENTADO
Destino físico de backup             PENDIENTE DE INVENTARIO
Knowledge Vault                      TD-004
PostgreSQL backup + restore          TD-003
Disaster Recovery                    TD-016
Open WebUI backup manual temporal    EXISTENTE / MISMO EQUIPO
Snapshots Btrfs/Snapper              ROLLBACK, NO BACKUP
```

## Próximo paso

Inventariar almacenamiento disponible en el equipo y seleccionar el primer destino físicamente independiente antes de inicializar Restic.
