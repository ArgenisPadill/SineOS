# SineOS — Gestión de secretos

**Estado:** Adoptado — implementación en progreso  
**Fecha:** 23-09-2026

## Propósito

Definir dónde pueden almacenarse credenciales, tokens, claves y otros secretos utilizados por SineOS, cómo deben protegerse y cómo se comprueba que no entren al repositorio.

## Principio

> Un secreto debe existir únicamente donde el componente que lo necesita pueda acceder a él, con el menor alcance y privilegio posibles.

Git conserva configuración reproducible, ejemplos y estructura. Git no conserva valores secretos reales.

## Qué se considera secreto

Entre otros:

- contraseñas;
- API keys;
- tokens;
- URLs Push que incorporen credenciales;
- claves privadas;
- secretos JWT;
- credenciales de bases de datos;
- material de autenticación;
- certificados privados;
- secretos persistentes de aplicaciones.

Un backup o dump de base de datos puede no ser una credencial, pero se trata como **dato sensible** porque puede contener configuración o información privada.

## Ubicaciones permitidas

### 1. `.env` local junto a un stack

Se permite cuando la herramienta de despliegue espera el archivo en esa ubicación y moverlo aportaría complejidad sin beneficio real.

Ejemplo actual:

```text
Containers/stacks/postgres/.env
```

Requisitos:

```text
Git: ignorado
archivo: 600
propietario: usuario SineOS
ejemplo versionado: .env.example sin valores reales
```

### 2. Configuración privada de usuario

Para secretos operativos que no necesitan residir junto al stack:

```text
~/.config/sineos/<componente>/
```

Requisitos:

```text
directorio SineOS: 700
subdirectorios sensibles: 700
archivos secretos: 600
```

Ejemplo validado:

```text
~/.config/sineos/monitoring/open-webui.env
~/.config/sineos/monitoring/postgresql.env
```

### 3. Almacén genérico de secretos

Para futuros componentes que no tengan una ubicación operativa propia se reserva:

```text
~/.config/sineos/secrets/
```

Este directorio no obliga a mover secretos existentes que ya estén correctamente protegidos y cuya ubicación sea parte del funcionamiento del componente.

Permisos requeridos:

```text
700  ~/.config/sineos/secrets/
600  archivos contenidos
```

### 4. Secretos generados por aplicaciones

Algunas aplicaciones generan su propio material criptográfico dentro de volúmenes persistentes.

Ejemplo:

```text
Containers/volumes/stirling-pdf/configs/backup/keys/
```

Estos archivos:

- permanecen fuera de Git;
- siguen la semántica de ownership requerida por el contenedor;
- no se copian a documentación;
- se auditan sin mostrar su contenido;
- pueden tener limitaciones de permisos impuestas por la aplicación upstream.

En Stirling PDF 2.14.3 se comprobó que el entrypoint restablece recursivamente `/configs` a modo 755 durante el arranque. No se mantiene un parche local frágil; la deuda queda registrada hasta una versión estable que permita conservar modos restrictivos.

## Ubicaciones prohibidas

Un secreto real no debe almacenarse en:

```text
README
CHANGELOG
Documentation/
Scripts/ versionados
Apps/ versionadas
compose.yaml versionado
.env.example
commits
issues públicos
capturas o reports públicos
```

## `.gitignore`

`.gitignore` es una barrera preventiva, no una solución de secretos.

SineOS ignora patrones como:

```text
.env
.env.*
*.secret
*.secrets
*.key
*.pem
Containers/volumes/*
Containers/backups/*
Containers/logs/*
```

Antes de confiar en `.gitignore` debe comprobarse que el archivo nunca haya sido rastreado previamente.

## Permisos

Valores de referencia:

| Tipo | Permiso esperado |
|---|---:|
| Directorio privado | 700 |
| Archivo secreto | 600 |
| Clave privada | 600 cuando la aplicación lo permite |
| Clave pública | 644 puede ser aceptable |
| `.env` con credenciales | 600 |
| Reporte de seguridad con hallazgos | 600 |

Las restricciones del runtime o de una aplicación externa deben documentarse si impiden aplicar estos modos.

## Inventario actual

| Componente | Ubicación | Tipo | Estado |
|---|---|---|---|
| PostgreSQL | `Containers/stacks/postgres/.env` | credenciales DB | Protegido 600 / fuera de Git |
| Monitoring Open WebUI | `~/.config/sineos/monitoring/open-webui.env` | Push URL | Protegido 600 |
| Monitoring PostgreSQL | `~/.config/sineos/monitoring/postgresql.env` | Push URL | Protegido 600 |
| Stirling PDF | volumen persistente `/configs` | JWT key generada | Fuera de Git; permisos controlados por upstream 2.14.3 |
| Open WebUI | pendiente | secret persistente | TD-005 |

Los valores reales nunca deben incluirse en este inventario.

## Escaneo de Git

SineOS utiliza Gitleaks para comprobar el working tree y el historial de Git.

Debian 13 Trixie proporciona el paquete `gitleaks` en sus repositorios oficiales.

Los reportes locales deben almacenarse fuera del repositorio, por ejemplo:

```text
~/.local/state/sineos/security/gitleaks/
```

con permisos:

```text
700 directorio
600 reportes
```

Los escaneos deben utilizar redacción de secretos cuando la herramienta lo permita.

## Hallazgo confirmado

Si Gitleaks encuentra una credencial real:

```text
no publicar el valor
      ↓
confirmar si es real
      ↓
rotar/revocar primero
      ↓
limpiar configuración actual
      ↓
evaluar historial Git
      ↓
documentar el incidente sin el secreto
```

Eliminar únicamente el texto del último commit no invalida una credencial que ya haya sido publicada.

## Rotación

Todo secreto debe poder rotarse sin reconstruir innecesariamente el sistema completo.

Se prioriza rotación cuando:

- se confirmó exposición;
- fue compartido accidentalmente;
- existe sospecha de compromiso;
- una política o proveedor lo exige;
- el componente cambia de propietario o alcance.

No se rota una credencial funcional únicamente para aparentar seguridad si no existe un procedimiento validado para actualizar todos sus consumidores.

## Backups

Los secretos necesarios para recuperar un servicio deben incluirse en la futura estrategia de backup de forma cifrada y controlada.

Un backup de secretos no debe almacenarse en Git.

## Herramientas futuras

`pass`, GPG, age/sops o mecanismos de secretos de Podman pueden evaluarse cuando aporten una ventaja concreta.

No se adopta una herramienta adicional hasta verificar:

- compatibilidad con Debian 13;
- integración con los consumidores;
- recuperación de claves;
- backup;
- complejidad operativa;
- comportamiento con Podman rootless.

## Definition of Done

TD-001 puede cerrarse cuando:

```text
[ ] Política documentada
[x] Directorio ~/.config/sineos restringido a 700
[x] URLs Push protegidas a 600
[x] PostgreSQL .env protegido a 600 y fuera de Git
[ ] Escaneo Gitleaks del working tree
[ ] Escaneo Gitleaks del historial
[ ] Hallazgos reales resueltos o aceptados
[ ] Secret persistente Open WebUI definido
[ ] Procedimiento de rotación documentado para secretos críticos
[ ] Comprobación recurrente incorporada al auditor o a un script de seguridad
```