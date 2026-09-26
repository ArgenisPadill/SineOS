# SineOS — Mantenimiento

**Estado:** VALIDADO  
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
        motor de backup certificado
               ↓
        SineOsBackups + Restic + restore + validación + GitHub
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



### Protección contra registro duplicado

Si el último reporte de auditoría corresponde a la misma fecha —o una anterior— que el ciclo ya validado localmente, la aplicación deshabilita **Registrar y sincronizar con GitHub** y el núcleo rechaza también la operación.

Esto evita crear commits redundantes o volver a cerrar el mismo ciclo por error.

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

El backup permanece deshabilitado hasta que se configure y valide explícitamente el destino externo.

## Backup externo

La interfaz integra el motor de respaldo externo certificado. El flujo crea el snapshot Restic, ejecuta `restic check`, restaura temporalmente el respaldo, valida su contenido y registra la evidencia mediante el protocolo Git de dos commits.

El flujo valida `SINEOS_BACKUP_ROOT`, UUID y serial del disco, identidad del repositorio Restic, estado Git, PostgreSQL, Knowledge Vault y los volúmenes seleccionados. PostgreSQL, Uptime Kuma, Open WebUI y Stirling PDF se validan funcionalmente desde la restauración temporal. La evidencia se registra en `Backup-Status.md` y `Backup-Log/Respaldo-<commit>.md`.

## Instalación

Desde la raíz de SineOS:

```bash
bash Scripts/Maintenance/install-sineos-maintenance.sh install
```

El instalador valida dependencias, crea estado y configuración privados, instala un **wrapper local** en `~/.local/bin`, registra el lanzador XFCE, crea service/timer de usuario y habilita el timer. No requiere root. El wrapper ejecuta Python sin modificar permisos de archivos versionados del repositorio.

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

La desinstalación retira timer, service, lanzador y wrapper de ejecución. Conserva deliberadamente `state.json` y `maintenance.env`.

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
[x] sintaxis Python
[x] sintaxis Bash
[x] instalación
[x] lanzador XFCE
[x] GUI GTK3
[x] estado inicial
[x] adopción de la auditoría v1.2.3
[x] timer habilitado y activo
[x] servicio de recordatorio termina en success con ciclo vigente
[x] creación de estado privado 700/600
[x] persistencia tras desinstalación / reinstalación
[x] desinstalación / rollback
[x] persistencia tras nueva sesión de XFCE o reinicio
[x] gate GitHub no interactivo mediante GCR validado
```

La función de commit/push se validará en el siguiente ciclo real o mediante una prueba controlada que no falsifique la fecha trimestral.


## Validación de instalación — 24-09-2026

Comprobado en el equipo real:

```text
Python                         OK
Bash                           OK
GTK 3.24.49                    OK
wrapper ~/.local/bin           OK
timer enabled                  OK
timer active                   OK
state dir 700                  OK
state.json 600                 OK
maintenance.env 600            OK
SINEOS_BACKUP_ENABLED=0        OK
Git final limpio               OK
GitHub sincronizado            OK
```

El primer instalador modificaba únicamente los modos de tres archivos versionados. Se verificó que su contenido era idéntico a Git, se restauraron los modos y se corrigió el instalador para usar un wrapper local sin volver a modificar archivos rastreados.

TD-022 permanece abierto hasta validar la adopción inicial, la GUI, el comportamiento del recordatorio y el rollback.


## Validación de adopción inicial — 24-09-2026

La auditoría validada del mismo día fue adoptada como inicio del primer ciclo trimestral administrado por la aplicación.

```text
Fecha validada       2026-09-24
Próxima salud        2026-12-24
Salud vencida        no
Auditor              1.2.3
Commit de referencia 62d725c17f4a9903976c5a63fefbd966154440c4
Backup activo        no
Git sincronizado     sí
```

Permisos comprobados:

```text
~/.local/state/sineos-maintenance            700
~/.local/state/sineos-maintenance/state.json 600
```

El servicio de recordatorio fue ejecutado manualmente con el ciclo vigente y terminó con:

```text
Result=success
ExecMainStatus=0
ActiveState=inactive
SubState=dead
```

El timer permanece `enabled` y `active`.

TD-022 continúa abierto exclusivamente para validar la GUI/lanzador, persistencia tras una nueva sesión y rollback/desinstalación.


## Validación de GUI y lanzador — 24-09-2026

Se abrió la aplicación mediante el lanzador XFCE con `gtk-launch sineos-maintenance`.

Resultado visual y funcional:

```text
Título                         SineOS · Mantenimiento
Estado general                 SineOS está al día
Salud trimestral               VALIDADA
Última validación              24-09-2026
Próxima validación             24-12-2026
Commit mostrado                62d725c17f4a…
Adoptar validación actual      deshabilitado
Registrar/sincronizar GitHub   deshabilitado
Ejecutar auditoría             habilitado
Backup externo                 VALIDADO / OPERATIVO
Git                            limpio
GitHub                         sincronizado
```

La sección de detalles técnicos mostró rama `main`, repositorio limpio, HEAD remoto sincronizado y el reporte local más reciente.

Abrir y cerrar la GUI no generó cambios en el working tree.


## Validación de rollback y reinstalación — 24-09-2026

Se ejecutó una desinstalación real de la integración y una reinstalación posterior.

La desinstalación retiró wrapper, lanzador XFCE y unidades systemd de usuario. El timer quedó deshabilitado/retirado.

Los archivos privados `state.json` y `maintenance.env` conservaron exactamente su contenido durante el rollback.

Tras reinstalar se recuperó el mismo ciclo:

```text
Salud validada     2026-09-24
Próxima salud      2026-12-24
Salud vencida      no
Commit salud       62d725c17f4a9903976c5a63fefbd966154440c4
Backup activo      no
Git sincronizado   sí
```

El timer quedó `loaded`, `active` y `enabled`. Los permisos volvieron a ser 700 para directorios privados y 600 para archivos privados. El working tree final quedó limpio.

Para cerrar TD-022 falta únicamente comprobar el mismo estado después de una nueva sesión de XFCE o un reinicio real.


## Validación post-inicio — 24-09-2026

Después de iniciar una nueva sesión se comprobó:

```text
Salud validada          2026-09-24
Próxima salud           2026-12-24
Salud vencida           no
Commit salud            62d725c17f4a9903976c5a63fefbd966154440c4
Backup activo           no
Git sincronizado        sí
Timer LoadState         loaded
Timer ActiveState       active
Timer UnitFileState     enabled
Wrapper                 disponible
Lanzador XFCE           disponible
state dir               700
state.json              600
config dir              700
maintenance.env         600
Working tree            limpio
```

La persistencia funcional queda validada.

Durante el primer acceso a GitHub de la nueva sesión, SSH solicitó nuevamente la passphrase de `~/.ssh/id_ed25519_sineos`. Tras introducirla, Git operó normalmente.

Antes de cerrar TD-022 debe validarse un flujo seguro para que el gate GitHub iniciado desde la GUI pueda disponer de la clave cifrada sin depender de una terminal interactiva ni retirar la passphrase.


## Autenticación GitHub desde la GUI

Las operaciones remotas de Git iniciadas por SineOS · Mantenimiento utilizan un entorno SSH propio y no interactivo.

Cuando existe:

```text
$XDG_RUNTIME_DIR/gcr/ssh
```

la aplicación usa ese socket GCR mediante `SSH_AUTH_SOCK`.

Además establece:

```text
GIT_TERMINAL_PROMPT=0
SSH_ASKPASS_REQUIRE=never
GIT_SSH_COMMAND=ssh -o BatchMode=yes
```

Objetivos:

- conservar la passphrase de la clave SineOS;
- no sustituir ni detener el `ssh-agent` normal de XFCE;
- evitar diálogos ocultos o esperas indefinidas desde la GUI;
- permitir `git ls-remote` y `git push` cuando GCR ya dispone de la clave desbloqueada;
- fallar de forma explícita si no existe una credencial utilizable.

La sesión validada del 24-09-2026 mostró simultáneamente:

```text
agente XFCE      /tmp/ssh-.../agent...
socket GCR       /run/user/1000/gcr/ssh
clave SineOS GCR presente
GitHub GCR       autenticación correcta
git ls-remote    exit 0 sin interacción
```

La aplicación no modifica la configuración global de SSH ni elimina la passphrase.


## Validación final GCR — 24-09-2026

Se ejecutó la aplicación con el `SSH_AUTH_SOCK` normal sustituido deliberadamente por una ruta inexistente.

El núcleo seleccionó:

```text
SSH_AUTH_SOCK       /run/user/1000/gcr/ssh
GIT_TERMINAL_PROMPT 0
SSH_ASKPASS_REQUIRE never
GIT_SSH_COMMAND     ssh -o BatchMode=yes
```

Resultado:

```text
branch       main
clean        True
local_head   42b58b931f9c18e9f8d809308f8d32d667779a02
remote_head  42b58b931f9c18e9f8d809308f8d32d667779a02
synced       True
```

La aplicación siguió mostrando `Git sincronizado: sí`.

El agente SSH normal de XFCE permaneció intacto y conservó la clave SineOS.

Con esta prueba queda validado el mecanismo no interactivo usado por las operaciones remotas de la GUI. El `git push` utiliza exactamente el mismo entorno GCR; su ejecución real se comprobará naturalmente en el siguiente ciclo que genere un estado nuevo, sin fabricar una auditoría ficticia.

TD-022 queda cerrado.
