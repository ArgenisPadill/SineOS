# SineOS — Auditoría comparativa y remediación preliminar (02-11-2026)

**Alcance:** comparación del archivo aportado por el propietario, `SINEOS-AUDITORIA-MIGRACION.md`, con el código y los issues/PR accesibles por el conector GitHub. **No hubo acceso al host Debian ni a volúmenes, credenciales, Restic, imágenes desplegadas o Vault privado.**

**Baseline observado:** `main` en `791e2161b206fd356badf727c4e62fc09d853f7d`; PR #6 en `49654440`, #12 en `ad526cfc`, #13 en `a75f2ae3` durante esta revisión. Comprobar de nuevo antes del merge: las ramas pueden cambiar.

**Método:** tres perspectivas de revisión de código (Seguridad, Respaldo/Recuperación, QA y gobierno), sin afirmar ejecución de subagentes, acceso a servicios reales ni pruebas no realizadas. Las modificaciones de esta rama son propuestas pendientes de aceptación.

## Comparación y evidencias

| ID | Afirmación del archivo recibido | Confirmación/corrección independiente | Estado verificable |
| --- | --- | --- | --- |
| C01 | PR #12 y #13 preparan reconstrucción y verificaciones | Ambos están abiertos en Draft; sus archivos existen en sus ramas, no en main. | PASS de existencia; PENDING de integración |
| C02 | El PR #6 debe revisarse antes del merge | Sigue Draft y `mergeable=false` en el corte consultado; requiere revisión propia. | PENDING |
| C03 | Scanner de secretos/historial sin ejecución comprobada | Confirmado. Además, el script existente permitía falsos resultados por no comprobar explícitamente la salida exitosa de Gitleaks. | Corrección propuesta; escaneo PENDING |
| C04 | `backup_engine.py` usa Vault fijo | Confirmado en tres lugares operativos y en el layout de restore: fuentes, exclusiones, manifiesto y ruta del restore. | Corrección propuesta; prueba en host PENDING |
| C05 | Bootstrap con dry-run y Ollama sin hash fijado | Confirmado por inspección del script en PR #12. `sh -n` revisa sintaxis, **no autenticidad**. | PENDING |
| C06 | Cuatro imágenes sin digest remoto certificado | Confirmado en Compose/plantilla. No equiparar `Image ID` local con digest de manifest. | PENDING |
| C07 | PR #12/#13 solapan documentación | Ambos modifican `Documentation/README.md`. PR #13 crea referencias a materiales de #12. Merge #12 antes de #13, tras pruebas. | PENDING |
| C08 | Sin licencia, About y reporte privado decidido | `LICENSE` ausente en main; `SECURITY.md` solo está en PR #13. About y reporte privado dependen del propietario/configuración GitHub. | PENDING |
| C09 | Piloto Office sin ninguna copia restaurable | **Desactualizado**: el issue #9 registra dos respaldos validados por hashes y arranque aislado de Windows hasta inicio de sesión. Office en el clon y backup externo siguen pendientes. | PASS de evidencia histórica parcial; NO certificado |
| C10 | TD-024, TD-019, TD-006/007 abiertos | Confirmado por `Technical-Debt.md`. También persiste TD-025: rutas rígidas en el auditor general. | PENDING |
| C11 | Privacidad del README y enlace skills pendientes | PR #13 propone saneamiento; la API de GitHub confirmó existencia de `.agents/skills/` y cuatro carpetas. Navegación/renderizado web específico no probado. | PASS de existencia; PENDING privacidad global |
| C12 | Hacer squash y completar gates antes de fusionar | #12 contiene 12 commits y #13 contiene 11 en el corte consultado; ningún merge ejecutado. | PENDING |
| C13 | DR validado históricamente | `Disaster-Recovery.md` registra recuperación en Debian 13.7 (02-10-2026). **No acredita** un backup actual ni los nuevos cambios. | PASS histórico; migración nueva PENDING |
| C14 | Evidencia fuera de Git | El auditor general `Scripts/Audit/sineos-audit.sh` escribe en `Documentation/Audit` dentro del árbol del repositorio y recoge `git config --global --list`, `git remote -v`, journal y procesos. El contenido podría contener datos privados. No publicar ni ejecutar sin revisión de saneamiento. | Riesgo nuevo, PENDING |

## Cambios propuestos en esta rama (sin tocar main ni host)

1. **Respaldo:** `configured_vault_root()` exige `SINEOS_VAULT` definido, absoluto, existente y con `.obsidian`; se eliminan las referencias fijas al Vault en las fuentes, exclusiones, manifiesto y restauración. Fallo temprano antes de crear staging de PostgreSQL. El layout restaurado usa rutas efectivas de repositorio/Vault.
2. **Scanner:** Gitleaks distingue ejecución correcta, hallazgos y errores. Un JSON ausente/inválido o un código de salida inesperado ya no puede producir PASS. No sigue enlaces simbólicos al crear el snapshot escaneable; los marca como error. El historial solicita `--all --full-history` de las referencias **presentes en la clonación local**, no de todas las refs remotas que no se hayan descargado.
3. **QA:** `tests/test_backup_vault.py` propone casos de variable ausente, ruta relativa, Vault inválido, ruta no estándar, exclusiones y layout de restore. **La presencia de pruebas no equivale a ejecución exitosa.**

## Riesgos y puntos que NO se cierran con el PR

- **Validación de host:** ejecutar `python3 -m unittest discover -s tests -p 'test_backup_vault.py'`, `python3 -m py_compile Apps/Maintenance/backup_engine.py`, `bash -n Scripts/Security/sineos-secrets-audit.sh`, y Gitleaks en entorno local seguro con las evidencias fuera de Git. `shellcheck` del bootstrap de PR #12 y prueba `--dry-run` en Debian 13 siguen PENDING.
- **SINEOS_VAULT operativo:** antes de adoptar el cambio, asegurar que la variable se propague al proceso que ejecuta el backup (GUI, systemd, timer o cron); no asumir herencia de `.bashrc`. Guardar la configuración privada con permisos restrictivos y comprobar existencia sin imprimir la ruta. Ausencia de variable = aborto deliberado, no fallback.
- **Restore real:** el test unitario no sustituye Restic, comparación de manifiesto, pruebas de PostgreSQL con contraseña válida/inválida, estado persistente de los otros stacks ni rollback aislado.
- **Supply chain:** aprobar y verificar hash del instalador Ollama antes de ejecutarlo, o `--skip-ollama`; no inventar valores. Resolver digest de imagen desde el host y PR separado.
- **Gate Seguridad #2:** continúa abierto por AppArmor, nftables/netavark, LUKS, Ollama, SSH si corresponde, rotación, snapshots, TD-018 y otras deudas. No saltar a SDE físico.
- **SineOS Office:** sigue congelado; no toca `./storage`, `./shared`, VM, contraseñas ni Samba. La prueba de VM parcial no acredita Office recuperado.

## Comandos de comprobación de privacidad (en estación autorizada, sin publicar salida)

```bash
python3 -m unittest discover -s tests -p 'test_backup_vault.py'
python3 -m py_compile Apps/Maintenance/backup_engine.py
bash -n Scripts/Security/sineos-secrets-audit.sh
# Requiere Gitleaks y referencias Git locales completas; genera reportes privados:
bash Scripts/Security/sineos-secrets-audit.sh
# El siguiente comando imprime SOLO nombres de variables, nunca valores:
awk -F= '/^[A-Z][A-Z0-9_]*=/{print $1}' Containers/stacks/postgres/.env.example
```

**No utilizar `git log -p | grep password` del archivo original:** podría mostrar contraseñas de commits históricos. Mantener informes de detección redactados y privados. Si aparece una credencial real, rotarla y evaluar limpieza del historial; borrar HEAD no revoca una credencial expuesta.

## Evidencia, reversión y criterio de aceptación

| Área | Prueba | Resultado | Evidencia | Rollback |
| --- | --- | --- | --- | --- |
| Revisión estática de código GitHub | Existencia de PR/rutas y referencias fijas | PASS (inspección) | Enlaces del repositorio, SHA anteriores | Ninguno; solo lectura |
| Código de backup modificado | Inspección textual y cambios versionados | PASS de preparación, **PENDING ejecución** | Diff privado del PR | Revertir commit(s) en rama o cerrar PR; no afectar main |
| Gitleaks endurecido | Inspección textual | PASS de preparación, **PENDING ejecución** | Diff del PR | Revertir commit(s) o cerrar PR |
| Pruebas unitarias | Archivo agregado; sin runner conectado | PENDING | A generar fuera de Git | Revertir commit de pruebas |
| Servicios y migración | No se accedió al host | PENDING | A producir tras autorización | Conservar host origen y snapshot comprobado |

**Criterio de salida:** el propietario revisa diff, confirma configuración real de `SINEOS_VAULT`, ejecuta tests y Gitleaks, prueba snapshot/restore aislados y acepta riesgos por escrito. Hasta ese momento: **NO certificar migración, NO cerrar gate #2, NO fusionar automáticamente y NO cambiar roadmap**.

**Referencias:** [gate de Seguridad #2](https://github.com/ArgenisPadill/SineOS/issues/2), [roadmap #4](https://github.com/ArgenisPadill/SineOS/issues/4), [Office #9](https://github.com/ArgenisPadill/SineOS/issues/9), [PR #6](https://github.com/ArgenisPadill/SineOS/pull/6), [PR #12](https://github.com/ArgenisPadill/SineOS/pull/12), [PR #13](https://github.com/ArgenisPadill/SineOS/pull/13).
