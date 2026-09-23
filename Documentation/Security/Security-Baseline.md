# SineOS — Security Baseline

## 1. Propósito

Este documento define la línea base de seguridad de SineOS.

Su objetivo es establecer:

- qué controles existen actualmente;
- qué controles están parcialmente implementados;
- qué controles siguen pendientes;
- qué principios deben respetarse al incorporar nuevos servicios;
- qué condiciones deben cumplirse antes de considerar cerrado el hardening.

Este documento describe el estado real de SineOS.

No debe interpretarse como una declaración de que todos los controles aquí descritos ya están implementados.

---

## 2. Principio general

La seguridad de SineOS se diseña mediante capas.

```text
Sistema operativo
       ↓
Control de acceso
       ↓
Red
       ↓
Servicios
       ↓
Contenedores
       ↓
Secretos
       ↓
Datos
       ↓
Backups
       ↓
Monitoreo y auditoría
       ↓
Recuperación
```

Ninguna capa individual debe considerarse suficiente por sí sola.

---

## 3. Modelo de seguridad

Las capas previstas para SineOS son:

```text
1. Sistema operativo / hardening
2. AppArmor / Mandatory Access Control
3. Firewall / nftables
4. SSH
5. Podman rootless / aislamiento
6. Gestión de secretos
7. LUKS + Btrfs
8. Snapshots / recuperación
9. Monitoreo / auditoría
10. VPN / privacidad cuando corresponda
11. Gestor de contraseñas
12. Backup / Disaster Recovery
```

Algunas capas están operativas.

Otras todavía requieren implementación o validación formal.

---

# 4. Estado general

| Área | Estado |
|---|---|
| Debian 13 estable | Operativo |
| UEFI | Operativo |
| Secure Boot | Habilitado |
| Btrfs | Operativo |
| Podman rootless | Operativo |
| Git mediante SSH | Operativo |
| Servicios ligados a loopback cuando aplica | Operativo en PostgreSQL y servicios locales seleccionados; Ollama requiere excepción técnica por pasta |
| AppArmor | Requiere auditoría formal |
| nftables | Operativo; revisión de convivencia con Podman/netavark pendiente |
| Hardening SSH | Requiere auditoría formal |
| Gestión central de secretos | Pendiente |
| LUKS | Requiere verificación/documentación |
| Snapshots Btrfs | Pendiente de política formal |
| Backup Vault | Pendiente |
| Backup PostgreSQL | Pendiente |
| Disaster Recovery | Pendiente |
| Monitoreo integral | Pendiente |
| Auditoría SineOS | Operativa |
| Rotación de credenciales | Pendiente |

---

# 5. Sistema operativo

La plataforma base es:

```text
Debian 13 Trixie
```

Debian Stable fue seleccionado como base por:

- estabilidad;
- mantenimiento;
- disponibilidad de paquetes;
- documentación;
- ciclo de soporte;
- compatibilidad con las herramientas utilizadas.

La seguridad del sistema debe construirse sobre la instalación estable y no mediante modificaciones innecesarias del sistema base.

---

## 6. Actualizaciones

El sistema debe mantenerse actualizado mediante los mecanismos oficiales de Debian.

Antes de realizar cambios importantes debe distinguirse entre:

```text
actualización de seguridad
actualización normal
cambio mayor de versión
```

Los upgrades mayores requieren planificación adicional.

No deben mezclarse con tareas de hardening sin necesidad.

---

## 7. Firmware y arranque

El equipo utiliza:

```text
UEFI 64-bit
Secure Boot habilitado
```

Secure Boot constituye una capa adicional dentro de la cadena de arranque.

No sustituye:

- cifrado;
- control de acceso;
- actualizaciones;
- backups.

---

# 8. Almacenamiento

El filesystem principal utiliza:

```text
Btrfs
```

Btrfs permite capacidades útiles como:

- subvolúmenes;
- snapshots;
- administración flexible del almacenamiento.

Sin embargo:

> Snapshot no equivale a backup.

Una pérdida física del dispositivo puede afectar simultáneamente los datos originales y sus snapshots locales.

---

## 9. Cifrado de almacenamiento

La arquitectura de seguridad contempla:

```text
LUKS
```

como capa de cifrado de almacenamiento.

Su estado exacto debe verificarse y documentarse antes de marcarlo como control validado.

Estado:

```text
REQUIERE VERIFICACIÓN
```

No debe suponerse que la existencia de Btrfs implica cifrado.

---

## 10. Snapshots

La arquitectura contempla snapshots Btrfs para facilitar:

- rollback;
- recuperación de cambios;
- protección frente a errores administrativos.

Todavía debe definirse formalmente:

```text
frecuencia
retención
automatización
limpieza
pruebas de restauración
```

Estado:

```text
PENDIENTE DE POLÍTICA
```

---

# 11. Usuarios y privilegios

Principio:

> Utilizar el menor privilegio necesario.

Los servicios que puedan ejecutarse sin privilegios administrativos deben preferir ese modelo.

Ejemplo actualmente implementado:

```text
Podman rootless
```

La administración cotidiana no debe realizarse como `root` cuando no sea necesario.

---

## 12. sudo

El uso de `sudo` debe reservarse para operaciones que realmente requieran privilegios administrativos.

Antes de ejecutar una instrucción privilegiada debe conocerse:

```text
qué modifica
por qué necesita root
cómo verificar el resultado
cómo revertirlo si falla
```

Evitar utilizar `sudo` como solución automática a problemas de permisos.

---

# 13. Podman rootless

SineOS utiliza:

```text
Podman 5.4.2
```

en modalidad rootless.

Esto reduce el impacto potencial de determinados errores de configuración de contenedores.

Arquitectura:

```text
usuario
   ↓
Podman rootless
   ↓
user namespace
   ↓
contenedor
```

Rootless constituye una capa de reducción de privilegios.

No convierte automáticamente un contenedor en seguro.

---

## 14. UID mapping

Los contenedores rootless pueden utilizar UID subordinados en el host.

Ejemplo validado con PostgreSQL:

```text
UID host observado: 100998
```

Esto no debe corregirse mediante:

```text
chmod 777
```

o:

```text
chown
```

arbitrario.

Primero debe comprenderse el user namespace.

---

## 15. Imágenes de contenedor

Las imágenes deben provenir de fuentes identificables.

Cuando un servicio alcance estabilidad operativa debe evitarse depender indefinidamente de etiquetas móviles.

Ejemplo actual pendiente:

```text
ghcr.io/open-webui/open-webui:main
```

La estrategia futura debe utilizar:

```text
versión fija
```

o:

```text
digest
```

cuando corresponda.

---

# 16. Red

La política de red debe seguir el principio:

> Un servicio no debe ser accesible desde más lugares de los necesarios.

Siempre que sea posible debe distinguirse entre:

```text
loopback
LAN
VPN
Internet
red de contenedores
```

Cada servicio debe tener una razón explícita para escuchar fuera de loopback.

---

## 17. nftables

OPERATIVO — validado el 23-09-2026.

INPUT usa política `drop`. Se permiten loopback, `established,related`, ICMP/ICMPv6 y LocalSend TCP/UDP 53317 limitado a `192.168.0.0/24`. La salida permanece permitida. Pendiente: revisar `flush ruleset` frente a Podman/netavark.

## 18. Regla de firewall

La implementación de nftables debe realizarse con especial cuidado para evitar:

- pérdida de conectividad;
- bloqueo de servicios necesarios;
- reglas demasiado permisivas;
- reglas no persistentes.

Antes de activar una política debe existir una forma de recuperación.

---

# 19. Ollama

Ollama utiliza actualmente:

```text
OLLAMA_HOST=0.0.0.0:11434
```

Esto permite que componentes como Open WebUI alcancen el runtime desde el entorno de contenedores.

Sin embargo, también significa que Ollama no está ligado exclusivamente a loopback.

Estado:

```text
FUNCIONAL
+
HARDENING PENDIENTE
```

---

## 20. Riesgo de Ollama

La configuración:

```text
0.0.0.0:11434
```

debe revisarse conjuntamente con:

```text
nftables
networking Podman
clientes autorizados
```

No debe exponerse Ollama a redes que no necesiten utilizarlo.

Referencia:

```text
Documentation/Operations/Ollama.md
Documentation/Operations/Technical-Debt.md
```

---

# 21. Open WebUI

Open WebUI utiliza:

```text
127.0.0.1:3000:8080
```

Esto limita la interfaz web al loopback del host.

Estado:

```text
ACCESO LOCAL CONFIGURADO
```

No debe modificarse a:

```text
0.0.0.0:3000
```

sin una decisión explícita de arquitectura y seguridad.

---

## 22. Open WebUI y secretos

La configuración definitiva de un secret persistente de Open WebUI sigue pendiente.

Un secret real no debe incorporarse directamente al archivo:

```text
Containers/stacks/open-webui/compose.yaml
```

si el archivo será versionado.

---

# 23. PostgreSQL

PostgreSQL se ejecuta mediante:

```text
Podman rootless
```

con persistencia fuera de la capa efímera del contenedor.

Los controles relevantes incluyen:

- aislamiento rootless;
- permisos del volumen;
- credenciales;
- exposición de red;
- backups;
- logs;
- disponibilidad comprobable mediante `pg_isready` cuando el contenedor está activo.

---

## 24. Credenciales PostgreSQL

Las credenciales utilizadas durante la configuración inicial deben considerarse información sensible.

No deben aparecer en:

```text
README
CHANGELOG
documentación
scripts públicos
commits
ejemplos reales
```

Existe una tarea pendiente de rotación de credenciales.

---

# 25. Gestión de secretos

La política general de secretos todavía debe formalizarse.

La estructura del proyecto contempla:

```text
Containers/secrets/
```

pero la existencia del directorio no constituye por sí sola una solución segura.

Estado:

```text
PENDIENTE
```

---

## 26. Principios de secretos

Los secretos deben cumplir:

```text
fuera de Git
mínimo acceso
rotación posible
recuperación controlada
no exposición en documentación
```

Ejemplos:

- API keys;
- tokens;
- contraseñas;
- secretos de aplicaciones;
- credenciales de bases de datos.

---

## 27. Git

Git contiene:

```text
código
infraestructura
scripts
documentación
configuración reproducible
```

Git no debe contener:

```text
contraseñas
tokens
API keys
datos privados
backups de bases de datos
reportes sensibles
```

---

## 28. .gitignore

`.gitignore` constituye una medida preventiva, no una frontera de seguridad.

Un archivo ignorado todavía puede:

- copiarse accidentalmente;
- compartirse;
- quedar en backups;
- contener permisos incorrectos.

Los secretos deben protegerse independientemente de `.gitignore`.

---

# 29. Auditoría

SineOS dispone del auditor:

```text
Scripts/Audit/sineos-audit.sh
```

El script recopila información diagnóstica del sistema.

Actualmente incluye también una sección dedicada a PostgreSQL:

```text
13.1 - POSTGRESQL SINEOS
```

---

## 30. Reportes de auditoría

Los reportes pueden contener información sensible sobre:

- hardware;
- hostname;
- usuarios;
- red;
- servicios;
- contenedores;
- almacenamiento;
- configuración.

Por ello los reportes `.txt` generados bajo:

```text
Documentation/Audit/
```

están excluidos de Git.

---

## 31. Auditoría no equivale a hardening

El auditor permite observar el estado.

No aplica automáticamente correcciones.

Separación:

```text
auditoría
   ↓
descubrir

hardening
   ↓
corregir
```

Esto evita que una herramienta de diagnóstico realice cambios inesperados.

---

# 32. AppArmor

AppArmor forma parte de la arquitectura de seguridad prevista para SineOS.

Sin embargo, antes de declarar esta capa como validada debe comprobarse:

- estado del servicio;
- perfiles activos;
- modo enforce/complain;
- cobertura real de aplicaciones relevantes.

Estado:

```text
REQUIERE AUDITORÍA FORMAL
```

---

# 33. SSH

GitHub utiliza autenticación mediante SSH y la conexión fue validada.

Esto no equivale a haber completado un hardening general del servicio SSH del host.

Debe distinguirse:

```text
cliente SSH
```

de:

```text
servidor SSH
```

La configuración de un servidor SSH debe auditarse únicamente si dicho servicio está instalado y habilitado.

---

## 34. GitHub SSH

La autenticación Git/GitHub mediante SSH se encuentra operativa.

Las claves privadas no deben:

- copiarse al repositorio;
- incluirse en documentación;
- enviarse por mensajería;
- almacenarse sin protección adecuada.

GitHub solo debe recibir la clave pública correspondiente.

---

# 35. Knowledge Vault

El Knowledge Vault reside en:

```text
/home/argenis/Obsidian/SineOS
```

Puede contener:

- conocimiento personal;
- documentación;
- información laboral;
- material académico;
- decisiones;
- procedimientos.

Debe tratarse como información local sensible.

---

## 36. Vault y Git

El Vault no forma parte del repositorio:

```text
/home/argenis/Workspace/SineOS
```

La separación es intencional.

```text
Workspace/SineOS
       ↓
infraestructura

Obsidian/SineOS
       ↓
conocimiento
```

No debe añadirse accidentalmente el Vault completo al repositorio.

---

# 37. Miyo

Miyo indexa semánticamente el Knowledge Vault.

El índice debe considerarse:

```text
derivado
```

y el Vault:

```text
fuente primaria
```

La pérdida del índice debe poder resolverse mediante reconstrucción.

La pérdida del Vault requiere recuperación desde backup.

---

## 38. IA cloud

La arquitectura puede utilizar:

```text
Gemini
DeepSeek
```

cuando aportan capacidad que los modelos locales no ofrecen.

Debe evitarse enviar información privada innecesaria.

Principio:

> Recuperar localmente y compartir únicamente el contexto necesario.

---

## 39. Ollama y privacidad

Ollama permite procesar localmente determinadas tareas.

Cuando un modelo local tenga capacidad suficiente y exista una razón de privacidad, debe preferirse el procesamiento local.

Esto no obliga a utilizar modelos locales para tareas que excedan claramente sus capacidades.

---

# 40. Backups

Los backups constituyen una capa de seguridad y continuidad.

Actualmente la política integral de backups sigue pendiente.

Prioridad:

```text
1. Datos irreemplazables
2. Knowledge Vault
3. PostgreSQL
4. Configuración no reproducible
5. Secretos según política definida
6. Estado secundario cuando sea necesario
```

---

## 41. Regla 3-2-1

La futura política de backup debe evaluar una estrategia equivalente al principio:

```text
3 copias
2 medios diferentes
1 copia fuera del equipo principal
```

La implementación concreta debe adaptarse a los recursos reales de SineOS.

No debe considerarse implementada hasta ser probada.

---

# 42. Disaster Recovery

Un backup solo tiene valor operativo si puede utilizarse para recuperar el sistema.

La futura prueba de Disaster Recovery debe considerar:

```text
Git
Vault
PostgreSQL
configuración
secretos necesarios
```

El resultado debe comprobarse en un entorno controlado.

---

# 43. Monitoreo

La arquitectura contempla:

```text
Prometheus
Grafana
Loki
Netdata
```

pero no deben declararse operativos únicamente porque existan directorios destinados a ellos.

Su estado debe documentarse después de implementación y validación.

---

# 44. Logs

Los logs pueden contener:

- nombres de usuario;
- rutas;
- direcciones IP;
- errores;
- identificadores;
- datos operativos.

No deben publicarse automáticamente.

Antes de compartir logs debe revisarse su contenido.

---

# 45. Datos personales

SineOS puede procesar información personal dentro del Vault y de proyectos futuros.

Debe aplicarse el principio:

```text
mínima información necesaria
```

No deben duplicarse datos sensibles innecesariamente entre servicios.

---

# 46. Actualizaciones

Una actualización no debe reducir controles existentes sin detectarlo.

Después de actualizaciones importantes deben revisarse:

```text
servicios
puertos
permisos
contenedores
logs
firewall
integraciones
```

Especialmente cuando se actualicen:

- Podman;
- Ollama;
- Open WebUI;
- PostgreSQL;
- Miyo.

---

# 47. Nuevos servicios

Antes de incorporar un nuevo servicio debe responderse:

```text
¿Qué problema resuelve?
¿Qué puerto utiliza?
¿Necesita Internet?
¿Necesita LAN?
¿Qué datos almacena?
¿Qué privilegios necesita?
¿Qué secretos utiliza?
¿Cómo se actualiza?
¿Cómo se respalda?
¿Cómo se elimina?
```

Si estas preguntas no tienen respuesta, el servicio todavía no está listo para incorporarse como componente permanente.

---

# 48. Puertos

Cada puerto abierto debe tener una razón.

La política futura debe mantener un inventario de:

```text
servicio
puerto
protocolo
interfaz
consumidor
justificación
```

Puertos conocidos actualmente relevantes:

```text
11434/tcp → Ollama
3000/tcp  → Open WebUI en loopback
```

Otros servicios deben agregarse al inventario cuando se implementen y validen.

---

# 49. Principio deny by default

La futura política de firewall debe evaluar un enfoque:

```text
denegar por defecto
        ↓
permitir explícitamente lo necesario
```

Debe implementarse de forma controlada para no perder conectividad administrativa.

---

# 50. Cambios de seguridad

Los cambios de seguridad deben seguir:

```text
diagnóstico
   ↓
plan
   ↓
cambio
   ↓
validación
   ↓
persistencia
   ↓
documentación
```

Cuando exista riesgo significativo debe existir además:

```text
rollback
```

---

# 51. Acciones peligrosas

Evitar utilizar como solución rápida:

```text
chmod 777
desactivar firewall
desactivar Secure Boot sin causa
ejecutar contenedores privilegiados sin necesidad
usar root para todo
publicar servicios en 0.0.0.0 sin análisis
guardar secretos en Git
copiar claves privadas
```

---

# 52. Security Baseline mínimo

Antes de considerar cerrada la fase inicial de hardening deben estar resueltos al menos:

```text
[ ] Auditoría de AppArmor
[x] Política nftables
[ ] Revisión de exposición de Ollama
[ ] Auditoría SSH
[ ] Verificación/documentación de LUKS
[ ] Gestión de secretos
[ ] Rotación de credenciales PostgreSQL
[ ] Secret persistente Open WebUI
[ ] Backup del Vault
[ ] Backup PostgreSQL
[ ] Restauración probada
[ ] Política de snapshots
[ ] Revisión de puertos
[ ] Disaster Recovery probado
```

---

# 53. Relación con deuda técnica

Los pendientes de seguridad deben registrarse también en:

```text
Documentation/Operations/Technical-Debt.md
```

La documentación específica explica el componente.

Technical Debt permite seguir su resolución.

Security Baseline establece el estándar que debe alcanzarse.

---

# 54. Prioridades inmediatas

El siguiente bloque de seguridad debe concentrarse primero en:

```text
1. Auditar estado actual
2. Verificar AppArmor
3. Verificar LUKS
4. Inventariar puertos
5. Revisar convivencia nftables/Podman y validar Ollama desde LAN
6. Proteger Ollama
7. Formalizar secretos
8. Rotar credenciales
9. Diseñar backups
10. Probar recuperación
```

No deben realizarse todos estos cambios simultáneamente.

Cada control debe implementarse y validarse individualmente.

---

# 55. Estado

SineOS dispone de varias decisiones de seguridad ya incorporadas:

```text
Debian Stable
Secure Boot
Podman rootless
Open WebUI limitado a loopback
Git mediante SSH
separación Vault / repositorio
reportes de auditoría fuera de Git
```

Al mismo tiempo mantiene pendientes importantes:

```text
nftables
hardening de Ollama
gestión de secretos
rotación de credenciales
verificación de AppArmor
verificación de LUKS
snapshots
backups
Disaster Recovery
```

Por tanto, el estado actual debe describirse como:

```text
BASE FUNCIONAL
+
HARDENING EN PROGRESO
```

El objetivo de la siguiente fase es reducir la superficie de exposición y garantizar que los datos importantes puedan recuperarse sin sacrificar la mantenibilidad del sistema.


---

# Actualización operativa — 2026-09-23

## Firewall

SineOS utiliza actualmente `nftables` con una cadena de entrada de política `drop`. Se permiten loopback, tráfico `established,related`, ICMP/ICMPv6 y LocalSend TCP/UDP 53317 limitado a la red LAN configurada `192.168.0.0/24`.

La configuración actual utiliza `flush ruleset`. Aunque los contenedores rootless continúan funcionando, queda pendiente revisar formalmente su interacción a largo plazo con las reglas que pueda administrar Podman/netavark antes de considerar cerrado este punto.

## Privacidad DNS y VPN

DNSCrypt escucha localmente en `127.0.2.1:53` y se utiliza por perfil de NetworkManager en redes de confianza. No se fuerza globalmente para evitar problemas con redes públicas y portales cautivos.

Cuando Proton VPN está conectado, Proton toma control del DNS efectivo y de la ruta mediante WireGuard y policy routing. Al desconectarlo, NetworkManager vuelve al DNS configurado para el perfil Wi-Fi.

NetworkPrivacy proporciona una interfaz GTK3 para activar DNSCrypt en la red actual, restaurar exactamente la configuración DNS previa y mostrar cuándo DNSCrypt queda en espera porque Proton VPN está activo. El estado original por perfil se almacena fuera del repositorio en `~/.local/state/sineos-network-privacy/profiles.json` con permisos restrictivos.

## Servicios revisados

- KDE Connect: retirado por no utilizarse.
- i2pd: retirado tras verificar que Proton VPN no dependía de él.
- redsocks: retirado; no existían redirecciones activas que lo utilizaran.
- AnyDesk: conservado por uso real; funciona con conexiones salientes bajo la política actual.
- Dropbox y MEGA: conservados por uso real.
- Avahi: conservado por dependencias y posible descubrimiento de impresión/escaneo; la política de entrada puede limitar descubrimiento mDNS desde LAN.
- Tor: servicio local en `127.0.0.1:9050`; pendiente identificar consumidores antes de decidir su permanencia.
- Ollama: escucha en todas las interfaces por requerimiento de comunicación con el alias de host de pasta; nftables bloquea el acceso LAN no solicitado. Se mantiene pendiente una validación adicional desde otro dispositivo de la LAN.

## PostgreSQL

PostgreSQL 18 se publica exclusivamente como `127.0.0.1:5432`. Se retiró `restart: unless-stopped` para mantener la política de inicio manual desde Podman Desktop. La persistencia se conserva mediante bind mount y fue validada después de recrear el contenedor.
