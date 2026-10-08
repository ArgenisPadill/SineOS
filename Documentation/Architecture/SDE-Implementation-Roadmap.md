# SDE — Roadmap de implementación 1.0

**Fecha de decisión:** 07-10-2026  
**Estado:** orden de implementación congelado  
**Issue maestro:** https://github.com/ArgenisPadill/SineOS/issues/1

## Regla de ejecución

SDE se implementa en orden de riesgo:

> recuperación → sesión → escritorio → pantallas → hardware e integración → configuración → certificación.

No se avanza a una fase que pueda romper el sistema si la fase anterior todavía no tiene rollback funcional.

# Fases

## Fase 1 — Recovery y respaldo pre-SDE

Implementar primero:
- snapshot/respaldo completo de XFCE actual;
- respaldo de LightDM, Picom, TLP, panel, atajos y wallpaper;
- rollback;
- Modo seguro;
- Last Known Good / Último estado funcional;
- recuperación local;
- recuperación desde release/tag/commit certificado;
- recuperación offline.

## Fase 2 — Base de sesión

- Plymouth;
- LightDM + Slick Greeter;
- pantalla de bloqueo SineOS;
- `Super+L`;
- hibernación al cerrar tapa;
- validación después de reanudar;
- apagado/reinicio gráfico.

## Fase 3 — Base visual

- tema;
- iconos;
- cursor;
- wallpaper SineOS;
- panel superior;
- dock;
- tipografía;
- Picom;
- OSD;
- notificaciones;
- materiales y movimiento.

## Fase 4 — Pantallas

- `Super+P`;
- duplicar;
- extender;
- solo pantalla interna;
- transacción con rollback;
- recuperación de ventanas;
- DPI y resoluciones;
- proyectores;
- Safe Areas.

## Fase 5 — Red y conectividad

- Wi-Fi guardado;
- 3 reintentos;
- Ethernet prioritario;
- failover a Wi-Fi;
- VPN con 3 reintentos;
- portal cautivo;
- Firefox para autenticación;
- coordinación con DNS cifrado y VPN.

## Fase 6 — Bluetooth, USB y almacenamiento

- reconexión Bluetooth;
- cambio automático de audio;
- montaje USB;
- indicador en barra;
- expulsión segura;
- avisos de espacio;
- SMART;
- protección de almacenamiento crítico.

## Fase 7 — Audio, cámara, micrófono y privacidad

- permisos sensibles;
- indicadores de uso;
- ubicación;
- captura/compartición;
- acceso remoto;
- bitácora de sesiones;
- autorizaciones Polkit temporales.

## Fase 8 — Impresión y escaneo

- instalación guiada;
- hoja de prueba SineOS;
- consumibles;
- mantenimiento;
- escaneo;
- OCR multidioma;
- PDF buscable;
- revisión antes de guardar.

## Fase 9 — Actualizaciones

- `apt update` al iniciar;
- agrupación por impacto;
- seguridad crítica;
- políticas de batería;
- límite hotspot 250 MB;
- puntos de restauración de 2 semanas;
- reportes de fallo.

## Fase 10 — Salud y diagnóstico

- batería;
- temperatura;
- ventiladores;
- RAM;
- CPU;
- GPU;
- SMART;
- sistema de archivos;
- aplicaciones congeladas;
- reportes de 6 meses;
- respaldo prioritario cuando corresponda.

## Fase 11 — Configuración de SineOS

- panel central de configuración;
- Apariencia;
- Pantallas;
- Audio;
- Red;
- Mouse y teclado;
- Notificaciones;
- Energía;
- Accesibilidad;
- Atajos;
- Privacidad;
- Aplicaciones;
- Sistema;
- configuración avanzada opcional;
- puntos ligeros de restauración de **7 días** para cambios avanzados importantes;
- reversión automática solo ante fallas críticas inmediatas;
- recomendación de revertir si hay inestabilidad pero el sistema sigue utilizable.

## Fase 12 — Rofi / launcher / acciones

SDE 1.0:
- aplicaciones;
- acciones del sistema;
- configuración;
- carpetas frecuentes.

No incluir indexador pesado de archivos en 1.0.

## Fase 13 — Certificación final

- C0 a C5;
- hardware físico de referencia;
- hibernación/reanudación;
- HDMI;
- rollback;
- reinstalación;
- consumo RAM/CPU/GPU;
- documentación final;
- sin necesidad de laboratorio de máquinas virtuales para certificación de hardware.

# Elementos diferibles a 1.1 o módulo posterior

- Carpetas protegidas;
- pantalla inalámbrica si no existe backend suficientemente estable;
- Overview completo si no pasa estabilidad/rendimiento;
- búsqueda amplia de archivos;
- normalización sofisticada de iconos externos;
- historial avanzado de notificaciones;
- wallpapers distintos por monitor.

## Overview

`Super+Tab` puede entrar en SDE 1.0 solo si la implementación elegida supera pruebas de estabilidad, rendimiento y recuperación.

Si no:
- conservar fallback funcional de XFWM/Alt+Tab;
- mover Overview completo a versión posterior.

## Pantalla inalámbrica

`Super+P` conserva la opción **Pantalla inalámbrica**.

Si el módulo no está instalado/certificado:
- informar que no está disponible;
- nunca afectar HDMI, DisplayPort o XRandR.

# Criterio de inicio de implementación

La construcción de Alpha 0.1 comienza únicamente después de:
- documentación consolidada;
- Definition of Done 1.0 congelada;
- manifiesto técnico inicial de paquetes/dependencias;
- recuperación pre-SDE definida.

## Regla final

> Primero se demuestra que SineOS puede volver atrás; después se le permite cambiar el escritorio.
