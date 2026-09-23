# Política de documentación y privacidad

SineOS debe poder reconstruirse sin publicar información innecesaria de la máquina, la red o la identidad del usuario.

## No publicar

- rutas absolutas del directorio personal;
- nombre de usuario local;
- direcciones, subredes, gateways o DNS concretos de redes privadas;
- direcciones asignadas por VPN o interfaces temporales;
- correos personales;
- claves SSH, fingerprints privados, contraseñas, API keys, tokens, cookies o secrets;
- URLs Push o endpoints que incorporen credenciales;
- UUID, MAC, números de serie u otros identificadores de dispositivos;
- auditorías, volcados o logs sin sanitizar.

## Marcadores públicos

La documentación debe utilizar marcadores semánticos:

```text
${SINEOS_REPO}        raíz local del repositorio
${SINEOS_VAULT}       raíz local del Knowledge Vault
${HOME}               directorio personal
<TRUSTED_LAN_CIDR>     red local autorizada
<HOST_BIND>            interfaz de escucha
<SERVICE_PORT>         puerto lógico de un servicio
localhost              acceso exclusivamente local
```

Los valores reales pertenecen a la configuración local, no a Git.

## Archivos de ejemplo

Los archivos `.example` pueden documentar nombres de variables, pero sus valores deben ser ficticios, genéricos o marcadores. Los archivos operativos con secretos permanecen ignorados por Git.

## Reportes y logs

Los diagnósticos pueden revelar información sensible aunque no contengan contraseñas. Permanecen locales por defecto y deben sanitizarse antes de compartirse o versionarse.

## Historial Git

Eliminar un dato en un commit posterior no lo elimina del historial. Si se publica accidentalmente un secreto, se debe evaluar la limpieza del historial y la rotación del dato afectado.
