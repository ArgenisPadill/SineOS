# SineOS — Mantenimiento

**Estado:** Implementación pendiente de validación local  
**Componente:** Aplicación nativa de mantenimiento  
**Plataforma:** Debian 13 + XFCE

## Propósito

SineOS · Mantenimiento convierte el ciclo trimestral de salud y respaldo en una operación visible y persistente del escritorio.

La aplicación no reemplaza los auditores ni las herramientas de backup. Su función es coordinarlos, mostrar estado, recordar vencimientos y aplicar el gate de validación con GitHub.

## Arquitectura

```text
SineOS · Mantenimiento
        │
        ├── salud trimestral
        │      ↓
        │   sineos-health-audit.sh
        │      ↓
        │   reporte local privado
        │      ↓
        │   Health-Status.md
        │      ↓
        │   commit + push + verificación origin/main
        │
        └── respaldo externo
               ↓
             TD-021
               ↓
        SineOsBackups + Restic + restore
```

## Código

```text
Apps/Maintenance/
├── sineos-maintenance.py
└── maintenance_core.py

Scripts/Maintenance/
├── install-sineos-maintenance.sh
└── run-health-audit-interactive.sh
```

`sineos-maintenance.py` implementa la interfaz GTK3.

`maintenance_core.py` contiene la lógica operativa: calendario trimestral real, estado local, interpretación del auditor, gate Git/GitHub, configuración de backup y recordatorios.

## Frecuencia trimestral

La fecha siguiente se calcula sumando **tres meses calendario** a la última validación. No se aproxima como 90 días.

Ejemplo:

```text
24-09-2026
      ↓
24-12-2026
```

## Recordatorio persistente

El recordatorio se implementa mediante un timer de usuario:

```text
sineos-maintenance-reminder.timer
```

El timer se evalúa diariamente con `OnCalendar=daily`, `Persistent=true` y un retraso aleatorio de hasta 15 minutos.

Esto no significa que la auditoría sea diaria. El timer solo pregunta si el ciclo trimestral ya venció. Si no venció, no notifica. Si venció, genera una notificación y seguirá haciéndolo en futuras evaluaciones mientras el estado local permanezca pendiente.

Cerrar visualmente una notificación **no valida el mantenimiento**.

## Gate GitHub

La validación trimestral solo queda cerrada cuando existe evidencia de sincronización con GitHub.

Para ciclos futuros:

```text
auditoría RESULTADO: OK
        ↓
Git limpio + main sincronizado
        ↓
actualizar Health-Status.md
        ↓
commit específico de salud
        ↓
git push origin main
        ↓
verificar HEAD local = origin/main
        ↓
guardar fecha + hash local
        ↓
recordatorio cerrado
```

La aplicación solo añade al commit `Documentation/Operations/Health-Status.md`. Si detecta otros archivos staged, cancela la operación.

El hash se guarda localmente después de comprobar que el remoto coincide con el commit nuevo.

## Primera adopción

La primera validación trimestral fue ejecutada manualmente antes de instalar la aplicación:

```text
24-09-2026
sineos-health-audit v1.2.3
21 OK
0 advertencias
0 errores
RESULTADO: OK
```

Por ello la primera instalación permite **Adoptar validación actual**. Esta operación registra localmente la auditoría válida existente únicamente si el último reporte es OK, la rama es `main`, el working tree está limpio y HEAD local coincide con `origin/main`.

## Auditoría desde la aplicación

El botón **Ejecutar auditoría** abre el emulador de terminal predeterminado de XFCE mediante `exo-open --launch TerminalEmulator` y ejecuta `Scripts/Maintenance/run-health-audit-interactive.sh`.

El wrapper solicita `sudo` únicamente para habilitar las lecturas administrativas ya usadas por el auditor. La aplicación gráfica no se ejecuta como root.

## Estado local

```text
~/.local/state/sineos-maintenance/state.json
```

Permisos esperados: directorio 700 y archivo 600.

El estado contiene fecha de última validación, hash del commit, versión del auditor y futuro estado de backup. No contiene secretos.

## Configuración local

```text
~/.config/sineos/maintenance.env
```

Permisos: 600.

Estado inicial:

```text
SINEOS_BACKUP_ENABLED=0
# SINEOS_BACKUP_ROOT=/ruta/del/disco/SineOsBackups
```

El backup queda deliberadamente deshabilitado hasta terminar TD-021.

## Backup externo

La interfaz reserva el bloque de respaldo, pero en esta versión el motor externo está **deshabilitado**. No ejecuta Restic, no monta discos y no escribe en `SineOsBackups`.

TD-021 debe implementar y validar primero detección del disco externo, `SINEOS_BACKUP_ROOT`, PostgreSQL, Vault, volúmenes seleccionados, Restic, `restic check`, restore temporal, comparación y bitácora `Respaldo-<commit>.md`.

## Instalación

Desde la raíz de SineOS:

```bash
bash Scripts/Maintenance/install-sineos-maintenance.sh install
```

El instalador valida dependencias, crea estado y configuración privados, instala un enlace en `~/.local/bin`, registra el lanzador XFCE, crea service/timer de usuario y habilita el timer. No requiere root.

## Estado

```bash
bash Scripts/Maintenance/install-sineos-maintenance.sh status
```

## Adoptar la validación inicial

```bash
bash Scripts/Maintenance/install-sineos-maintenance.sh adopt-current
```

## Desinstalación

```bash
bash Scripts/Maintenance/install-sineos-maintenance.sh uninstall
```

La desinstalación retira timer, service, lanzador y enlace de ejecución. Conserva deliberadamente `state.json` y `maintenance.env`.

## Dependencias

- Python 3;
- Python GI;
- GTK3;
- Git;
- `notify-send` / `libnotify-bin`;
- `exo-open` / XFCE Exo;
- systemd user session.

## Seguridad

- GUI ejecutada como usuario normal;
- sin daemon root;
- sin privilegios persistentes;
- estado y configuración privados;
- no almacena secretos en Git;
- valida Git antes y después del push;
- no mezcla cambios del usuario en el commit de salud;
- no habilita backup antes de validarlo.

## Validación pendiente

Antes de cerrar TD-022 deben comprobarse:

```text
[ ] sintaxis Python
[ ] sintaxis Bash
[ ] instalación
[ ] lanzador XFCE
[ ] estado inicial
[ ] adopción de la auditoría v1.2.3
[ ] timer habilitado y activo
[ ] ausencia de notificación mientras el ciclo esté vigente
[ ] persistencia del estado
[ ] desinstalación / rollback
```

La función de commit/push se validará en el siguiente ciclo real o mediante una prueba controlada que no falsifique la fecha trimestral.
