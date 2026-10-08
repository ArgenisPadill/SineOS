# SDE — Privacidad, permisos y acceso remoto

**Fecha de decisión:** 07-10-2026  
**Estado:** planeación congelada / obligatorio para SDE 1.0  
**Issue maestro:** https://github.com/ArgenisPadill/SineOS/issues/1

## Principio

SineOS solo debe interrumpir al usuario con permisos cuando existe una razón real de privacidad, seguridad o privilegios. No se duplican diálogos que ya gestione correctamente una aplicación.

# Permisos sensibles

## Cámara y micrófono

- El primer acceso requiere permiso.
- Cámara y micrófono se autorizan por separado.
- El permiso dura solo esa ocasión.
- La siguiente ocasión vuelve a solicitarse.
- Mientras exista acceso activo, SineOS muestra un indicador visible.
- El indicador identifica qué aplicación utiliza cámara, micrófono o ambos.
- Desde el indicador se puede cortar el acceso cuando el backend lo permita de forma segura.

## Ubicación

- El acceso a ubicación requiere permiso.
- El permiso dura solo esa ocasión.
- El usuario puede elegir ubicación aproximada o precisa cuando el backend lo permita.

## Captura y compartición de pantalla

- Las capturas iniciadas manualmente por el usuario no requieren permiso adicional.
- Una aplicación que solicite captura o compartición de pantalla debe pasar por un permiso sensible cuando el stack lo permita.
- El usuario puede elegir ventana o monitor cuando la tecnología subyacente ofrezca esa granularidad.

## Contactos, calendario, archivos y portapapeles

SineOS respeta el modelo de permisos de cada aplicación.

Cuando una aplicación exponga varios permisos relacionados, pueden presentarse en una sola ventana con casillas independientes y un botón **Aceptar**.

SineOS no inventa una capa de permisos incompatible con aplicaciones que no soporten esa granularidad.

## Notificaciones

Si una aplicación ya gestiona su propio permiso de notificaciones, SineOS no duplica la pregunta.

SineOS centraliza después el control desde Configuración.

# Privilegios administrativos

## Polkit

Cuando una aplicación requiera una acción administrativa:
- SineOS muestra qué aplicación pide permiso;
- explica para qué acción;
- ofrece **Ver detalles técnicos**;
- la aplicación no recibe root general;
- la autorización se limita a la aplicación y acción autorizada.

## Autorización temporal

- Puede mantenerse durante la sesión para esa misma aplicación y acción.
- Otra aplicación requiere autorización separada.
- Una acción administrativa diferente requiere nueva autorización.
- La autorización expira al cerrar sesión, reiniciar o apagar.
- La expiración ocurre en silencio.
- Mientras exista una autorización temporal activa, SineOS muestra un indicador discreto con aplicación, acción y opción de revocar.

# Segundo plano e inicio automático

Para evitar fatiga de permisos:
- SineOS no pregunta por defecto cada vez que una app se agrega al inicio automático;
- tampoco pregunta por cada tarea programada o servicio residente;
- los registra y expone en Configuración;
- el usuario puede deshabilitarlos manualmente;
- si el comportamiento cambia de forma claramente sospechosa o anómala, SineOS puede avisar.

Ruta conceptual:
`Configuración de SineOS → Aplicaciones → Inicio automático / Segundo plano / Servicios`

# Recursos en segundo plano

SineOS puede observar consumo sostenido de procesos y servicios en segundo plano sin convertirlo en una política de cierre automático.

- Si una aplicación o servicio mantiene CPU o RAM anormalmente altos durante varios minutos, avisar.
- Mostrar aplicación/proceso y detalles suficientes para identificar el consumo.
- Ofrecer cerrar/detener cuando sea seguro, pero nunca cerrar automáticamente.
- El consumo breve o una aplicación activa en primer plano no debe disparar avisos.
- El drenaje anormal de batería se evalúa únicamente cuando el equipo está usando batería y el comportamiento es sostenido.
- Ante drenaje anormal, mostrar detalles y permitir al usuario decidir si cierra el proceso.
- No usar esta función como excusa para añadir un daemon pesado o muestreo de alta frecuencia.

# Acceso remoto

AnyDesk, RustDesk, TeamViewer y herramientas equivalentes se tratan como **Acceso remoto**, no como simple captura de pantalla.

SineOS no duplica los permisos internos de estas aplicaciones.

## Indicador

Mientras exista una sesión remota:
- mostrar indicador visible;
- indicar qué aplicación está activa;
- indicar si la sesión es entrante o saliente;
- el indicador es informativo y no abre la aplicación.

## Notificaciones

- notificación informativa al iniciar una sesión remota;
- notificación informativa al terminar;
- una desconexión inesperada también se registra.

## Bitácora

Ruta interna:

`~/.local/state/sineos-desktop/logs/remote-access/remote-access.log`

Bitácora incremental e indefinida. Si el usuario la elimina manualmente o usa **Limpiar registros**, el historial desaparece y la siguiente sesión remota crea un archivo nuevo.

Registrar por sesión:
- aplicación;
- dirección: entrante o saliente;
- ID remoto;
- IP remota cuando la aplicación la exponga;
- fecha;
- hora de inicio;
- hora de cierre;
- cierre normal o desconexión inesperada.

No guardar:
- contraseñas;
- tokens;
- contenido de la sesión.

La bitácora se consulta desde:

`Configuración de SineOS → Privacidad → Acceso remoto`

Debe existir el botón **Limpiar registros**.

Al usarlo:
- mostrar confirmación simple;
- no pedir contraseña adicional;
- borrar toda la bitácora;
- la siguiente sesión crea una bitácora nueva.

# Carpetas protegidas — posterior a 1.0

Las Carpetas protegidas SineOS quedan fuera de SDE 1.0 y se consideran para SDE 1.1 o módulo posterior.

Decisiones ya congeladas para su futura implementación:
- cada carpeta tiene contraseña propia;
- no usa la contraseña normal de la sesión;
- visible en Thunar con icono de candado;
- desbloqueo mientras se use;
- bloqueo automático tras 15 minutos sin actividad y sin archivos abiertos;
- bloqueo inmediato al bloquear sesión, cerrar sesión, hibernar o apagar;
- opción **Bloquear ahora**;
- root puede actuar como recuperación administrativa;
- quitar o cambiar contraseña mediante root requiere autenticación administrativa y advertencia;
- no pretende proteger frente a un administrador root con control del sistema.

## Regla final

> SineOS debe proteger lo sensible sin convertir el escritorio en una secuencia interminable de autorizaciones.
