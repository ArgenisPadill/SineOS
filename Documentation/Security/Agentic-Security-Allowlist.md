# SineOS — Allowlist inicial de skills defensivas

**Estado:** PROPUESTA INICIAL  
**Fuente revisada:** `mukul975/Anthropic-Cybersecurity-Skills@54a798831d2266a3ca61ce68a7acb80b81160d57`

Esta lista define el conjunto inicial de skills que SineOS puede evaluar durante la fase final de seguridad.

No implica que todas sus instrucciones se ejecuten automáticamente.

## Nivel A — Prioridad SineOS

| Skill | Uso previsto | Modo inicial |
|---|---|---|
| `hardening-linux-endpoint-with-cis-benchmark` | Comparar el host Linux contra controles de hardening | Evaluación/lectura; remediación manual |
| `performing-container-security-scanning-with-trivy` | Escanear imágenes, filesystem y configuración de contenedores | Lectura/scan |
| `implementing-secret-scanning-with-gitleaks` | Comprobar secretos en Git e historial | Lectura/scan |
| `validating-backup-integrity-for-recovery` | Verificar que los backups sean recuperables | Validación controlada |
| `validating-tpm-measured-boot-attestation` | Evaluar TPM/measured boot si el hardware lo soporta | Lectura primero |
| `generating-and-analyzing-sboms` | Inventario de dependencias y supply-chain | Lectura/generación local |
| `analyzing-linux-audit-logs-for-intrusion` | Evaluar telemetría/auditd y capacidad de investigación | Lectura |
| `triaging-security-incident-with-ir-playbook` | Definir proceso de triage e incident response | Procedimiento/documentación |

## Nivel B — Candidatas posteriores

- scanning de imágenes con Trivy/Grype;
- detección de container drift/escape;
- vulnerability prioritization;
- network traffic analysis;
- supply-chain analysis;
- ransomware recovery testing;
- Secure Boot analysis;
- LLM/agent security y guardrails.

Se incorporan al flujo estable solamente después de revisar dependencias, alcance y compatibilidad con Debian/Podman.

## Exclusiones automáticas

No se habilitan automáticamente skills cuyo objetivo primario sea:

- explotación;
- persistencia ofensiva;
- credential dumping;
- phishing ofensivo;
- Command and Control;
- evasión de defensas;
- movimiento lateral;
- exfiltración;
- container escape ofensivo;
- bypass de controles.

Su existencia en la biblioteca puede ser útil para threat modeling y comprensión defensiva, pero su ejecución requiere una tarea explícita, autorizada y separada.

## Compatibilidad

Una skill del upstream puede asumir Ubuntu, RHEL, Docker, Kubernetes, Splunk u otras tecnologías que SineOS no utiliza.

Por eso ningún comando upstream se copia automáticamente al sistema.

Ejemplo importante: la skill de CIS Linux incluye recomendaciones genéricas como deshabilitar servicios. SineOS conserva servicios como Avahi cuando existe una razón funcional; la recomendación debe contrastarse con el diseño real.

## Regla

> La allowlist selecciona conocimiento que el agente puede consultar; no concede autorización automática para ejecutar todos los comandos contenidos en la skill.