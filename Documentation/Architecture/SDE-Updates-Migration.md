# SDE — Actualizaciones y migración desde XFCE

**Fecha de decisión:** 07-10-2026  
**Estado:** planeación congelada / obligatorio para SDE 1.0  
**Issue maestro:** https://github.com/ArgenisPadill/SineOS/issues/1

# Actualizaciones

## Comprobación

Cada vez que la computadora se enciende y el usuario inicia sesión:
- ejecutar `apt update` silenciosamente en segundo plano;
- si no hay Internet, dejar la tarea pendiente;
- ejecutarla automáticamente cuando exista conexión real a Internet;
- un portal cautivo debe resolverse antes de considerar disponible Internet.

Si no existen actualizaciones, no mostrar nada.

## Presentación

Si existen actualizaciones, mostrar:
- qué aplicaciones cambian;
- qué componentes del sistema cambian;
- si hay kernel nuevo;
- impacto esperado;
- necesidad de cerrar sesión o reiniciar.

Agrupar por impacto. Como mínimo:
- Aplicaciones;
- Sistema;
- Puede afectar la sesión;
- Críticas / requieren reinicio;
- Seguridad crítica.

El usuario decide qué grupos instalar y cuáles dejar pendientes.

## Posponer

- El usuario puede elegir **Actualizar ahora** o **Posponer**.
- Si pospone una actualización normal, no volver a insistir inmediatamente en esa sesión.
- Si una actualización normal lleva **más de 15 días pendiente**, recordar cada **3 días**.
- Una actualización de seguridad crítica pendiente se recuerda cada **3 días** desde que se pospone.
- Las actualizaciones críticas se muestran de forma más visible, pero nunca se instalan a la fuerza.

## Cierre de sesión y reinicio

Regla de oro:
- actualización menor que requiere recargar componentes de sesión → cierre de sesión;
- actualización sensible de SDE/XFCE/LightDM/gráficos → cierre de sesión + validación al volver;
- kernel, initramfs, systemd u otros componentes críticos que lo requieran → reinicio.

Antes de cerrar sesión o reiniciar:
- permitir guardar trabajo;
- cerrar aplicaciones de forma normal;
- no matar aplicaciones con trabajo pendiente sin intervención;
- detectar contenedores, máquinas virtuales y servicios relevantes;
- esperar a que el usuario los detenga o suspenda cuando corresponda.

## Fallo de actualización

Si una actualización falla:
- avisar;
- no intentar reparar automáticamente;
- no hacer rollback automático;
- generar reporte técnico;
- pausar nuevas actualizaciones hasta que el usuario repare manualmente el estado de APT/dpkg;
- el usuario decide la reparación.

Si la actualización problemática vuelve a aparecer:
- marcarla como problemática conocida;
- mostrar el reporte anterior;
- el usuario decide manualmente si vuelve a instalarla.

## Punto de restauración

Antes de una actualización importante:
- crear punto de restauración temporal;
- retenerlo **máximo 2 semanas**;
- permitir **Volver al estado anterior** mientras esté vigente;
- tras restaurar, validar el sistema;
- si queda saludable, volver al funcionamiento normal;
- la actualización que causó el problema no se reinstala automáticamente.

## Energía para actualizar

Antes de iniciar:
- si está usando batería y tiene **más de 50 %**, puede actualizar;
- si está usando batería y tiene **50 % o menos**, esperar;
- si está en 50 % o menos, conectar a corriente y esperar a superar 50 % antes de iniciar;
- excepción: si está conectada a corriente pero la batería está degradada y técnicamente no puede alcanzar 50 %, permitir la actualización;
- una vez iniciada la actualización, terminarla aunque se desconecte el cargador o la batería caiga por debajo de 50 %;
- nunca pausar APT/dpkg a mitad de una transacción por una regla de batería.

## Hotspot y datos móviles

Regla general absoluta:
- por hotspot/datos móviles, la descarga total permitida es de **máximo 250 MB**;
- si supera 250 MB, no se descarga ni instala;
- la regla aplica sin importar el tipo, criticidad o riesgo de la actualización;
- se espera Wi-Fi normal o Ethernet.

# Migración desde XFCE actual

## Respaldo pre-SDE

Antes de modificar el escritorio:
- crear respaldo completo del estado actual;
- conservarlo como referencia pre-SDE;
- debe permitir restaurar el entorno anterior.

Debe incluir al menos:
- configuración XFCE;
- panel;
- atajos;
- wallpaper;
- temas;
- iconos;
- cursor;
- Picom;
- LightDM;
- autostart;
- TLP;
- configuración de pantallas;
- estado relevante de SDE/migración.

## Atajos

- SDE instala su mapa de atajos desde cero.
- Los atajos anteriores quedan en el respaldo.
- Se conservan automáticamente teclas de hardware y multimedia que no entren en conflicto.

## Panel y dock

- Reemplazar completamente el panel actual por la estructura SDE.
- El panel anterior queda en el respaldo pre-SDE.
- Aplicar panel superior + dock desde plantilla limpia y controlada.

## Wallpaper y protector

- Reemplazar wallpaper por uno oficial SineOS.
- Generar fondo adecuado con marca de agua SineOS discreta.
- Protector/bloqueo visual también usa identidad SineOS.
- El usuario puede cambiar wallpaper y protector cuando quiera.
- El wallpaper anterior queda respaldado.

## Escritorio

- Escritorio limpio por defecto.
- **Papelera** visible.
- USB/discos externos no aparecen como iconos; solo barra superior y Thunar.
- El usuario puede personalizar posteriormente los elementos visibles.

## Tema, iconos y cursor

- Reemplazar por los oficiales SineOS.
- Conservar los anteriores en respaldo.

## Picom

- Reemplazar configuración actual por una configuración SDE limpia, versionada y certificada.
- Conservar la anterior en respaldo.
- Si falla, usar compositor XFWM o rollback.

## LightDM

- Mantener LightDM.
- Reemplazar configuración visual/greeter por la experiencia SineOS.
- Conservar configuración anterior en respaldo.

## TLP

- No sobrescribir a ciegas.
- Respaldar configuración actual.
- Aplicar una política SineOS nueva, limpia y versionada.
- Ajustar parámetros dependientes de hardware solo después de validación.

## Redes y VPN

- Conservar conexiones existentes de NetworkManager.
- Conservar redes Wi-Fi guardadas.
- Conservar VPN existentes.
- SDE agrega comportamiento y UX, no obliga a recrear conexiones funcionales.

## Aplicaciones y asociaciones

- Conservar aplicaciones instaladas.
- Respetar navegador predeterminado actual.
- Respetar PDF, imágenes, video, audio y editor de texto actuales.
- Solo intervenir si una asociación está rota, apunta a una aplicación inexistente o es claramente inválida.

## Inicio automático

- Conservar programas actuales.
- Desactivar únicamente componentes que entren en conflicto directo o dupliquen funciones SDE.
- Respaldar lo desactivado.

## Pantallas

- Conservar configuración anterior en respaldo.
- SDE inicia detección limpia de salidas.
- Los nuevos perfiles solo se guardan después de validarse.

## Bluetooth

- Conservar emparejamientos existentes.

## Impresoras y escáneres

- Conservar los que funcionen correctamente.
- Si existe configuración rota, driver ausente o dispositivo no válido, proponer reconfiguración guiada.

## Regla final

> La migración a SDE reemplaza únicamente lo que SDE debe poseer y conserva, respalda o respeta todo lo demás.
