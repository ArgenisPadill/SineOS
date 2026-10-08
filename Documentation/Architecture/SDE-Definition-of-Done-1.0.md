# SDE — Definición de terminado 1.0

**Fecha de decisión:** 07-10-2026  
**Estado:** congelado / obligatorio para declarar SDE 1.0 estable  
**Issue maestro:** https://github.com/ArgenisPadill/SineOS/issues/1

## Principio

SDE 1.0 no se considera terminado porque “se vea bien” ni porque instale correctamente.

Debe demostrar que:
- puede instalarse;
- puede funcionar;
- puede fallar de forma segura;
- puede recuperarse;
- puede desinstalarse;
- puede reproducirse;
- mantiene bajo consumo;
- conserva la capacidad de diagnóstico.

# C0 — Arranque y recuperación

Debe pasar:
- arranque gráfico SineOS;
- login funcional;
- bloqueo funcional;
- cierre de sesión;
- reinicio;
- apagado;
- GRUB accesible;
- diagnóstico disponible;
- fallback de compositor;
- fallback de panel;
- rollback pre-SDE;
- Modo seguro;
- recuperación local;
- recuperación desde release/tag/commit certificado;
- recuperación offline.

# C1 — Escritorio y UX

Debe pasar:
- panel superior;
- dock;
- tema;
- iconos;
- cursor;
- wallpaper;
- OSD;
- notificaciones;
- Focus;
- Reduced Motion;
- Snap Preview;
- configuración persistente;
- sin clics muertos;
- sin movimientos inesperados;
- latencia dentro de objetivos;
- estados accesibles sin depender solo de color.

# C2 — Sesión y energía

Debe pasar:
- LightDM + greeter SineOS;
- usuario preseleccionado;
- contraseña obligatoria;
- Super+L;
- xfce4-screensaver;
- hibernación al cerrar tapa;
- reanudación con bloqueo;
- Resume Validation;
- AC prioriza rendimiento;
- batería prioriza eficiencia;
- estados de batería baja/crítica;
- salud de batería;
- política térmica;
- recuperación de perfil energético.

# C3 — Pantallas

Debe pasar:
- pantalla interna;
- HDMI/DisplayPort disponible en hardware físico;
- hot-plug;
- duplicar;
- extender;
- solo pantalla interna;
- transacción Mantener/Revertir;
- rollback automático por timeout;
- recuperación de ventanas fuera de pantalla;
- resoluciones heredadas;
- 1080p/1200p/1440p/4K cuando el hardware exista;
- DPI razonable;
- Safe Areas.

Pantalla inalámbrica no bloquea 1.0 si el backend no está certificado.

# C4 — Red y dispositivos

Debe pasar:
- Wi-Fi guardado;
- 3 reintentos;
- portal cautivo;
- reconexión VPN;
- prioridad Ethernet;
- failover a Wi-Fi;
- Bluetooth;
- reconexión de dispositivos;
- cambio de audio Bluetooth;
- USB;
- montaje;
- expulsión segura;
- poco espacio;
- firmware/driver genérico y específico;
- rollback de driver.

# C5 — Privacidad y permisos

Debe pasar:
- cámara;
- micrófono;
- ubicación;
- indicadores de uso;
- compartición de pantalla cuando el stack lo permita;
- autorizaciones Polkit acotadas;
- revocación por sesión;
- acceso remoto visible;
- bitácora incremental;
- Configuración → Privacidad → Acceso remoto;
- limpieza manual de registros.

# C6 — Impresión y escaneo

Debe pasar:
- instalación guiada de impresora;
- detección de red;
- hoja de prueba SineOS;
- consumibles;
- bloqueo al 1 %;
- reconexión;
- cola;
- escáner;
- una/múltiples páginas;
- OCR;
- PDF buscable;
- revisión antes de guardar;
- reconexión;
- limpieza por inactividad.

# C7 — Actualizaciones

Debe pasar:
- apt update al iniciar sesión;
- reintento cuando vuelva Internet;
- clasificación por impacto;
- seguridad crítica;
- posponer;
- recordatorio cada 3 días según reglas;
- cierre de sesión o reinicio según impacto;
- punto de restauración de 2 semanas;
- rollback manual;
- reporte de fallo;
- bloqueo temporal de nuevas actualizaciones si APT/dpkg queda inconsistente;
- regla de batería;
- límite absoluto de 250 MB en hotspot/datos móviles.

# C8 — Salud de hardware

Debe pasar:
- SMART;
- alerta de disco crítico;
- apertura de herramienta de respaldo;
- modo de protección de almacenamiento;
- RAM;
- CPU;
- GPU;
- temperatura;
- ventiladores;
- sistema de archivos;
- respaldo prioritario;
- reportes;
- restauración desde backup;
- validación completa posterior;
- Modo seguro si persisten errores críticos.

# C9 — Migración

Debe pasar:
- respaldo pre-SDE completo;
- restauración del XFCE previo;
- atajos SDE desde cero;
- panel/dock SDE desde cero;
- wallpaper SineOS;
- Papelera visible;
- USB no visible en escritorio;
- tema/iconos/cursor SineOS;
- Picom SDE;
- LightDM SineOS;
- TLP migrado de forma controlada;
- redes/VPN preservadas;
- asociaciones de aplicaciones preservadas;
- autostart preservado salvo conflictos;
- Bluetooth preservado;
- impresoras/escáneres funcionales preservados.

# C10 — Configuración

Debe pasar:
- Configuración de SineOS;
- categorías de usuario coherentes;
- Mostrar configuración avanzada;
- persistencia de esa elección;
- niveles de riesgo de Configuración avanzada;
- puntos ligeros de restauración de 7 días;
- reversión automática solo ante fallas críticas inmediatas;
- recomendación de revertir ante inestabilidad;
- protección de ajustes críticos en modo lectura o flujo administrativo explícito;
- una configuración, un lugar.

# C11 — Rendimiento

Objetivos iniciales:
- RAM adicional idle objetivo <= 150 MB;
- CPU adicional idle ~0–1 %;
- procesos residentes extra <= 2–3;
- grabadores residentes = 0;
- servicios duplicados = 0;
- sin escrituras continuas innecesarias.

Estos valores deben medirse en el hardware físico de referencia.

# C12 — Documentación y replicabilidad

Debe existir:
- documentación en español de México;
- dependencias declaradas;
- manifiesto de paquetes;
- release/tag/commit reproducible;
- checksums;
- scripts idempotentes;
- procedimientos de instalación;
- actualización;
- rollback;
- desinstalación;
- recuperación;
- troubleshooting;
- matriz de soporte honesta.

# Exclusiones permitidas de SDE 1.0

No bloquean SDE 1.0 si quedan correctamente documentadas:
- Carpetas protegidas;
- pantalla inalámbrica sin backend certificado;
- Overview completo;
- búsqueda amplia de archivos;
- wallpapers distintos por monitor;
- historial avanzado de notificaciones;
- normalización avanzada de iconos externos.

# Regla final

> SDE 1.0 está terminado únicamente cuando puede usarse, romperse, recuperarse y reproducirse de forma predecible en el hardware físico certificado.
