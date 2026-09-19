# SineOS — PostgreSQL 18

## 1. Propósito

Este documento describe la implementación y operación de PostgreSQL dentro de SineOS.

PostgreSQL funciona como uno de los servicios de base de datos principales de la plataforma y se ejecuta mediante Podman rootless.

Los objetivos de esta implementación son:

- aislamiento mediante contenedores;
- ejecución sin privilegios root;
- persistencia de datos;
- reproducibilidad;
- facilidad de migración;
- monitoreo del estado del servicio;
- separación entre configuración, datos y secretos.

La implementación actual utiliza PostgreSQL 18.

---

## 2. Arquitectura

La arquitectura general es:

```text
Debian 13
   ↓
Podman rootless
   ↓
Stack SineOS PostgreSQL
   ↓
PostgreSQL 18
   ↓
Volumen persistente
```

El servicio forma parte de:

```text
/home/argenis/Workspace/SineOS
```

dentro de la estructura:

```text
Containers/
├── stacks/
│   └── postgres/
├── volumes/
├── backups/
├── configs/
├── secrets/
└── logs/
```

El repositorio Git contiene la definición de infraestructura.

Los datos persistentes no deben tratarse como código fuente.

---

## 3. Runtime de contenedores

PostgreSQL se ejecuta utilizando:

```text
Podman 5.4.2
```

en modalidad:

```text
rootless
```

La ejecución rootless reduce la necesidad de privilegios administrativos para operar los contenedores de SineOS.

El entorno utiliza:

```text
cgroup v2
netavark
pasta
```

como parte de la infraestructura de contenedores.

---

## 4. PostgreSQL

Versión utilizada:

```text
PostgreSQL 18
```

La versión 18 introdujo consideraciones específicas relacionadas con la ubicación de los datos dentro de la imagen oficial.

Durante la configuración de SineOS se ajustó el volumen persistente para utilizar:

```text
/var/lib/postgresql
```

en lugar de asumir configuraciones utilizadas tradicionalmente por versiones anteriores.

Esta decisión debe conservarse durante futuras modificaciones del stack.

---

## 5. Stack

La definición del servicio se encuentra en:

```text
Containers/stacks/postgres/
```

El stack forma parte del repositorio Git de SineOS.

La configuración versionada debe permitir reconstruir el servicio sin versionar directamente los datos de PostgreSQL.

Separación conceptual:

```text
compose/configuración
        ↓
      Git

datos PostgreSQL
        ↓
persistencia local / backup
```

---

## 6. Persistencia

PostgreSQL utiliza almacenamiento persistente fuera de la capa efímera del contenedor.

Esto significa que eliminar o recrear el contenedor no debe implicar automáticamente eliminar la base de datos.

Flujo:

```text
Contenedor PostgreSQL
        ↓
mount
        ↓
/var/lib/postgresql
        ↓
directorio persistente del host
```

La persistencia debe comprobarse siempre después de cambios significativos en:

- imagen;
- versión;
- compose;
- permisos;
- UID mapping;
- migraciones.

---

## 7. PostgreSQL 18 y el volumen de datos

Para PostgreSQL 18 se adoptó el mount:

```text
/var/lib/postgresql
```

Esta configuración fue validada funcionalmente.

No debe modificarse a una ruta histórica de PostgreSQL únicamente por costumbre sin comprobar primero el comportamiento de la imagen utilizada.

Principio:

> La configuración debe corresponder a la versión real del servicio.

---

## 8. UID rootless

Debido al uso de Podman rootless, los usuarios dentro del contenedor se representan mediante subordinate UID/GID en el host.

Durante la implementación se verificó que el usuario PostgreSQL se mapea en el host al UID:

```text
100998
```

Este valor explica por qué los archivos persistentes pueden aparecer en el host con un UID diferente al usuario local.

No debe corregirse mediante `chown` arbitrario sin comprender primero el namespace de usuarios utilizado por Podman.

---

## 9. Rootless user namespace

Conceptualmente:

```text
usuario postgres
dentro del contenedor
        ↓
user namespace
        ↓
UID subordinado
en el host
```

Por esta razón:

```text
UID contenedor ≠ UID visible en host
```

puede ser completamente normal.

Los permisos del almacenamiento deben evaluarse teniendo en cuenta el mapping rootless.

---

## 10. Healthcheck

El stack de PostgreSQL incluye comprobación de salud.

El healthcheck permite distinguir entre:

```text
contenedor iniciado
```

y:

```text
PostgreSQL realmente disponible
```

Esto es importante porque un proceso de contenedor puede existir mientras el servicio interno todavía está inicializando o presenta un problema.

El estado de salud fue validado durante la implementación inicial.

---

## 11. Validación funcional

La implementación de PostgreSQL fue probada verificando:

- creación del contenedor;
- inicio correcto;
- healthcheck;
- persistencia;
- acceso al servicio;
- comportamiento después de recrear el contenedor;
- permisos del almacenamiento rootless.

El stack se considera funcional.

Esto no significa que todas las tareas de producción, seguridad y recuperación estén terminadas.

---

## 12. Contraseña de PostgreSQL

PostgreSQL requiere credenciales para su operación.

Las contraseñas no deben almacenarse en:

- README;
- documentación;
- scripts públicos;
- historial Git;
- archivos versionados;
- ejemplos reales de configuración.

Principio:

> Git contiene la infraestructura, no los secretos.

La contraseña utilizada durante la instalación inicial debe considerarse un secreto operacional.

Existe una tarea pendiente para rotar las credenciales como parte del endurecimiento futuro del sistema.

---

## 13. Secrets

La estructura de SineOS contempla:

```text
Containers/secrets/
```

para la administración de secretos relacionados con servicios.

Los secretos reales no deben ser versionados.

La estrategia definitiva de gestión de secretos todavía debe formalizarse.

Opciones futuras pueden incluir mecanismos específicos de Podman o un sistema dedicado de gestión de secretos.

---

## 14. Inicio automático

Actualmente existe un mecanismo de inicio mediante servicio systemd de usuario.

Este mecanismo permite iniciar PostgreSQL automáticamente dentro del entorno del usuario.

Sin embargo, debe considerarse:

```text
solución funcional temporal
```

y no la arquitectura definitiva.

La dirección prevista para SineOS es utilizar Quadlet.

---

## 15. Quadlet

Quadlet permite describir contenedores y servicios Podman mediante archivos integrados con systemd.

La intención futura es reemplazar el mecanismo temporal de autostart por una definición Quadlet mantenible.

Estado:

```text
PENDIENTE
```

---

## 16. Problema detectado en Quadlet

Durante las pruebas se detectó una discrepancia de nombre de red.

La configuración Quadlet hacía referencia a:

```text
Network=postgres
```

mientras que la red real utilizada por el stack corresponde a:

```text
sineos-postgres
```

Esta diferencia debe resolverse antes de considerar terminada la migración a Quadlet.

No debe activarse una configuración Quadlet sin validar primero la red real disponible.

---

## 17. Estado del autostart

Estado actual:

| Componente | Estado |
|---|---|
| PostgreSQL container | Operativo |
| Persistencia | Validada |
| Healthcheck | Validado |
| systemd user autostart | Funcional |
| Quadlet | Pendiente |
| Red Quadlet | Requiere corrección |

El mecanismo actual puede mantenerse mientras se diseña y valida correctamente la migración.

---

## 18. Operación básica

Antes de realizar acciones administrativas debe comprobarse el estado real del servicio.

Ejemplos de operaciones habituales:

```text
consultar contenedores
consultar estado
consultar logs
iniciar servicio
detener servicio
reiniciar servicio
comprobar healthcheck
```

Las acciones destructivas sobre datos no deben ejecutarse como parte de una rutina normal de diagnóstico.

---

## 19. Diagnóstico por capas

Cuando PostgreSQL presente un problema debe evitarse asumir inmediatamente que la base de datos está dañada.

Orden recomendado:

```text
Host
 ↓
Podman
 ↓
Red
 ↓
Contenedor
 ↓
Healthcheck
 ↓
Logs
 ↓
PostgreSQL
 ↓
Datos
```

Este orden ayuda a distinguir un problema de infraestructura de un problema real de base de datos.

---

## 20. Auditoría SineOS

El auditor de SineOS incluye una sección específica:

```text
13.1 - POSTGRESQL SINEOS
```

Esta sección fue incorporada después de la implementación del stack PostgreSQL.

El script se encuentra en:

```text
Scripts/Audit/sineos-audit.sh
```

Su propósito es recopilar información diagnóstica sin realizar cambios deliberados en la configuración del sistema.

Los reportes generados no deben versionarse.

---

## 21. Reportes de auditoría

Los reportes del auditor se generan actualmente bajo:

```text
Documentation/Audit/
```

Los archivos de reporte con extensión `.txt` están excluidos mediante `.gitignore`.

Esto evita publicar accidentalmente información local relacionada con:

- host;
- red;
- usuarios;
- servicios;
- contenedores;
- configuración;
- almacenamiento.

La documentación permanente puede residir dentro de `Documentation/`, pero los reportes generados son artefactos locales.

---

## 22. Backups

La estructura del proyecto contempla:

```text
Containers/backups/
```

Sin embargo, disponer del directorio no equivale a tener una política completa de backup.

Todavía debe definirse formalmente:

- frecuencia;
- método;
- retención;
- cifrado;
- ubicación externa;
- validación;
- restauración;
- pruebas periódicas.

La estrategia de backup de PostgreSQL debe considerarse una tarea pendiente.

---

## 23. Backup lógico

Una futura estrategia puede utilizar herramientas nativas de PostgreSQL para generar backups lógicos.

La implementación definitiva deberá documentar:

- bases incluidas;
- formato;
- compresión;
- automatización;
- retención;
- verificación.

No debe considerarse implementada hasta realizar y validar una restauración.

Principio:

> Un backup no está validado hasta que puede restaurarse.

---

## 24. Backup físico

Si en el futuro se implementan backups físicos, deberán tener en cuenta:

- consistencia;
- versión PostgreSQL;
- permisos;
- UID mapping;
- almacenamiento;
- estado del servicio.

Copiar arbitrariamente el directorio de datos mientras PostgreSQL está activo no debe considerarse automáticamente una estrategia válida de recuperación.

---

## 25. Restauración

Debe existir eventualmente un procedimiento reproducible para:

```text
instalar Podman
        ↓
obtener repositorio SineOS
        ↓
crear almacenamiento
        ↓
restaurar PostgreSQL
        ↓
levantar servicio
        ↓
validar datos
```

Este procedimiento será especialmente importante durante una migración de hardware.

Actualmente debe considerarse pendiente.

---

## 26. Migración

Uno de los objetivos de SineOS es evitar reconstruir manualmente todo el entorno al cambiar de computadora.

Para PostgreSQL deben distinguirse dos elementos:

### Infraestructura

Se recupera desde Git:

```text
compose
configuración
documentación
scripts
```

### Datos

Se recuperan desde:

```text
backup
```

Git no debe utilizarse como mecanismo de backup de la base de datos.

---

## 27. Monitoreo

La arquitectura de SineOS contempla herramientas como:

```text
Prometheus
Grafana
Loki
Netdata
```

Sin embargo, la existencia de directorios o stacks previstos no significa que PostgreSQL ya esté completamente integrado con ellos.

El monitoreo avanzado debe documentarse únicamente cuando sea implementado y validado.

---

## 28. Seguridad

PostgreSQL debe operar bajo los principios generales de seguridad de SineOS:

- mínimo privilegio;
- rootless cuando sea viable;
- secretos fuera de Git;
- exposición de red mínima;
- backups protegidos;
- credenciales rotables;
- logs revisables;
- configuración reproducible.

La implementación funcional actual todavía tiene tareas de hardening pendientes.

---

## 29. Exposición de red

La disponibilidad de PostgreSQL debe limitarse a los componentes que realmente necesiten acceso.

No debe exponerse indiscriminadamente a interfaces externas.

Antes de modificar puertos o redes debe comprobarse:

- quién necesita conectarse;
- desde dónde;
- qué red Podman se utiliza;
- qué política de firewall existe.

La política definitiva se integrará con el futuro hardening de red de SineOS.

---

## 30. Relación con pgAdmin

La arquitectura de contenedores contempla un stack separado para:

```text
pgAdmin
```

PostgreSQL y pgAdmin deben mantenerse como servicios independientes.

La existencia del directorio de stack no implica que pgAdmin esté necesariamente operativo.

Su estado debe documentarse cuando sea configurado y validado.

---

## 31. Estructura recomendada

Conceptualmente:

```text
Containers/
├── stacks/
│   ├── postgres/
│   │   └── compose.yaml
│   └── pgadmin/
│
├── volumes/
│   └── postgres/
│
├── backups/
│
├── configs/
│
├── secrets/
│
└── logs/
```

La ubicación exacta de archivos debe mantenerse coherente con el repositorio real.

---

## 32. Actualización de PostgreSQL

Una actualización mayor de PostgreSQL no debe tratarse como una simple actualización de imagen.

Antes de cambiar de versión mayor debe evaluarse:

```text
compatibilidad
formato de datos
migración
backup
rollback
extensiones
clientes
```

Debe existir un backup validado antes de realizar una migración mayor.

---

## 33. Actualización de imagen

Antes de actualizar la imagen del contenedor:

1. revisar versión actual;
2. revisar release objetivo;
3. revisar cambios incompatibles;
4. asegurar backup;
5. detener de manera controlada si corresponde;
6. actualizar;
7. validar healthcheck;
8. validar acceso;
9. validar datos;
10. revisar logs.

No debe utilizarse una política de actualización ciega para una base de datos persistente.

---

## 34. Troubleshooting

### El contenedor no inicia

Comprobar:

```text
Podman
compose
logs
volumen
permisos
UID mapping
red
```

### PostgreSQL aparece iniciado pero no responde

Comprobar el healthcheck y los logs antes de modificar datos.

### Permission denied en almacenamiento

Recordar que el stack utiliza Podman rootless.

Comprobar el namespace y el UID mapping antes de utilizar `chown`.

El UID observado durante la implementación fue:

```text
100998
```

### Quadlet no encuentra la red

Comprobar la discrepancia conocida:

```text
Network=postgres
```

frente a:

```text
sineos-postgres
```

### Los datos desaparecen al recrear el contenedor

Detener la operación y verificar inmediatamente el mount persistente.

No continuar creando o inicializando instancias hasta comprender qué directorio está siendo utilizado.

---

## 35. Validación después de cambios

Después de cualquier modificación significativa comprobar:

```text
[ ] El compose es válido
[ ] Podman puede crear el contenedor
[ ] PostgreSQL inicia
[ ] Healthcheck es correcto
[ ] El volumen está montado
[ ] Los datos persisten
[ ] Los permisos son correctos
[ ] La red funciona
[ ] Los logs no muestran errores críticos
[ ] Las credenciales funcionan
[ ] No se agregaron secretos a Git
```

---

## 36. Deuda técnica

Pendientes conocidos:

```text
[ ] Migrar autostart systemd temporal a Quadlet
[ ] Corregir referencia de red del Quadlet
[ ] Validar Quadlet después de la corrección
[ ] Rotar contraseña PostgreSQL
[ ] Formalizar gestión de secretos
[ ] Definir política de backup
[ ] Automatizar backups
[ ] Definir retención
[ ] Probar restauración completa
[ ] Documentar recuperación ante desastre
[ ] Integrar monitoreo cuando corresponda
[ ] Revisar hardening de red
```

---

## 37. Principios operativos

### Persistencia primero

Antes de modificar un contenedor con datos debe comprenderse dónde se encuentra la persistencia.

### Rootless no significa sin permisos

Los UID del contenedor pueden mapearse a UID subordinados en el host.

### Contenedor no equivale a servicio saludable

Debe utilizarse el healthcheck.

### Git no es backup de datos

Git conserva infraestructura y documentación.

### Backup no equivale a recuperación

La restauración debe probarse.

### Automatización después de comprender el proceso

Quadlet, backups y mantenimiento deben automatizarse después de validar manualmente el comportamiento correcto.

---

## 38. Estado actual

| Elemento | Estado |
|---|---|
| PostgreSQL 18 | Operativo |
| Podman rootless | Operativo |
| Persistencia | Validada |
| Mount `/var/lib/postgresql` | Validado |
| UID mapping | Identificado |
| Healthcheck | Validado |
| Auditoría PostgreSQL | Integrada |
| Autostart systemd user | Funcional temporal |
| Quadlet | Pendiente |
| Backup automatizado | Pendiente |
| Restauración validada | Pendiente |
| Rotación de credenciales | Pendiente |
| Hardening final | Pendiente |

---

## 39. Estado

PostgreSQL 18 se encuentra operativo dentro de SineOS utilizando Podman rootless y almacenamiento persistente.

La implementación funcional actual puede representarse como:

```text
Debian 13
   ↓
Podman rootless
   ↓
PostgreSQL 18
   ↓
/var/lib/postgresql
   ↓
persistencia del host
```

El servicio ha sido validado funcionalmente.

Las siguientes tareas importantes son:

```text
Quadlet
backup
restauración
gestión de secretos
hardening
```

Estas tareas deben completarse antes de considerar PostgreSQL una implementación operativa completamente cerrada.
