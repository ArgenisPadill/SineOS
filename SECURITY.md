# Política de seguridad de SineOS

> Estado: procedimiento de reporte público adoptable; no implica que los controles del host estén certificados.

## Reportar vulnerabilidades

**No publiques** vulnerabilidades explotables, contraseñas, llaves, tokens, datos del Vault, documentos académicos, volcados, credenciales ni capturas con información privada en issues, PR o discusiones públicas.

1. Visita la pestaña **Security** de este repositorio y utiliza **Report a vulnerability** si el reporte privado de vulnerabilidades está habilitado.
2. Si la opción privada no está disponible, abre un issue **sin detalles técnicos sensibles** solicitando un canal privado de comunicación al mantenedor. No agregues pruebas de concepto ni archivos secretos.
3. Una vez establecido un canal privado, comparte impacto, pasos de reproducción mínimos, versiones afectadas y propuesta de mitigación **solo por ese canal**.

No se garantiza un SLA de respuesta o pago de recompensas. El proyecto es personal; no se anuncia un programa de bug bounty. El mantenedor decidirá cuándo comunicar una corrección o aviso.

## Alcance

Se aceptan reportes relacionados con código y configuraciones versionadas de SineOS. El entorno instalado del mantenedor, servicios domésticos, Vault, backups y credenciales **no** son un entorno público de pruebas ni están autorizados para pentesting.

No se autorizan pruebas sobre la laptop, IPs, dominios, redes ni servicios reales por el hecho de que el repositorio sea público.

## Seguridad en cambios propuestos

- Mantener Podman rootless, secretos fuera de Git, binds locales y políticas de firewall vigentes.
- Revisar dependencias e imágenes antes de actualizar.
- Para cambios operativos: respaldo, gate de reversión, validación en host y autorización expresa.
- Registrar PASS, FAIL y PENDING con evidencia saneada.
- Evitar publicar configuración exacta de infraestructura, datos de usuarios, rutas privadas y resultados crudos de auditorías.

Véase [Documentación de seguridad](Documentation/Security/README.md), [Gestión de secretos](Documentation/Security/Secrets-Management.md) y [Estándar de ingeniería](Documentation/Architecture/Engineering-Delivery-Standard.md).
