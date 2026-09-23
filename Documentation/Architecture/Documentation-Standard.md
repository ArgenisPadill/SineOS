# SineOS — Estándar de documentación

**Decisión congelada:** 23-09-2026  
**Estado:** Adoptado

## Propósito

SineOS debe poder comprenderse y reconstruirse sin depender de la memoria de quien lo configuró.

La documentación forma parte del sistema, no es un complemento opcional.

## Principio

> Si una configuración no puede reconstruirse o explicarse leyendo el repositorio, todavía no está completamente integrada en SineOS.

## Capas documentales

### Architecture

Responde principalmente:
- ¿por qué existe este componente?;
- ¿por qué se eligió esta solución?;
- ¿cómo se relaciona con el resto del sistema?;
- ¿qué decisiones y límites de diseño existen?

### Operations

Responde principalmente:
- ¿cómo se instala?;
- ¿cómo se usa?;
- ¿cómo se inicia y detiene?;
- ¿cómo se valida?;
- ¿cómo se actualiza?;
- ¿cómo se diagnostica?;
- ¿cómo se desinstala o revierte?

### Security

Responde:
- ¿qué riesgos existen?;
- ¿qué controles están implementados?;
- ¿qué privilegios requiere?;
- ¿qué secretos maneja?;
- ¿qué exposición de red tiene?;
- ¿qué falta endurecer?

### Recovery

Responde:
- ¿qué debe respaldarse?;
- ¿cómo se restaura?;
- ¿cómo se migra?;
- ¿cómo se reconstruye después de una pérdida?

Recovery solo debe documentarse como procedimiento cuando haya sido probado razonablemente.

## Definition of Done documental

Un componente estable de SineOS debe cubrir, cuando aplique:

```text
Propósito / justificación
Arquitectura
Dependencias
Instalación
Configuración
Uso normal
Estado y validación
Actualización
Troubleshooting
Seguridad
Backup
Restore / rollback
Desinstalación
Limitaciones
Deuda técnica
```

No todos los componentes necesitan una sección independiente para cada punto, pero la información no debe quedar únicamente en la memoria o en una conversación.

## Código y documentación deben coincidir

Los documentos deben representar el estado real del repositorio y del sistema validado.

Debe evitarse:
- describir directorios inexistentes como si estuvieran implementados;
- documentar servicios no desplegados como activos;
- mantener rutas personales en documentación pública;
- declarar terminado un control no validado;
- conservar instrucciones históricas incompatibles con el estado actual.

## Procedimientos no probados

Una idea, plan o propuesta no debe presentarse como procedimiento confirmado.

Debe marcarse como:
- pendiente;
- propuesta;
- deuda técnica;
- experimento;
- no validado.

## Comandos

Los comandos publicados deben tener contexto.

Debe quedar claro:
- desde qué directorio se ejecutan;
- con qué usuario;
- si requieren `sudo`;
- qué modifican;
- cómo verificar el resultado.

Los comandos destructivos o difíciles de revertir requieren advertencia y, cuando exista, rollback.

## Dependencias

Las dependencias relevantes deben documentarse usando nombres de paquete o herramientas reales.

Si una versión concreta es necesaria, debe registrarse.

## Estado

Los documentos operativos deben distinguir entre:
- operativo;
- validado;
- experimental;
- pendiente;
- retirado;
- deuda técnica.

## Documentación de aplicaciones

Las aplicaciones propias siguen además:

`Documentation/Architecture/Native-Applications.md`

## Documentación de scripts

Los scripts siguen además:

`Documentation/Architecture/Script-Standard.md`

y deben figurar en:

`Scripts/README.md`

## Privacidad documental

Todo contenido público debe respetar:

`Documentation/Security/Documentation-Privacy.md`

Antes de publicar se revisan secretos, tokens, credenciales, rutas personales innecesarias, direcciones privadas específicas, identificadores de dispositivos y logs.

## Índice

Todo documento estable debe poder localizarse desde:

`Documentation/README.md`

Un documento técnicamente correcto pero imposible de encontrar también constituye deuda documental.

## Regla de mantenimiento

Cuando un cambio modifica el comportamiento real de un componente, debe revisarse su documentación en el mismo bloque de trabajo o registrarse explícitamente la deuda generada.

## Criterio final

La documentación de SineOS debe permitir que una persona técnicamente competente pueda responder:

1. ¿Qué es esto?
2. ¿Por qué existe?
3. ¿Cómo se instala?
4. ¿Cómo se usa?
5. ¿Cómo sé que funciona?
6. ¿Qué puede romper?
7. ¿Cómo lo actualizo?
8. ¿Cómo lo recupero?
9. ¿Qué riesgos o secretos maneja?
10. ¿Qué sigue pendiente?

Si las respuestas dependen exclusivamente de recordar una conversación pasada, la documentación todavía está incompleta.