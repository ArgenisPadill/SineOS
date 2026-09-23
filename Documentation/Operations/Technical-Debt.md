# SineOS — Deuda Técnica

## 1. Propósito

Este documento centraliza la deuda técnica conocida de SineOS.

Su objetivo es distinguir entre:

```text
funcional
```

y:

```text
terminado
```

Un componente puede estar operativo y aun mantener pendientes relacionados con:

- seguridad;
- reproducibilidad;
- automatización;
- backups;
- recuperación;
- mantenimiento;
- documentación.

Este documento no sustituye la documentación específica de cada componente.

---

## 2. Criterios de prioridad

Se utilizan tres niveles:

### Alta

Puede afectar:

- seguridad;
- pérdida de datos;
- recuperación;
- exposición de servicios;
- secretos.

### Media

Puede afectar:

- reproducibilidad;
- mantenimiento;
- automatización;
- migraciones;
- estabilidad operativa.

### Baja

Mejora principalmente:

- comodidad;
- organización;
- optimización;
- experiencia de administración.

---

## 3. Resumen

| ID | Prioridad | Área | Pendiente | Estado |
|---|---|---|---|---|
| TD-001 | Alta | Seguridad | Implementar política nftables | Pendiente |
| TD-002 | Alta | Ollama | Revisar exposición de `11434` | Pendiente |
| TD-003 | Alta | PostgreSQL | Rotar credenciales | Pendiente |
| TD-004 | Alta | Secretos | Formalizar gestión de secretos | Pendiente |
| TD-005 | Alta | Backups | Definir política general de backup | Pendiente |
| TD-006 | Alta | PostgreSQL | Validar backup y restauración | Pendiente |
| TD-007 | Alta | Vault | Definir backup del Knowledge Vault | Pendiente |
| TD-008 | Media | PostgreSQL | Migrar autostart a Quadlet | Pendiente |
| TD-009 | Media | PostgreSQL | Corregir red del Quadlet | Pendiente |
| TD-010 | Media | Open WebUI | Fijar versión o digest | Pendiente |
| TD-011 | Alta | Open WebUI | Definir secret persistente | Pendiente |
| TD-012 | Media | Miyo | Sincronizar AppImage y CLI | Pendiente |
| TD-013 | Media | Miyo | Benchmark semántico multinota | Pendiente |
| TD-014 | Baja | Miyo | Eliminar nota temporal de prueba | Pendiente |
| TD-015 | Baja | Shell | Hacer permanente `~/.local/bin` | Pendiente |
| TD-016 | Media | Recuperación | Documentar migración completa | Pendiente |
| TD-017 | Alta | Recuperación | Probar recuperación ante desastre | Pendiente |
| TD-018 | Media | Open WebUI | Evaluar gestión futura mediante Quadlet | Pendiente |

---

# 4. Seguridad

## TD-001 — Política nftables

**Prioridad:** Alta
**Estado:** Pendiente

### Situación

La política definitiva de firewall de SineOS todavía no está implementada.

Esto es especialmente relevante porque algunos servicios pueden escuchar fuera de loopback.

### Objetivo

Definir una política explícita que determine:

```text
qué entra
qué sale
qué servicios escuchan
qué interfaces pueden acceder
```

### Criterio de cierre

```text
[ ] Política definida
[ ] Reglas documentadas
[ ] Reglas aplicadas
[ ] Persistencia validada después de reinicio
[ ] Servicios autorizados comprobados
[ ] Servicios no autorizados bloqueados
```

---

## TD-002 — Exposición de Ollama

**Prioridad:** Alta
**Estado:** Pendiente

### Situación

Ollama utiliza actualmente:

```text
OLLAMA_HOST=0.0.0.0:11434
```

Esta configuración permitió la integración con componentes como Open WebUI.

Sin embargo, la exposición debe revisarse junto con la política de firewall.

### Objetivo

Permitir únicamente los accesos realmente necesarios.

### Criterio de cierre

```text
[ ] Identificar consumidores autorizados
[ ] Definir alcance de red necesario
[ ] Implementar protección
[ ] Validar Open WebUI → Ollama
[ ] Validar clientes locales necesarios
[ ] Comprobar que accesos no autorizados estén bloqueados
```

Referencia:

```text
Documentation/Operations/Ollama.md
```

---

## TD-003 — Rotación de credenciales PostgreSQL

**Prioridad:** Alta
**Estado:** Pendiente

### Situación

Las credenciales utilizadas durante la implementación inicial deben rotarse como parte del hardening.

### Objetivo

Generar nuevas credenciales y actualizar únicamente los consumidores autorizados.

### Criterio de cierre

```text
[ ] Nueva credencial generada
[ ] Servicios dependientes actualizados
[ ] Credencial anterior invalidada
[ ] Acceso validado
[ ] Ningún secreto agregado a Git
```

Referencia:

```text
Documentation/Operations/PostgreSQL.md
```

---

## TD-004 — Gestión de secretos

**Prioridad:** Alta
**Estado:** Pendiente

### Situación

SineOS contempla:

```text
Containers/secrets/
```

pero todavía no existe una política definitiva para la administración de secretos.

### Objetivo

Definir cómo almacenar y proporcionar:

- contraseñas;
- API keys;
- tokens;
- secretos de aplicaciones.

### Principio

```text
Git
 ↓
configuración

Gestor de secretos
 ↓
credenciales
```

### Criterio de cierre

```text
[ ] Estrategia seleccionada
[ ] Secretos fuera de Git
[ ] Permisos definidos
[ ] Procedimiento de rotación documentado
[ ] Procedimiento de recuperación documentado
```

---

# 5. Backups y recuperación

## TD-005 — Política general de backup

**Prioridad:** Alta
**Estado:** Pendiente

### Situación

Existen estructuras previstas para backups, pero todavía no existe una política integral.

### Objetivo

Definir:

```text
qué
cuándo
dónde
cuánto tiempo
cómo cifrar
cómo verificar
cómo restaurar
```

### Datos prioritarios

```text
Knowledge Vault
PostgreSQL
configuraciones no reproducibles
secretos según política futura
```

### Criterio de cierre

```text
[ ] Fuentes críticas identificadas
[ ] Frecuencia definida
[ ] Retención definida
[ ] Destino definido
[ ] Cifrado evaluado
[ ] Automatización implementada
[ ] Restauración probada
```

---

## TD-006 — Backup y restauración PostgreSQL

**Prioridad:** Alta
**Estado:** Pendiente

### Situación

PostgreSQL tiene persistencia validada, pero persistencia no equivale a backup.

### Objetivo

Implementar una estrategia de backup y demostrar que puede restaurarse.

### Criterio de cierre

```text
[ ] Método seleccionado
[ ] Backup automatizado
[ ] Retención definida
[ ] Backup validado
[ ] Restauración en entorno controlado
[ ] Integridad comprobada
[ ] Procedimiento documentado
```

Principio:

> Un backup no está validado hasta que puede restaurarse.

---

## TD-007 — Backup del Knowledge Vault

**Prioridad:** Alta
**Estado:** Pendiente

### Situación

El Knowledge Vault contiene la memoria permanente de SineOS:

```text
/home/argenis/Obsidian/SineOS
```

Miyo puede reconstruir su índice.

Las notas del Vault no son reemplazables de la misma manera.

### Objetivo

Proteger el Vault independientemente del índice de Miyo.

### Criterio de cierre

```text
[ ] Método de backup seleccionado
[ ] Copia externa definida
[ ] Frecuencia definida
[ ] Versionado evaluado
[ ] Restauración probada
[ ] Integridad comprobada
```

---

# 6. PostgreSQL / Podman

## TD-008 — Migración a Quadlet

**Prioridad:** Media
**Estado:** Pendiente

### Situación

PostgreSQL utiliza actualmente un mecanismo funcional de systemd de usuario.

La arquitectura prevista es migrar a Quadlet.

### Objetivo

Integrar PostgreSQL de forma nativa con:

```text
Podman
+
systemd
+
Quadlet
```

### Criterio de cierre

```text
[ ] Quadlet corregido
[ ] Servicio inicia
[ ] Servicio detiene correctamente
[ ] Autostart validado
[ ] Reinicio del equipo probado
[ ] Persistencia validada
[ ] Healthcheck validado
```

---

## TD-009 — Red del Quadlet PostgreSQL

**Prioridad:** Media
**Estado:** Pendiente

### Situación

Existe una discrepancia entre:

```text
Network=postgres
```

y la red real:

```text
sineos-postgres
```

### Objetivo

Corregir la referencia antes de activar definitivamente el Quadlet.

### Criterio de cierre

```text
[ ] Nombre real confirmado
[ ] Quadlet corregido
[ ] Red disponible
[ ] PostgreSQL inicia
[ ] Conectividad validada
```

---

# 7. Open WebUI

## TD-010 — Fijar imagen

**Prioridad:** Media
**Estado:** Pendiente

### Situación

Actualmente se utiliza:

```text
ghcr.io/open-webui/open-webui:main
```

`main` es una etiqueta móvil.

### Riesgo

Una descarga futura puede producir un runtime distinto sin cambios en Git.

### Objetivo

Utilizar:

```text
versión explícita
```

o:

```text
digest
```

### Criterio de cierre

```text
[ ] Versión seleccionada
[ ] Imagen probada
[ ] Compose actualizado
[ ] Persistencia validada
[ ] Ollama validado
[ ] Cambio documentado
```

---

## TD-011 — Secret persistente Open WebUI

**Prioridad:** Alta
**Estado:** Pendiente

### Situación

Todavía debe definirse un secret persistente administrado correctamente.

### Objetivo

Evitar secretos embebidos directamente en archivos versionados.

### Criterio de cierre

```text
[ ] Secret generado
[ ] Almacenamiento seguro
[ ] Integración implementada
[ ] Reinicio validado
[ ] Secret ausente de Git
```

---

## TD-018 — Evaluar Quadlet para Open WebUI

**Prioridad:** Media
**Estado:** Pendiente

### Situación

Open WebUI utiliza actualmente Compose con:

```text
restart: unless-stopped
```

La estrategia futura de servicios de SineOS puede utilizar Quadlet.

### Objetivo

Evaluar si Open WebUI debe migrarse al mismo modelo operativo que otros servicios persistentes.

### Criterio de cierre

Una de estas dos decisiones debe quedar documentada:

```text
[ ] Migrar a Quadlet
```

o:

```text
[ ] Mantener Compose deliberadamente
```

---

# 8. Miyo

## TD-012 — Sincronización AppImage / CLI

**Prioridad:** Media
**Estado:** Pendiente

### Situación

La aplicación se encuentra en:

```text
~/.local/opt/miyo/Miyo.AppImage
```

El CLI funcional fue extraído y copiado a:

```text
~/.miyo/bin/miyo
```

Actualizar la AppImage no actualiza automáticamente esta copia.

### Objetivo

Crear un procedimiento reproducible para mantener ambas versiones sincronizadas.

### Criterio de cierre

```text
[ ] Procedimiento definido
[ ] Versión comprobable
[ ] Actualización probada
[ ] CLI validado después de actualización
[ ] Búsqueda semántica validada
```

---

## TD-013 — Benchmark semántico multinota

**Prioridad:** Media
**Estado:** Pendiente

### Objetivo

Validar recuperación y síntesis entre múltiples notas.

Debe probar:

```text
búsqueda conceptual
síntesis entre notas
recuperación de decisiones
consulta técnica previa a acciones
```

### Criterio de cierre

```text
[ ] Dos o más notas de prueba
[ ] Recuperación semántica correcta
[ ] Síntesis correcta
[ ] Prueba con agente
[ ] Resultado documentado
```

---

## TD-014 — Nota temporal Miyo

**Prioridad:** Baja
**Estado:** Pendiente

Actualmente existe una nota temporal:

```text
Prueba Miyo.md.md
```

Debe mantenerse únicamente hasta completar el benchmark semántico.

Después:

```text
[ ] Eliminar nota
[ ] Verificar watcher/index
[ ] Confirmar que ya no aparece en resultados
```

---

# 9. Shell y herramientas

## TD-015 — PATH de `~/.local/bin`

**Prioridad:** Baja
**Estado:** Pendiente

`llmfit` está instalado en:

```text
~/.local/bin/llmfit
```

Debe comprobarse que:

```text
~/.local/bin
```

se encuentre disponible permanentemente en Zsh.

### Criterio de cierre

```text
[ ] PATH revisado
[ ] Configuración persistente
[ ] Nueva sesión probada
[ ] llmfit disponible directamente
```

---

# 10. Migración y recuperación

## TD-016 — Procedimiento de migración

**Prioridad:** Media
**Estado:** Pendiente

Uno de los objetivos centrales de SineOS es evitar reconstruir manualmente todo el entorno al cambiar de computadora.

### Objetivo

Documentar:

```text
nuevo hardware
     ↓
Debian
     ↓
Git
     ↓
SineOS
     ↓
contenedores
     ↓
Vault
     ↓
datos
     ↓
IA
```

### Criterio de cierre

```text
[ ] Dependencias identificadas
[ ] Orden de instalación definido
[ ] Datos críticos identificados
[ ] Procedimiento escrito
[ ] Procedimiento probado
```

---

## TD-017 — Disaster Recovery

**Prioridad:** Alta
**Estado:** Pendiente

### Objetivo

Demostrar que SineOS puede recuperarse después de una pérdida importante del sistema.

Debe incluir al menos:

```text
repositorio
Vault
PostgreSQL
configuraciones
secretos necesarios
```

### Criterio de cierre

```text
[ ] Escenario definido
[ ] Backups disponibles
[ ] Restauración ejecutada
[ ] Servicios levantados
[ ] Datos verificados
[ ] Resultado documentado
```

---

# 11. Dependencias entre pendientes

Algunas tareas deben ejecutarse en orden.

### Seguridad

```text
TD-001 nftables
      ↓
TD-002 Ollama
```

### PostgreSQL

```text
TD-009 red Quadlet
      ↓
TD-008 migración Quadlet
```

### Backups

```text
TD-005 política general
      ↓
TD-006 PostgreSQL
      ↓
TD-017 Disaster Recovery
```

y:

```text
TD-005 política general
      ↓
TD-007 Vault
      ↓
TD-017 Disaster Recovery
```

### Miyo

```text
TD-013 benchmark
      ↓
TD-014 eliminar nota temporal
```

---

# 12. Orden sugerido de resolución

Por riesgo y dependencia:

```text
1.  Security Baseline
2.  TD-001 nftables
3.  TD-002 exposición Ollama
4.  TD-003 rotación PostgreSQL
5.  TD-004 gestión de secretos
6.  TD-011 secret Open WebUI
7.  TD-005 política de backup
8.  TD-007 backup Vault
9.  TD-006 backup PostgreSQL
10. TD-009 red Quadlet
11. TD-008 PostgreSQL Quadlet
12. TD-010 fijar Open WebUI
13. TD-012 actualizar Miyo/CLI
14. TD-013 benchmark Miyo
15. TD-014 eliminar prueba Miyo
16. TD-015 PATH
17. TD-016 migración
18. TD-017 Disaster Recovery
```

TD-018 puede resolverse junto con la estandarización futura de servicios.

---

# 13. Qué no debe hacerse

No resolver deuda técnica mediante cambios improvisados que creen una deuda mayor.

Evitar especialmente:

```text
chmod 777
chown arbitrario sobre volúmenes rootless
secretos dentro de Git
puertos abiertos innecesariamente
actualizaciones ciegas de bases de datos
etiquetas móviles como solución permanente
automatización sin recuperación probada
```

---

# 14. Regla de cierre

Una tarea no debe marcarse como terminada únicamente porque:

```text
se ejecutó un comando
```

Debe existir evidencia de que:

```text
cambio
  ↓
validación
  ↓
persistencia
  ↓
documentación
```

funcionan correctamente.

Cuando corresponda, también:

```text
rollback / recuperación
```

---

# 15. Mantenimiento de este documento

Cuando aparezca una deuda nueva:

1. asignar ID;
2. definir prioridad;
3. describir el estado actual;
4. definir objetivo;
5. definir criterio de cierre.

Cuando una deuda sea resuelta:

1. validar técnicamente;
2. actualizar la documentación específica;
3. marcarla como resuelta;
4. registrar el cambio en `CHANGELOG.md` cuando corresponda.

No eliminar inmediatamente el registro histórico de una deuda importante.

---

# 16. Estado general

SineOS dispone actualmente de una base funcional que incluye:

```text
Debian 13
Btrfs
Podman rootless
PostgreSQL 18
Ollama
Open WebUI
Obsidian
Miyo
Git / GitHub
arquitectura híbrida de IA
```

La siguiente fase no consiste en agregar servicios por agregar.

Consiste en fortalecer:

```text
seguridad
backups
recuperación
reproducibilidad
mantenimiento
```

El objetivo es convertir una plataforma funcional en una plataforma recuperable, mantenible y predecible.


---

# Revisión de deuda técnica — 2026-09-23

## Cerrado o redefinido

- **Firewall ausente:** cerrado. nftables está activo con entrada restrictiva.
- **PostgreSQL expuesto por el host:** cerrado para el escenario actual. El puerto se publica solo en `127.0.0.1:5432`.
- **Autostart de PostgreSQL:** redefinido. La política actual es arranque manual desde Podman Desktop; no se restaurará Quadlet/autostart mientras esta política siga vigente.
- **DNS de confianza:** implementado mediante DNSCrypt por perfil de NetworkManager y administrable con NetworkPrivacy.
- **Proton split tunneling fallando:** cerrado tras instalar headers del kernel y validar el servicio.

## Pendiente

- Determinar si alguna aplicación consume Tor en `127.0.0.1:9050`.
- Revisar formalmente la convivencia de `flush ruleset` de nftables con Podman/netavark.
- Validar desde otro equipo de la LAN que Ollama no sea accesible externamente bajo el firewall actual.
- Retirar `restart: unless-stopped` de Open WebUI para alinearlo con la política de arranque manual, recreando el contenedor sin afectar su volumen persistente.
- Auditar AppArmor con herramientas de usuario cuando se decida instalar `apparmor-utils`.
- Revisar candidatos de `apt autoremove` manualmente; no ejecutar autoremove a ciegas porque aparecen paquetes que pueden seguir siendo útiles, incluido `sshfs`.
- Completar cifrado, snapshots, backup y recuperación.
