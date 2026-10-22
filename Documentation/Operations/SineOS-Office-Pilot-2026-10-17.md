# SineOS Office — corte operativo del piloto (17-10-2026)

> **AVISO DE ESTADO VIGENTE (21-10-2026):** Este documento conserva únicamente el estado **histórico del 17-10-2026**; algunas afirmaciones (por ejemplo, ausencia de copia restaurable o la madurez de RemoteApp) han quedado superadas. La decisión actual es **[SineOS Office: PILOTO LOCAL OPERATIVO CONGELADO / NO CERTIFICADO](SineOS-Office-Pilot-Frozen-2026-10-21.md)**, con escritorio RDP único como vía principal. No constituye integración completa de SineOS, SDE o SLDE.


**Estado:** PILOTO LOCAL FUNCIONAL / NO CERTIFICADO / PENDIENTE DE ENDURECIMIENTO.  
**Origen de la evidencia:** pruebas interactivas del usuario en su Debian 13 y Windows 11 invitado, compartidas el 17-10-2026; no se obtuvo acceso directo al host desde esta revisión de GitHub.  
**Seguimiento:** [issue #7 (piloto)](https://github.com/ArgenisPadill/SineOS/issues/7), [issue #8 (sesiones RAIL)](https://github.com/ArgenisPadill/SineOS/issues/8), [issue #9 (seguridad/backup)](https://github.com/ArgenisPadill/SineOS/issues/9), [plan original](../Architecture/Office-Compatibility-Planning.md), [roadmap](Project-Roadmap.md).  
**Alcance de este commit:** memoria documental del estado observado; **sin** sincronizar archivos locales de configuración, ejecutar comandos en la laptop ni certificar recuperación.

> **Congelación de referencia.** Este documento es el punto de reanudación del piloto de SineOS Office. No describe una funcionalidad instalada por el repositorio principal ni una publicación de SLDE/SDE. Todo lo señalado como `PENDIENTE` requiere revisión y pruebas en el host antes de un cambio. La prioridad global Seguridad → SDE 1.0 → Oracle/n8n/Minecraft → reproducibilidad → SLDE no cambia; este piloto respondió a una necesidad académica concreta por una ejecución excepcional del usuario.

## 1. Resultado efectivo de la sesión

- Windows 11 Pro 25H2 (compilación observada 26200.8037), virtualizado mediante **Dockur Windows + QEMU/KVM** dentro de **Podman rootless**; sin instalar Docker ni libvirt para este piloto.
- Microsoft **Office LTSC Professional Plus 2024**, 64 bits, instalado desde el Office Deployment Tool oficial. Word, Excel y PowerPoint abren individualmente y el usuario mostró la interfaz de Office con estado «Producto activado». **La titularidad y condiciones de las licencias, incluida la activación de Windows Pro, NO se auditaron ni certificaron**; no almacenar en Git claves, técnicas de activación ni pruebas con identificadores.
- **FreeRDP X11 3.15.0** permitía escritorio completo, pero se congelaba al abrir RemoteApp. Actualización desde **Debian 13 `trixie-backports` a FreeRDP 3.32.1** (`freerdp3-x11` transicional y `freerdp-x11`) permitió abrir Bloc de notas y las tres aplicaciones de Office mediante RAIL. Simulación APT previa: 4 paquetes actualizados, 2 nuevos, 0 eliminados; resultado instalado `3.32.1+dfsg-1~bpo13+1`.
- Desde **XFCE/X11** funcionan lanzadores de Word, Excel y PowerPoint **sin terminal visible** y con autenticación RDP automática. También funciona el lanzador del **escritorio completo**. No debe asumirse que se pueden abrir múltiples sesiones RDP simultáneas sin conflictos.
- Se validaron lectura y escritura entre Windows y Debian a través de una **carpeta compartida dedicada** vía Samba, accesible desde Windows como `\\host.lan\Data`; Word abrió, modificó y guardó un DOCX y Debian verificó el contenido añadido. Se probó apertura de DOCX con doble clic en Thunar. Se reportó que XLSX/PPTX abren, aunque con lentitud y notificaciones tras desconexiones; aún no hay aceptación de cierre limpio ni benchmark.
- **No existe un respaldo recuperable/snapshot del Windows invitado validado para este piloto**: el usuario optó por posponer la copia en esa sesión. Este riesgo permanece abierto y prioritario antes de ensayos destructivos.

## 2. Límites y arquitectura local observada

| Elemento | Valor observado o documentado en sesión | Alcance |
|---|---|---|
| Host | Debian 13 Trixie, XFCE/X11, Btrfs | Hardware compartido; no benchmark |
| Carpeta base del piloto | `${HOME}/Workspace/SineOS-Office/` | Independiente del repositorio SineOS principal |
| Código upstream clonado | `./winapps/` (winapps-org/winapps) | No asumir WinApps `setup.sh` instalado |
| Compose del piloto | `./compose.yaml` y `./.env` | Archivos locales, **no versionados en este repositorio** |
| Contenedor | `sineos-office-windows` | Podman rootless; `restart: "no"` |
| VM | Windows 11 Pro; 4 GiB RAM; 4 vCPU; disco 96 GiB configurado | No se midió carga real ni crecimiento del disco |
| Persistencia | `./storage:/storage` | Imagen/disco, **no copiar a Git** |
| Intercambio | `./shared:/shared` | Se expone a Windows por `\\host.lan\Data` |
| OEM scripts | `./winapps/oem:/oem:ro` | El instalador OEM fue utilizado durante el piloto |
| Red del invitado | Podman rootless con modo de usuario (`passt`) | No se validó integralmente con VPN/firewall |
| Puertos hacia el host | `127.0.0.1:8006/tcp`, `127.0.0.1:3389/tcp` y `127.0.0.1:3389/udp` | Evita publicación deliberada hacia LAN/WAN; auditar exposición efectiva |
| Credenciales | `SINEOS_OFFICE_PASSWORD` en `./.env` (`chmod 600` observado) | Nunca publicar valores ni colocarlos en línea de comandos |
| Lector de contraseña | `${HOME}/.local/bin/sineos-office-askpass` | Lee clave localmente; no enviar secreto a logs |
| Escritorio Windows | `${HOME}/.local/bin/sineos-office` | Lanzador XFCE `sineos-office.desktop` |
| RemoteApps individuales | `${HOME}/.local/bin/sineos-office-app` | `sineos-word.desktop`, `sineos-excel.desktop`, `sineos-powerpoint.desktop` |
| Apertura de archivo | `${HOME}/.local/bin/sineos-office-file` | Asociaciones `sineos-file-*.desktop`, restringidas a `shared` |
| Logs locales | `${HOME}/.local/state/sineos-office/` | Privados, nunca subir logs crudos |
| Asociaciones MIME | `${HOME}/.config/mimeapps.list` | DOCX comprobado; XLSX/PPTX instaladas, con validación incompleta |

**Detalles de implementación:** en scripts se usa `xfreerdp3 /args-from:stdin` con credenciales emitidas por lector local y `/cert:tofu`. La aplicación remota se inicia con `/app:program:C:/Program Files/Microsoft Office/root/Office16/<EJECUTABLE>`; para archivos se usa `cmd:"\\host.lan\Data\<RUTA_RELATIVA>"`. Ejecutables probados: `WINWORD.EXE`, `EXCEL.EXE`, `POWERPNT.EXE`.

**Precaución sobre `/args-from:stdin`:** evita exponer la contraseña como argumento del proceso, pero la clave existe en memoria y el entorno local del usuario puede acceder al lector y a `.env`. El inicio automático requiere proteger la sesión XFCE. No se publicó ningún contenido de `.env` ni material de licencia.

**Desviación upstream intencionada:** la configuración WinApps genérica utiliza nombre de contenedor `WinApps`, rutas en `~/.config/winapps` y `+home-drive`/redirección de `/home`. El piloto usa nombre y ruta personalizados, **no comparte `/home` entero**, y no debe ejecutar el instalador estándar sin auditar estos supuestos. **La integración actual son scripts locales construidos durante la sesión, no una instalación validada de WinApps `setup.sh`.**

## 3. Pruebas observadas (evidencia, no certificación)

| ID | Prueba | Resultado |
|---|---|---|
| OF-01 | KVM, Podman rootless y Windows invitado | Funcionaron durante el piloto |
| OF-02 | Escritorio RDP en FreeRDP 3.15 y luego 3.32.1 | Funcionó |
| OF-03 | RemoteApp 3.15 / Bloc de notas | Congelamiento reproducido |
| OF-04 | RemoteApp 3.32.1 / Bloc de notas | Abrió; en una prueba aparecieron varias ventanas |
| OF-05 | RemoteApp 3.32.1 / Word | Una ventana; funcionó |
| OF-06 | RemoteApp 3.32.1 / Excel | Funcionó tras cerrar instancia invisible; `EXCEL.EXE /safe` y luego inicio normal funcionaron |
| OF-07 | RemoteApp 3.32.1 / PowerPoint | Funcionó, arranque percibido como más lento |
| OF-08 | Lanzadores XFCE individuales y escritorio completo sin terminal | Usuario confirmó funcionamiento |
| OF-09 | Intercambio bidireccional Samba `Data` | Creación desde Windows y lectura desde Debian correctas |
| OF-10 | Word editó DOCX de `shared`; lectura posterior en Debian | Se verificó contenido editado |
| OF-11 | DOCX abierto mediante doble clic desde Thunar | Usuario confirmó |
| OF-12 | XLSX/PPTX desde Thunar | Abrieron; latencia y aviso de error posterior aún bajo investigación |
| OF-13 | Cerrar Excel con `Alt+Fn+F4` | Ventana Excel desaparece, pero RDP/RAIL pueden quedar activos |
| OF-14 | Inspección con `pgrep` / `xwininfo` | RAIL auxiliar `Program Manager`, `Rdptray`, PowerShell; sesiones residuales |
| OF-15 | Tarea `TimeSync` creada por OEM WinApps | Se encontró `Running` y proceso `TimeSync.ps1`; se detuvo y deshabilitó reversible; proceso oculto dejó de aparecer |
| OF-16 | Tras deshabilitar `TimeSync` | PowerShell residual desapareció, pero RDP y ventanas auxiliares continuaron hasta cierre diferido; **causa exacta no resuelta** |

## 4. Problemas abiertos y riesgos (NO marcar como resueltos)

### Prioridad inmediata del piloto

1. **Gestión de sesiones RAIL:** `xfreerdp3` puede permanecer activo tras cerrar el último documento/aplicación, con ventanas `Program Manager` / `Rdptray` visibles en Alt+Tab. Evitar terminar procesos sin comprobar documentos abiertos. Diferenciar RAIL auxiliar y aplicación real, cierres diferidos y múltiples instancias.
2. **Lanzador de escritorio completo:** el script actual bloquea la apertura si detecta *cualquier* FreeRDP, incluso una RemoteApp residual. Hacer comprobación específica, control concurrente, mensajes gráficos y opción de recuperación segura.
3. **Falsos avisos de error:** `sineos-office-file` muestra `Fallo la apertura` al recibir cualquier código no cero desde FreeRDP, incluso **después** de haber abierto el documento, cuando el servidor produce `ERRINFO_RPC_INITIATED_DISCONNECT [0x00010001]`. Diferenciar establecimiento, sesión en curso, salida normal y pérdida real; **no silenciar errores arbitrariamente**.
4. **Endurecimiento del recurso compartido:** permisos observados `drwxrwsrwx` (2777), propiedad remapeada a ID numéricos por Podman rootless y acceso Samba de invitado dentro del contenedor. Minimizar permisos mediante cambios reversibles y pruebas completas, sin quebrar escritura de Office; no guardar documentos sensibles antes de corregirlo.
5. **Backup y restauración de la VM:** definir copia consistente del almacenamiento persistente `storage`, prueba de restore, cifrado, retención, espacio y recuperación; **NO HAY restore validado**. Respetar backups Restic/Btrfs del sistema, sin afirmar cobertura automática del invitado.
6. **Hora del invitado:** tarea `TimeSync` de WinApps **deshabilitada** el 17-10 por no estar adaptada a la topología (`\\tsclient\home` no compartido); estudiar alternativa que no monte todo `/home`, probar suspensión/hibernación/resume, desfase y recuperación. No eliminar la tarea sin cambio aprobado.

### Aceptación pendiente / diseño posterior

7. **Archivos fuera de `shared`:** actualmente `sineos-office-file` rechaza rutas ajenas a la carpeta. Diseñar apertura desde Descargas/Documentos sin copias divergentes, manejo de colisiones, symlinks, nombres especiales, edición concurrente, guardado atómico y rollback.
8. **Pruebas con archivos reales anonimizados:** plantillas universitarias complejas, macros, fuentes, paginación, impresión/PDF, fidelidad, cierres repetidos, documentos grandes y concurrencia Word+Excel+PowerPoint.
9. **Rendimiento y recursos:** medir inicio en frío/caliente, latencia PowerPoint, memoria/swap/CPU/I/O y autonomía; no tomar la VM de 4 GiB/4 vCPU como certificación de capacidad.
10. **Auditoría de seguridad y licenciamiento:** RDP, `/cert:tofu`/pinning, cifrado del host, compartición, clipboard, Samba, `passt`, nftables, VPN/DNSCrypt, actualizaciones Windows, ediciones/licencias/uso autorizado de VM y Office.
11. **Reproducibilidad:** inventariar contenido exacto y hashes de scripts locales, vincular en `Scripts/README.md` solo **después de auditar y probar**, crear templates sin secretos, procedimiento de instalación/actualización, desinstalación y rollback. No asumir que los scripts documentados aquí ya existen en Git.
12. **Gobernanza:** redactar ADR de adoptar/adaptar/diferir y certificar gates antes de integrar oficialmente en SDE/SLDE. Piloto no modifica ni cierra issues de Seguridad/SDE ni estados TD previos.

## 5. Runbook de recuperación provisional

**Desde Debian, como usuario normal, SIN sudo (salvo procedimientos APT explícitos):**

~~~bash
# Estado del invitado y de las conexiones; solo lectura
podman inspect --format '{{.State.Status}}' sineos-office-windows
pgrep -a -u "$(id -u)" -x xfreerdp3 || true
xwininfo -root -tree 2>/dev/null | grep -i RAIL || true

# Verificar que RDP solo responde en el puerto previsto
nc -z -w 3 127.0.0.1 3389

# Estado de paquete
xfreerdp3 /version
apt-cache policy freerdp3-x11 freerdp-x11

# Revisar logs LOCALES sin copiarlos al repositorio
tail -n 30 "${HOME}/.local/state/sineos-office/files-excel.log"
~~~

- Si el menú del escritorio completo no abre, revisar primero clientes FreeRDP aún activos: el lanzador tiene un bloqueo global por proceso. **Guardar documentos y cerrar aplicaciones** antes de solicitar desconexión. Nunca aplicar `pkill` indiscriminadamente sobre sesiones desconocidas.
- Si un DOCX está dentro de `shared`, los lanzadores de archivo convierten ruta relativa Linux a `\\host.lan\Data\...`. Un archivo fuera de `shared` debe rechazarse **sin moverlo ni copiarlo silenciosamente**.
- Si un proceso se identifica por PID y se confirma que es una sesión residual sin documentos sin guardar, una señal `TERM` al **PID concreto** de FreeRDP puede liberar ventanas RAIL; la salida no cero podría activar actualmente un aviso de error engañoso.
- Para recuperar la tarea de sincronización horaria **solo si se decide y valida la dependencia** en PowerShell administrador: `Enable-ScheduledTask -TaskName "TimeSync"`. Su estado al corte es **Disabled**. No habilitarla ciegamente: el script upstream espera `\\tsclient\home`.
- No borrar `storage`, no ejecutar `podman-compose down -v`, no eliminar volúmenes, no reinstalar Windows/Office ni actualizar componentes sin plan de recuperación.
- La reversión de un lanzador debe limitarse a su archivo local respaldado, dejando intacto el contenedor y su almacenamiento. Se crearon respaldos locales del lanzador general y de `mimeapps.list` durante la sesión, pero su inventario exacto **no fue auditado desde GitHub**.
- Cambiar FreeRDP a 3.32.1 resolvió RemoteApp en esta prueba; **un downgrade no está certificado** y requiere simulación APT y pruebas.

## 6. Para reanudar sin repetir todo mañana

1. Verificar sesión limpia: `pgrep -ax xfreerdp3` y ventanas RAIL; guardar/terminar sesiones previas de manera consciente, sin apagar la VM por defecto.
2. Confirmar estado de `TimeSync` (Disabled) y si quedan ventanas PowerShell al iniciar una nueva RemoteApp.
3. Reproducir **una sola sesión** con un archivo de prueba XLSX dentro de `shared`: abrir → editar → guardar → cerrar aplicación por completo → observar 30–60 s → revisar código de salida/log/ventanas. Separar error de apertura de cierre tardío.
4. Solo después, diseñar y revisar cambios de scripts con backup, lint, pruebas de Word/Excel/PowerPoint y rollback, cuidando autenticación vía `/args-from:stdin`.
5. Antes de trabajar con documentos reales/confidenciales o cambios de VM, priorizar permisos mínimos y **backup recuperable**. Medir capacidad/compatibilidad académica en etapa posterior.

## 7. Alcance de revisión documental

- Se revisaron en GitHub el plan original, roadmap, estándar documental, política de privacidad e índice.
- Se inspeccionó upstream WinApps: `oem/install.bat` crea `TimeSync`; `oem/TimeSync.ps1` usa un bucle y `\\tsclient\home`; `oem/RDPApps.reg` habilita permisos RemoteApp; el backend WinApps oficial usa supuestos distintos del piloto.
- No se leyó ni versionó el `compose.yaml`, los scripts ni los secretos reales de la laptop: **la configuración aquí descrita procede de pruebas de conversación y debe cotejarse con el host para convertirla en código reproducible**.
- No se ejecutaron tests automáticos, auditoría de red ni restore desde GitHub. Mantener **estado piloto**, no «listo para producción».

**Próxima acción de desarrollo:** issue #7, estabilización de sesiones/notificaciones, con prioridad de riesgo para la copia recuperable y permisos compartidos.