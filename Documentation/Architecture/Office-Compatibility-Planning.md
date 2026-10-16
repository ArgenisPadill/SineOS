# SineOS — Compatibilidad de documentos Microsoft Office (plan de evaluación)

**Registro:** 2026-10-16  
**Estado:** PENDIENTE / INVESTIGACIÓN DOCUMENTAL / NO IMPLEMENTADO / SIN AUTORIZACIÓN DE INSTALACIÓN  
**Seguimiento:** [Issue #7 — Compatibilidad Word/Excel](https://github.com/ArgenisPadill/SineOS/issues/7)  
**Dependencias de gobernanza:** [Roadmap](../Operations/Project-Roadmap.md), [SLDE módulo 11](SLDE-Planning.md), [Política de evolución](Technology-Evolution-Policy.md) y [Seguridad](../Security/Security-Baseline.md)

## 1. Resumen ejecutivo

Existe una **necesidad funcional concreta de docencia**: revisar, completar y entregar plantillas universitarias de Word/Excel sin perder composición, fórmulas ni impresión. No se trata de reemplazar la suite ofimática estándar de SineOS ni de convertir Microsoft Office en dependencia del sistema.

Experiencia reportada, todavía **sin reproducir ni certificar**:
- **LibreOffice:** determinados archivos presentan solapamiento de elementos y cambios de disposición.
- **ONLYOFFICE Desktop:** abre algunos de los archivos, pero se vuelve lento y llega a congelar el equipo.
- **FreeOffice, Google Workspace y Microsoft 365 web:** no consiguen abrir determinados archivos del caso real.

La estrategia inicial preferida **para estudiar, no aprobada para instalar**, es:
1. Caracterizar los documentos y diagnosticar rendimiento/compatibilidad de las soluciones ya presentes.
2. Comparar una **VM Windows con Microsoft Office original** como referencia de fidelidad, preferiblemente mediante **QEMU/KVM + libvirt** si el inventario actual lo permite.
3. **Solo si el escritorio completo funciona y aporta valor**, ensayar integración opcional de Word/Excel por **WinApps + FreeRDP**.
4. Reconsiderar RDP a un Windows existente, WinBoat, Wine/Bottles/CrossOver o no integración en función de pruebas, licencia, costo, privacidad y consumo.

No afirmar que Microsoft Office nativo reproduce todo de forma perfecta: los archivos pueden depender de fuentes, complementos, vínculos externos, macros, versiones de Office o configuraciones de impresora.

## 2. Relación con SineOS y precedencia

Plataforma de referencia **documentada** en el README (no verificada físicamente en esta investigación): Gateway GWTN141-10, Intel i5-1135G7 (4C/8T), **16 GB LPDDR4**, Intel Iris Xe, SSD SATA 512 GB, Debian 13 Trixie, kernel 6.12, XFCE 4.20 / X11, Btrfs y Podman rootless. El historial menciona QEMU/KVM usado para una recuperación NTFS; **eso no prueba que esté instalado o disponible actualmente**.

- **Componente futuro candidato:** SLDE **11 — Ofimática**, con dependencia transversal de virtualización **08** si se justifica. No alterar el inventario aprobado de 16 módulos.
- **SDE 1.0:** experiencia de escritorio congelada, **no** un lugar donde introducir por inferencia una nueva pila Office ni modificar sus contratos.
- **SineOS Core:** no incorporar Office, Wine, RDP o una VM como requisito de arranque, sistema de mantenimiento, backups o auditoría.
- **Prioridad inalterada:** Seguridad → SDE 1.0 → Oracle/n8n/Minecraft → reproducibilidad → SLDE. Este estudio no crea una fase intermedia. Cualquier piloto anticipado es una **excepción explícita por necesidad operativa**, a autorizar y documentar por separado; nunca automática.
- **Deuda técnica:** la necesidad funcional no es por sí misma una TD de SineOS existente. Mantener su seguimiento mediante issue #7, sin tocar la numeración TD.

## 3. Hipótesis que requieren pruebas

**Fidelidad:** sustitución de tipografías o métricas; diferencias OOXML y de paginación; cuadros de texto/posicionamiento; tablas complejas; imágenes/objetos OLE; controles, comentarios, gráficos, macros VBA; vínculos/estilos y plantillas especiales (DOCX/DOTX/DOCM, XLSX/XLTX/XLSM, etc.). Ninguna causa se asume probada.

**Congelamientos ONLYOFFICE:** presión de RAM/swap, agotamiento de memoria (OOM), aceleración/renderizado Intel, tamaño o estructura interna del documento, versión y regresión de la aplicación, servicios concurrentes, disco y errores observables en logs. No atribuir a Wayland, pues la configuración de referencia es X11.

**Reproducción segura:** obtener copias de archivos anonimizados y una salida PDF generada con Microsoft Office del mismo archivo como comparador. Nunca subir a GitHub documentos académicos con nombres/calificaciones de estudiantes, contratos, tokens o rutas privadas.

## 4. Opciones candidatas y compensaciones (estimación previa, no benchmark)

| Alternativa | Ventaja posible | Riesgo / limitación | Estado |
|---|---|---|---|
| Diagnóstico + fuentes y ajustes LibreOffice/ONLYOFFICE | Sin Windows adicional; costo bajo | No garantiza OOXML idéntico ni corrige todos los archivos | Primera evaluación |
| QEMU/KVM + libvirt + Windows/Office legítimos | Motor original de Office y VM controlable | RAM/SSD, mantenimiento/licencias de Windows, integración manual | Candidato de referencia |
| VM anterior + WinApps / FreeRDP | Word y Excel como ventanas integradas en XFCE/X11 | RDP, secretos, redirección de recursos, compatibilidad de edición de Windows y scripts upstream | Solo después de VM validada |
| WinBoat (Windows VM mediante Podman/Docker y UI Electron) | Experiencia integrada y arranque guiado | Beta, requisitos/privilegios, sobrecarga, separación de datos y conflictos potenciales | Alternativa por estudiar |
| Wine / Bottles / CrossOver | Potencialmente menos recursos que VM | Compatibilidad muy variable según versión/instalador de Office; VBA/servicios/actualizaciones inciertos | No presumir éxito |
| RDP a equipo Windows ya existente | Menor carga local | Depende de red/equipo remoto, acceso y políticas institucionales | Alternativa condicionada |
| No integrar; usar Office en otro equipo | Cero nuevos componentes en host | Flujo menos cómodo | Opción válida |

La VM Windows con Office instalado **no elimina** la obligación de tener licencias adecuadas. Comprobar soporte de **host RDP/RemoteApp** en la edición Windows seleccionada (por ejemplo, Windows Pro), Microsoft 365/Office instalado y restricciones de uso. **WinApps no es un emulador de Office; muestra una aplicación que realmente se ejecuta en Windows.** WinApps soporta backends libvirt y Podman, pero su documentación propone por defecto redirección de /home hacia Windows; eso debe bloquearse o restringirse y verificarse **antes de aceptar una instalación**.

Recursos **solo orientativos para prueba futura**: 2 vCPU y 4–6 GiB RAM asignados a la VM; su viabilidad se decide con mediciones y memoria disponible real. El espacio SSD y los recursos de Podman/Ollama/otras aplicaciones pueden hacer inviable mantenerla encendida mientras se trabaja.

## 5. Plan de pruebas sin modificar el sistema

### 5.1 Inventario de solo lectura (por ejecutar en el host, no certificado)

Los siguientes comandos **no instalan ni cambian configuración**; algunos pueden fallar si el programa no existe. No compartir públicamente la salida íntegra de journald o información sensible.

~~~bash
cat /etc/os-release
uname -r
echo "Sesión: $XDG_SESSION_TYPE"
free -h
swapon --show
df -h "$HOME"
command -v virsh || true
command -v virt-manager || true
command -v qemu-system-x86_64 || true
command -v xfreerdp3 || true
ls -l /dev/kvm 2>/dev/null || true
virsh -c qemu:///system list --all 2>/dev/null || true
~~~

En el futuro, revisar impacto de servicios/paquetes **antes** de ejecutar instalaciones: verificar paquetes con dpkg/apt, dependencias, servicios, módulos KVM, privilegios libvirt, redes NAT, permisos de imágenes, espacio libre y cambios sobre nftables; comprobar que Btrfs/Restic y la recuperación siguen funcionando. No aplicar de forma ciega instrucciones de Internet ni comandos de descarga y ejecución simultáneas.

### 5.2 Diagnóstico reproducible de documentos

- Registrar tipo de archivo real, tamaño, número de páginas/hojas, medios incrustados, macros, fuentes declaradas, características particulares y versión de suite.
- Abrir **una copia de trabajo** con LibreOffice, ONLYOFFICE y Office original: comparar captura/PDF, salto de página, superposiciones, contenido, fórmulas y edición/guardado posterior.
- En ONLYOFFICE registrar carga RAM/CPU, swap, I/O, proceso y errores; revisar **localmente** logs del usuario, journal, mensajes OOM y aceleración GPU. No desactivar medidas de seguridad para hacer que abra.
- Formular diagnóstico con causa, evidencia, versión y corrección reversible, sin editar originales.

### 5.3 Piloto hipotético de VM (requiere aprobación separada)

1. Verificar gate/permiso de implementación, baseline, licencias, reserva de disco/RAM y disponibilidad KVM real. Revisar fuente y versiones de paquetes en repos oficiales de Debian.
2. Comprobar backup Restic **y restauración de prueba**, además de un mecanismo de checkpoint/snapshot adecuado para la imagen VM; no asumir que un snapshot local sustituye un backup externo.
3. Crear una VM **bajo demanda**, red NAT/aislada, con disco dinámico y volumen de datos dedicado; aplicar actualizaciones del invitado y deshabilitar exposición RDP pública.
4. Instalar Windows/Office **desde fuentes oficiales y con licencias válidas**; probar documentos sin WinApps, incluyendo impresión PDF y macros solo cuando sean indispensables y autorizadas.
5. Si funciona, revisar un **commit/tag concreto** de WinApps, scripts y dependencias antes de ejecutarlos; probar FreeRDP con credenciales protegidas, redirección mínima de carpetas y portapapeles controlado. Si no es posible impedir acceso de Windows a todo /home o al Vault, no aprobar integración.
6. Medir inicio, apertura, edición, exportación, consumo, impacto en batería y concurrencia con SineOS; realizar pruebas de cierre, recuperación, actualización y desinstalación.

No se proporciona un instalador ejecutable antes de conocer versiones efectivas y obtener autorización; las órdenes operativas requerirán runbook separado con dry-run, límites y rollback.

## 6. Seguridad, privacidad y recuperación

- **Aislamiento:** privilegios mínimos; no añadir usuario a grupos privilegiados o exponer /dev/kvm por defecto sin auditoría. Revisar si conviene sesión de libvirt frente a instancia de sistema.
- **Red:** sólo conexiones necesarias VM↔host, política nftables vigente, VPN/DNSCrypt, sin abrir RDP 3389 a LAN/WAN; evitar reglas NAT/bridge nuevas sin pruebas de firewall. Comprobar redirecciones de RDP, discos, impresoras y clipboard.
- **Datos:** carpeta de intercambio dedicada de permisos mínimos y archivos desidentificados; ningún acceso por defecto a /home completo, Vault, claves SSH, credenciales, DB, carpetas de respaldo o datos institucionales.
- **Windows invitado:** parches, antivirus/Defender, cuentas separadas, credenciales no almacenadas en Git ni en scripts, revisión de telemetría y licenciamiento. No habilitar macros de origen desconocido.
- **Recuperación:** manifest de versiones, imágenes VM fuera de Git, backup consistente, restore probado, snapshots si corresponden, procedimiento de parada y eliminación de servicios/VM/paquetes **sin borrar datos por defecto**.
- **Actualizaciones:** nunca sustituir versiones sin pruebas; comparar logs saneados, rendimiento y fidelidad con baseline para detectar regresiones.
- **No mezclar** Office Windows con contenedores existentes, bases de datos, IA ni infraestructura central.

## 7. Evidencia y criterios de decisión

Para elegir solución, documentar: cinco archivos representativos anonimizados como mínimo si se dispone de ellos (no almacenar los reales en Git), representación PDF de referencia, incidencias visuales y funcionales, consumo pico RAM/CPU/swap, uso de disco, tiempos de carga, licencias, mantenimiento del proyecto, permisos/red, pruebas de backup/restore, desinstalación y efecto sobre otros servicios.

**Aceptación:** los documentos prioritarios conservan el diseño relevante para la universidad, se editan/guardan/imprimen sin regresiones inaceptables, no hay congelamientos bajo la carga habitual medida, no se exponen datos o credenciales, y la función puede eliminarse sin dañar Debian/SineOS. Si las pruebas fallan: **diferir o descartar** es un resultado correcto.

**Puerta de salida documental:** ADR con resultado adoptar / adaptar / diferir / descartar. Un prototipo no equivale a funcionalidad certificada; la autorización del registro no autoriza pruebas con privilegios ni despliegue.

## 8. Referencias externas para validar antes del piloto

- [WinApps — README](https://github.com/winapps-org/winapps): integración mediante Windows en Podman o libvirt y FreeRDP; revisar rama, versiones y documentación actuales al probar.
- [WinApps — backend libvirt](https://github.com/winapps-org/winapps/blob/main/docs/libvirt.md): integración con VM existente; **no** ejecutar scripts remotos directamente.
- [WinBoat](https://github.com/winboat-org/winboat): alternativa en desarrollo/beta basada en VM contenida; revisar requisitos y permisos.
- [Debian Wiki — KVM](https://wiki.debian.org/KVM) y [QEMU](https://wiki.debian.org/QEMU): explicación de virtualización y gestión de instancias.

**Revisión de estado:** 2026-10-16. Las opciones upstream pueden cambiar; ningún enlace externo constituye evidencia de compatibilidad certificada con la laptop ni una aprobación de instalación.
