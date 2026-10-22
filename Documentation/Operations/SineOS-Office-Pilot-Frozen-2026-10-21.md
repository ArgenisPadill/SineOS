# SineOS Office — piloto local operativo congelado (21-10-2026)

> **DECISIÓN CONGELADA — PILOTO LOCAL OPERATIVO / NO CERTIFICADO / NO INTEGRACIÓN COMPLETA.**
>
> **Método principal:** un único escritorio Windows 11 mediante FreeRDP desde Debian 13 XFCE/X11.
> **RemoteApp individual (Word/Excel/PowerPoint):** experimental y no aceptado como modalidad estable.
> **Gobernanza:** este piloto NO constituye integración oficial, reproducible o certificada de SineOS Core, SDE ni del módulo 11 de SLDE.

**Fecha del corte:** 21 de octubre de 2026 (México, UTC-6).  
**Seguimiento:** [#7 — piloto y aceptación](https://github.com/ArgenisPadill/SineOS/issues/7) · [#8 — RemoteApp/RAIL](https://github.com/ArgenisPadill/SineOS/issues/8) · [#9 — seguridad y recuperación](https://github.com/ArgenisPadill/SineOS/issues/9).  
**Antecedente histórico:** [corte del 17-10-2026](SineOS-Office-Pilot-2026-10-17.md) (no refleja por sí solo el último estado).  
**Plan y criterios originales:** [compatibilidad de Office](../Architecture/Office-Compatibility-Planning.md).

## Alcance operativo congelado

- Host: Debian 13, XFCE/X11; VM Windows 11 en Dockur/QEMU-KVM mediante Podman rootless; Office LTSC Professional Plus 2024 instalado.
- Acceso diario: **una única conexión al escritorio Windows mediante FreeRDP**, abriendo Word, Excel y PowerPoint desde Inicio, dentro de esa misma sesión.
- Intercambio: carpeta Samba dedicada; los archivos de QA se revisan desde Debian. No permitir acceso por defecto a todo el directorio personal del host.
- No usar los lanzadores RemoteApp individuales como vía principal ni abrir conexiones RDP paralelas para cada aplicación.
- El piloto es una solución **local, opcional y bajo demanda** a una necesidad de compatibilidad documental. No es una función distribuida, empaquetada, automatizada ni certificada de SineOS.

## Evidencia observada y límites

| Área | Estado del corte |
| --- | --- |
| Escritorio Windows en una sola sesión RDP | **OPERATIVO**, validado interactivamente por el usuario |
| Word / DOCX de QA | **PASS** integridad y texto presente |
| Excel / XLSX de QA | **PASS** integridad; A2=123, B2 fórmula `=A2*2` y resultado almacenado 246 |
| PowerPoint / PPTX de QA | **PASS** integridad ZIP/CRC/XML y dos diapositivas con texto |
| Forma gráfica en el PPTX | **PENDIENTE**, no detectada en la comprobación |
| Ejecución de diapositivas F5/Esc | **PENDIENTE** de confirmación específica |
| Portapapeles bidireccional de la sesión final | **PENDIENTE** de confirmación específica |
| Cierre y reapertura controlados de las tres aplicaciones | **PENDIENTE** de confirmación específica |
| RemoteApp individual y concurrencia de aplicaciones | **EXPERIMENTAL / NO APROBADO**; conflictos de sesiones RAIL; véase #8 |
| Dos respaldos locales de VM | **PASS** SHA-256 de siete archivos por copia y revalidación del origen |
| Restauración aislada de VM | **PASS** arranque Windows hasta inicio de sesión y apagado limpio |
| Office ejecutado dentro del clon restaurado | **NO PROBADO**; no declarar restauración funcional integral certificada |
| Políticas de Windows Update | Seis políticas registradas localmente; comprobación post-reinicio **PENDIENTE** |

**Interpretación:** integridad de archivos QA y arranque restaurado no equivalen a pruebas completas de fidelidad académica, impresión, seguridad, licencias, recuperación de Office o certificación del sistema.

## Pendientes sin cerrar

1. Seguridad: permisos mínimos en Samba, secretos, exposición RDP y red, firewall, cifrado, mantenimiento Windows/Defender y licencias; registrar evidencia y aprobaciones en #9.
2. Recuperación: respaldo externo a otro medio físico, cifrado/retención y prueba funcional de Office en clon aislado antes de considerar certificación integral; #9 permanece abierto.
3. Operación y aceptación: F5, portapapeles, forma gráfica, reapertura/cierre, documentos universitarios reales *anonimizados*, rendimiento, fuentes, exportación/impresión y políticas Windows Update post-reinicio; #7 permanece abierto.
4. RemoteApp: sesiones desconectadas, ventanas RAIL, apertura simultánea, notificaciones de error, cierre limpio y regresiones; #8 permanece abierto.
5. Reproducibilidad y empaquetado: scripts de instalación/actualización/rollback auditados, dependencias/versiones, políticas de licencias y puertas de aceptación de SDE/SLDE; **no implementado ni certificado**.

## Regla de congelamiento y reanudación

- **No introducir cambios funcionales automáticos** en la VM, Office, activaciones, FreeRDP, lanzadores, configuración de red o seguridad por el solo hecho de documentar este estado.
- Preservar los dos respaldos existentes; no subir discos de VM, copias, contraseñas, identificadores de licencia, archivos `.env`, documentos académicos ni logs crudos a GitHub.
- Toda mejora posterior debe tramitarse como trabajo separado con alcance, evidencia, revisión de seguridad, respaldo/rollback y pruebas de regresión. No reactivar RemoteApp como modalidad principal sin aceptación específica.
- Mantener inalterado el orden maestro **Seguridad → SDE → Oracle/n8n/Minecraft → reproducibilidad → SLDE** y los gates asociados.
- La etiqueta «piloto local operativo» describe únicamente el flujo probado, **no** autoriza declararlo «estable certificado», «integrado completamente», «listo para producción» ni cerrar #7/#8/#9.

**Fuente de verdad de esta decisión de congelamiento:** este documento, el índice de documentación y las actualizaciones de los issues #7, #8 y #9. La bitácora del 17-10-2026 se conserva como antecedente histórico, no como descripción vigente.
