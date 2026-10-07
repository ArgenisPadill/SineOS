# SineOS Session & Power Experience — Experiencia de sesión y energía

**Fecha de decisión:** 07-10-2026  
**Estado:** planeación congelada / obligatorio para SDE 1.0  
**Proyecto maestro:** SineOS Desktop Experience (SDE)  
**Issue maestro:** https://github.com/ArgenisPadill/SineOS/issues/1  
**Plataforma objetivo:** Debian 13 (Trixie) + XFCE 4.20 + X11 + LightDM

## Propósito

SineOS debe presentar una experiencia coherente desde que se enciende el equipo hasta que se apaga.

La identidad gráfica no debe desaparecer durante:
- arranque;
- inicio de sesión;
- bloqueo;
- hibernación;
- reanudación;
- reinicio;
- apagado.

Durante el uso normal no deben mostrarse mensajes de estado del kernel o systemd, salvo cuando el usuario solicite diagnóstico o el sistema no pueda continuar normalmente.

La seguridad y la recuperación siempre tienen prioridad sobre la estética.

---

# 1. Experiencia de arranque

## Arranque normal

Se utilizará Plymouth como capa gráfica durante el arranque.

Flujo esperado:

```text
Firmware / UEFI
      ↓
GRUB (normalmente oculto o muy breve)
      ↓
Plymouth SineOS
      ↓
LightDM / Login SineOS
      ↓
Escritorio SDE
```

El arranque gráfico normal debe mostrar:
- identidad SineOS;
- una animación de carga sutil;
- texto corto opcional como `Iniciando…`.

Normalmente no debe mostrar:
- salida de comandos del kernel;
- mensajes de initramfs;
- estados de unidades systemd;
- logs de arranque desplazándose por pantalla.

## Acceso a diagnóstico

Los mensajes de arranque se ocultan, no se eliminan.

Requisitos:
- el diagnóstico debe seguir disponible cuando sea necesario;
- los estados de emergencia o falla deben mostrar información útil;
- la recuperación no debe depender de que Plymouth funcione;
- GRUB debe permanecer disponible como ruta de recuperación.

Una falla gráfica nunca debe ocultar indefinidamente un error crítico de arranque.

---

# 2. Experiencia de inicio de sesión

## Gestor de pantalla

Se mantiene LightDM.

Slick Greeter será la base preferida para el login de SineOS, salvo que durante la implementación aparezca una limitación bloqueante.

## Comportamiento de identidad del usuario

La pantalla normal de login debe:
- mostrar o preseleccionar el último usuario local válido o el usuario principal configurado;
- mostrar nombre e identidad visual del usuario;
- solicitar contraseña siempre;
- nunca almacenar ni autocompletar la contraseña;
- ofrecer `Cambiar usuario` como ruta secundaria en equipos multiusuario.

El usuario no debe volver a escribir su nombre de usuario en cada inicio de sesión normal.

El autologin no forma parte de la experiencia predeterminada de SDE.

## Integración visual

El login debe utilizar el mismo lenguaje visual que SDE:
- identidad SineOS;
- wallpaper o fondo SineOS;
- tipografía Inter;
- acento y tokens SineOS;
- espaciado y radios coherentes;
- contraste accesible;
- estados de foco de teclado visibles.

El login debe seguir siendo utilizable si falla la capa visual opcional.

---

# 3. Pantalla de bloqueo

## Locker

`xfce4-screensaver` será el locker preferido de SDE.

No se deben ejecutar varios lockers compitiendo al mismo tiempo.

## Bloqueo manual

`Super + L` bloquea inmediatamente la sesión actual.

El bloqueo manual:
- no suspende;
- no hiberna;
- no cierra sesión;
- conserva las aplicaciones en ejecución;
- oculta contenido sensible del escritorio;
- requiere la contraseña del usuario actual para desbloquear.

## UX de la pantalla de bloqueo

La pantalla de bloqueo debe mostrar:
- identidad SineOS;
- usuario actual;
- campo de contraseña;
- hora y fecha;
- estado de batería/corriente cuando aporte valor;
- indicador de distribución de teclado cuando sea relevante;
- acceso a accesibilidad cuando esté soportado.

No debe mostrar:
- previews de ventanas;
- contenido de mensajes;
- salida de terminal;
- notificaciones con contenido sensible.

Concepto visual:

```text
SineOS
hora / fecha

Usuario
[ Contraseña ]

Desbloquear
```

La pantalla de bloqueo debe verse relacionada con el login, pero debe quedar claro que se trata de una sesión ya iniciada y protegida.

## Seguridad al desbloquear

Requisitos:
- la contraseña siempre es obligatoria;
- Esc no debe saltarse el bloqueo;
- cerrar el prompt no debe exponer la sesión;
- la autenticación utiliza mecanismos normales de PAM/sistema;
- la personalización visual nunca sustituye ni debilita la autenticación.

---

# 4. Hibernación al cerrar la tapa

Cerrar la tapa de la laptop debe solicitar **hibernación**, no suspensión.

Política predeterminada de SDE:

```text
cerrar tapa
   ↓
hibernar
```

Antes de habilitar esta política en una máquina, la certificación SDE debe comprobar:
- que la hibernación esté soportada;
- configuración válida de swap/resume;
- restauración correcta de la sesión;
- recuperación correcta de pantallas;
- recuperación correcta de audio;
- recuperación del panel y dock;
- recuperación del compositor.

SDE no debe hacer fallback silencioso a suspensión si falla la hibernación.

Si la hibernación no está disponible o está rota, debe reportarse como una falla de configuración o certificación.

---

# 5. Experiencia al reanudar

Flujo esperado:

```text
Encender / reanudar
      ↓
Visual de reanudación SineOS
      ↓
Validación posterior a reanudación
      ↓
Pantalla de bloqueo SineOS
      ↓
Contraseña
      ↓
Sesión existente
```

Después de hibernar, el usuario debe autenticarse antes de regresar al escritorio.

## Validación posterior a reanudación

Ejecutar una validación de una sola vez después de reanudar.

Comprobar, cuando aplique:
- panel activo;
- estado del compositor;
- estado del dock;
- topología de pantallas visible;
- ventanas no perdidas fuera del área visible;
- salida de audio válida;
- ausencia de overlays obsoletos;
- configuración razonable de DPI y pantallas.

El validador termina al concluir y no debe convertirse en un daemon permanente.

Las reparaciones deben limitarse al componente que falló.

---

# 6. Política al estar conectada a corriente

SineOS utiliza TLP como capa de política energética.

No se agregará de forma predeterminada un segundo daemon que compita por la misma política de energía.

Cuando la laptop está conectada a corriente, la intención de SDE es:

**Priorizar rendimiento.**

Esto no significa fijar un governor específico de CPU para todos los equipos.

La implementación debe elegir parámetros apropiados de TLP según la ruta de CPU/driver certificada.

El comportamiento normal con corriente puede incluir:
- permitir CPU boost cuando corresponda;
- reducir restricciones agresivas de ahorro;
- priorizar capacidad de respuesta;
- conservar seguridad térmica;
- conservar protecciones propias del hardware.

Estado visible para el usuario:

```text
Corriente conectada
Modo de energía: Rendimiento
```

El feedback debe ser breve y no intrusivo.

---

# 7. Política de batería

Cuando se desconecta la corriente, la intención de SDE es:

**Priorizar eficiencia de batería sin sacrificar una respuesta utilizable.**

Estado visible:

```text
Usando batería
Modo de energía: Eficiente
```

El cambio debe ser automático mediante las políticas AC/BAT de TLP.

Política inicial:

| Batería | Comportamiento predeterminado |
|---|---|
| >20 % | modo de batería normal |
| <=20 % | aviso discreto de batería baja |
| <=10 % | aviso crítico |
| <=5 % | solicitar hibernación de emergencia |

Los umbrales son valores configurables, no constantes permanentes en código.

La implementación podrá ajustarlos después de pruebas reales de hardware.

## Hibernación de emergencia

La hibernación de emergencia solo debe habilitarse después de que la hibernación haya aprobado la certificación de esa máquina.

Si no existe hibernación segura, SDE no debe fingir que esa protección está disponible.

---

# 8. Apagado de pantalla mientras está bloqueada

Bloquear la sesión y apagar la pantalla son operaciones distintas.

Comportamiento esperado:
- `Super+L` bloquea inmediatamente;
- la pantalla puede apagarse después de un intervalo configurable de inactividad;
- la laptop permanece encendida salvo que aplique otra política explícita de energía;
- una entrada de teclado o mouse reactiva la pantalla y muestra el bloqueo SineOS;
- la contraseña sigue siendo obligatoria.

---

# 9. Experiencia de reinicio y apagado

Plymouth debe proporcionar también la transición gráfica para reinicio y apagado cuando sea técnicamente viable.

Reinicio normal:

```text
SineOS
Reiniciando…
```

Apagado normal:

```text
SineOS
Apagando…
```

Durante el uso normal no deben mostrarse mensajes de systemd o kernel desplazándose por pantalla.

Sin embargo:
- los errores críticos de apagado deben seguir siendo diagnosticables;
- los modos de recuperación o depuración pueden mostrar salida detallada;
- el pulido gráfico nunca debe impedir un apagado limpio.

---

# 10. Continuidad de sesión

El ciclo completo debe sentirse como el mismo sistema:

```text
ENCENDER
   ↓
Arranque SineOS
   ↓
Login SineOS
   ↓
Escritorio SDE
   ↓
Bloqueo / Hibernación / Reanudación
   ↓
Bloqueo SineOS
   ↓
Escritorio SDE
   ↓
Apagado / Reinicio SineOS
```

Durante el uso normal no debe parecer que el sistema cambia entre componentes Debian/XFCE visualmente no relacionados.

---

# 11. Reglas de seguridad

Obligatorio:
- sin autocompletado de contraseña;
- sin autologin predeterminado;
- el bloqueo siempre requiere contraseña;
- reanudar desde hibernación regresa a una sesión bloqueada;
- PAM y los mecanismos normales del sistema siguen siendo autoritativos;
- la pantalla bloqueada no filtra contenido de notificaciones;
- cerrar sesión y bloquear son acciones distintas;
- ninguna personalización visual puede debilitar autenticación o recuperación.

---

# 12. Comportamiento ante fallas y recuperación

Si falla Plymouth:
- el arranque continúa mostrando la salida normal del sistema.

Si falla la integración o tema de Slick Greeter:
- LightDM debe seguir siendo utilizable con una configuración de respaldo conocida.

Si falla `xfce4-screensaver`:
- SDE health/recovery debe detectar el problema;
- una falla de bloqueo se considera un defecto de seguridad;
- SDE debe ofrecer una ruta de fallback documentada.

Si falla la aplicación de política TLP:
- el sistema sigue siendo utilizable;
- SDE reporta la falla;
- no se habilita automáticamente otro daemon de energía que compita.

Si la hibernación no aprueba certificación:
- no se habilita hibernación al cerrar tapa hasta corregir el problema.

---

# 13. Criterios de aceptación de SDE 1.0

## Arranque
- arranque gráfico normal;
- sin texto rutinario de kernel/systemd;
- ruta de diagnóstico disponible;
- GRUB y recuperación accesibles.

## Login
- último usuario o usuario principal preseleccionado;
- contraseña siempre obligatoria;
- cambio de usuario disponible;
- sin autologin predeterminado;
- coherencia visual con SDE.

## Bloqueo
- Super+L bloquea inmediatamente;
- sesión en ejecución preservada;
- contraseña obligatoria;
- contenido sensible oculto;
- apagado de pantalla independiente del bloqueo.

## Hibernación
- cerrar tapa solicita hibernación;
- sin fallback silencioso a suspensión;
- reanudar restaura la sesión existente;
- pantalla de bloqueo visible después de reanudar.

## Energía
- política AC prioriza rendimiento;
- política BAT prioriza eficiencia;
- estados de batería baja y crítica visibles;
- hibernación de emergencia solo después de certificación.

## Apagado y reinicio
- transición gráfica SineOS;
- texto normal de apagado oculto;
- salida de diagnóstico disponible cuando sea necesaria.

## Recuperación
- personalizaciones de login, bloqueo y energía pueden revertirse a valores funcionales conocidos;
- la recuperación no depende de que la capa gráfica esté funcionando.

---

# Regla final

> SineOS debe sentirse como el mismo sistema desde que se enciende hasta que se apaga, mientras autenticación, recuperación y seguridad energética siempre tienen prioridad sobre el acabado visual.
