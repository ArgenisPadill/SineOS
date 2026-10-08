# SDE — Integración de red, dispositivos y almacenamiento

**Fecha de decisión:** 07-10-2026  
**Estado:** planeación congelada / obligatorio para SDE 1.0  
**Issue maestro:** https://github.com/ArgenisPadill/SineOS/issues/1

## Principio

SineOS debe automatizar la recuperación de conectividad y dispositivos sin ocultar al usuario los fallos ni tomar decisiones sensibles por él.

## Red y reconexión

- Las redes Wi-Fi guardadas se conectan automáticamente.
- Ante una falla de conexión, SineOS realiza hasta **3 intentos automáticos**.
- Si falla el tercer intento, muestra un aviso claro y deja la decisión al usuario.
- SineOS distingue entre **sin red**, **red local sin Internet** y **portal cautivo**.
- No se hardcodean SSID, dominios ni redes concretas.

## Portales cautivos

Cuando SineOS detecta un portal cautivo:
1. reconoce que existe conectividad local pero falta autenticación;
2. abre Firefox para completar el portal;
3. no guarda las credenciales del portal cautivo;
4. espera a que el usuario autentique;
5. confirma acceso real a Internet;
6. reactiva la política normal de DNS cifrado;
7. reactiva la VPN si estaba habilitada.

Si una VPN activa impide completar el portal, SineOS puede pausarla temporalmente y volver a conectarla después de la autenticación.

## Ethernet y Wi-Fi

- Ethernet tiene prioridad sobre Wi-Fi cuando ambas están disponibles.
- Wi-Fi funciona como respaldo.
- Si Ethernet falla, SineOS cambia automáticamente a una red Wi-Fi guardada.
- Cuando Ethernet vuelve, SineOS regresa automáticamente a cable.
- Esta política también aplica si Ethernet proviene de un adaptador USB.

## VPN

- Si una VPN se cae, SineOS intenta reconectarla hasta **3 veces**.
- Si el tercer intento falla, muestra un aviso.
- SineOS no decide automáticamente si el usuario debe continuar sin VPN, reintentar o desconectarse.
- La decisión final queda en manos del usuario.

## Bluetooth

- Dispositivos ya emparejados se conservan durante la migración a SDE.
- Un dispositivo Bluetooth guardado que no conecta recibe hasta **3 intentos automáticos**.
- Si falla, se avisa sin borrar el emparejamiento.
- SineOS no elimina automáticamente un dispositivo Bluetooth por una falla de reconexión.
- Audífonos Bluetooth conectados pasan a ser salida de audio automáticamente.
- Si se desconectan o se quedan sin batería, el audio regresa automáticamente a las bocinas de la laptop.
- El problema recurrente de emparejamientos que dejan de reconectar debe diagnosticarse antes de borrar y volver a vincular.

## USB y almacenamiento extraíble

- USB y discos externos se montan automáticamente.
- Si el montaje falla, se realizan hasta **3 intentos**.
- Si falla el tercer intento, SineOS muestra un aviso.
- Un montaje correcto genera una notificación breve.
- Thunar no se abre automáticamente.
- Los dispositivos montados aparecen en Thunar y en un indicador de la barra superior, no como iconos de escritorio.
- Desde la barra superior se puede desmontar o expulsar un dispositivo sin abrir Thunar.
- Si hay archivos en uso, SineOS impide la expulsión forzada y avisa.
- Tras desmontar correctamente, muestra “Ya puedes retirar el dispositivo” o equivalente.

## Espacio disponible

- Una unidad externa al **90 % de ocupación** genera aviso de poco espacio.
- El disco interno al **90 % de ocupación** genera una advertencia más visible y persistente.
- La falta de espacio del disco interno se considera un riesgo operativo para actualizaciones, logs y funcionamiento general.

## Drivers y firmware

Al conectar hardware nuevo:
1. SineOS identifica el dispositivo;
2. comprueba si ya funciona con el driver genérico del kernel;
3. si existe firmware o driver adicional en repositorios oficiales de Debian, informa al usuario;
4. explica qué mejora aporta frente al driver genérico;
5. el usuario decide si instalar;
6. si decide no instalar, se conserva el driver genérico cuando sea funcional;
7. antes de instalar un driver específico, se conserva estado suficiente para rollback;
8. si la validación falla, SineOS puede volver al driver genérico funcional.

No se descargan ni ejecutan automáticamente drivers, instaladores .run/.sh o paquetes desde sitios no confiables.

## Regla final

> SineOS automatiza reconexión y recuperación básica, pero nunca elimina emparejamientos, instala drivers externos ni fuerza decisiones de red sensibles sin participación del usuario.
