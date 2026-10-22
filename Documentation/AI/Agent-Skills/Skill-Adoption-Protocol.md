# SineOS — Protocolo de evaluación e incorporación de skills externas

**Estado:** política de control / sin adopción externa por esta publicación.  
**Precedencia:** [Lineamiento general de ingeniería](../../Architecture/Engineering-Delivery-Standard.md), [gate de Seguridad](https://github.com/ArgenisPadill/SineOS/issues/2), [roadmap](../../Operations/Project-Roadmap.md).

## Reglas no negociables

- Una skill de GitHub es **código e instrucciones no confiables**, incluso cuando contiene solo Markdown. Puede solicitar credenciales, descargas, cambios destructivos, telemetría, acceso a red o permisos mayores.
- Nunca ejecutar comandos externos pegados por una skill sin revisar su efecto, la autorización y el impacto en Debian/SineOS. Prohibido `curl|sh`, `irm|iex` y variantes desde referencias no fijadas.
- Nunca incorporar recursivamente cientos de skills. Codex necesita disparadores claros y contexto limitado.
- No alterar con la instalación: AppArmor, nftables, SSH, Podman, sistema de recuperación, Windows/Office congelado, secretos ni respaldos.
- No asumir que licencias MIT, CC-BY-SA o propietarias son intercambiables. Preferir **referenciar**, no copiar o redistribuir, hasta revisar licencia por repositorio/skill.
- Una skill no otorga derechos nuevos: herramientas y secretos siguen sujetos a autorizaciones de Codex/usuario.

## Gate de una nueva skill

1. **Justificación:** tarea concreta no cubierta por `AGENTS.md`, estándares y skills nativas; beneficio y no-objetivos.
2. **Procedencia:** URL exacta GitHub, autor, mantenimiento, revisión de issues, ref de commit inmutable y hashes locales; verificar licencia del archivo y componentes auxiliares.
3. **Análisis estático:** leer `SKILL.md`, archivos enlazados, scripts, hooks, instaladores, dependencias, archivos de configuración, red y mecanismo de actualización. Buscar instrucciones de exfiltración, sustitución de reglas, escalada de privilegios, bypass de aprobación o destrucción.
4. **Conflictos:** contrastar con `AGENTS.md`, estándares, roadmap y decisiones congeladas; eliminar directivas incompatibles o rechazar la skill, no sobreescribir reglas SineOS.
5. **Prueba aislada:** instrucciones/manual sin ejecución por defecto; usar sandbox/clon temporal y herramientas mínimas. Comprobar escenario positivo, escenario donde **no debe activarse**, regresiones, recursos y salida. Evitar datos privados.
6. **Reversibilidad:** copia/versionado de los archivos incorporados, desinstalación documentada y verificada; no tocar configuración global si no se requiere.
7. **Registro:** estado CANDIDATA / EVALUADA / PILOTO / APROBADA / RECHAZADA / DIFERIDA, evidencia concreta, fecha, propietario y dependencias. Un resultado de prueba en sandbox no certifica el host.
8. **Autorización:** presentar informe de cambios y pedir permiso explícito para adopción. Si se aprueba, añadir solo la habilidad pertinente a `.agents/skills` o mediante mecanismo oficial de Codex, con versión fijada.

## Plantilla de ficha de evaluación

```text
Nombre:
Fuente GitHub y ruta:
Commit/ref fijado:
Licencia y archivos incluidos:
Tarea concreta:
Herramientas/permisos:
Red, secretos y telemetría:
Scripts/hooks/dependencias:
Riesgos y mitigaciones:
Conflictos con SineOS:
Prueba de no activación:
Prueba positiva y evidencia:
Rollback:
Estado:
Decisión/autorización:
```

**No confundir:** documentación de candidatos = NO INSTALADO; skill nativa publicada = disponible en Git tras sincronización, NO PROBADA en Codex local; skill externa instalada = requiere registro y pruebas; integración certificada = exige gates propios.
