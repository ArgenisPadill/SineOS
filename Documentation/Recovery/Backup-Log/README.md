# SineOS — Bitácora de respaldos

Este directorio conserva evidencia versionada de los respaldos **validados** de SineOS.

No contiene datos respaldados, contraseñas, secretos, rutas privadas completas ni repositorios Restic.

## Nombre de cada registro

Cada respaldo aprobado genera un registro:

```text
Respaldo-<COMMIT_DEL_EVENTO>.md
```

El commit utilizado en el nombre es el **commit del evento de respaldo**.

Un archivo no puede incluir en su propio nombre el hash del commit que lo contiene, porque el nombre forma parte del contenido del commit y cambiaría el hash. Por ello SineOS utiliza un protocolo de dos commits.

## Protocolo de validación GitHub

```text
backup externo
    ↓
restic check
    ↓
restore de prueba
    ↓
comparación / validación
    ↓
actualizar Backup-Status.md
    ↓
COMMIT A = commit del evento de respaldo
    ↓
push COMMIT A
    ↓
crear Respaldo-<COMMIT_A>.md
    ↓
COMMIT B = commit de bitácora/sincronización
    ↓
push COMMIT B
    ↓
verificar HEAD local = origin/main = main remoto
    ↓
recordatorio puede marcarse como completado
```

La aplicación local guarda ambos hashes **después** de que existan:

- `event_commit`: COMMIT A;
- `sync_commit`: COMMIT B, obtenido después de crear y hacer push del commit.

El hash B no se escribe dentro del archivo comprometido por B.

## Contenido mínimo

Cada archivo `Respaldo-<commit>.md` registra únicamente metadatos no secretos:

```text
Fecha:
Tag SineOS:
Commit del evento:
Resultado Restic:
Resultado restore:
Estado:
```

El estado solo puede ser:

```text
VALIDADO
```

Los intentos fallidos se conservan en reportes locales privados y no se presentan como respaldos aprobados.

## Regla

> Un respaldo no cuenta como realizado hasta que pueda restaurarse y su evidencia quede sincronizada con GitHub.


### Regla de no autorreferencia

`Respaldo-<COMMIT_A>.md` puede contener el hash A porque ese hash ya existe antes de crear el archivo.

No puede contener el hash B del commit que incluye ese mismo archivo. El cierre del segundo commit se demuestra mediante el push y la igualdad del HEAD local/remoto; el hash B se conserva en el estado local privado de la aplicación.
