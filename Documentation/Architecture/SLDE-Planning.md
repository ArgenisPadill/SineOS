# SineOS Laboratory & Development Environment (SLDE) — Planeación inicial

**Decisión:** 08-10-2026
**Estado:** PLANIFICADO / NO IMPLEMENTADO / BLOQUEADO POR SEGURIDAD, SDE Y CONSOLIDACIÓN POST-SDE.
**Issue:** [#3 SLDE](https://github.com/ArgenisPadill/SineOS/issues/3)
**Roadmap maestro:** [Project-Roadmap](../Operations/Project-Roadmap.md)

## Objetivo y límites

SLDE será un subsistema opcional de herramientas de ingeniería, investigación, docencia, desarrollo y laboratorios. **No es SDE** y no reemplaza SineOS Core. Integrar una herramienta significa poder ofrecerla, detectarla, gestionarla y recuperarla, **no** instalarla ni ejecutarla permanentemente.

La fase actual se limita a inventario y planeación. No crear aún directorios `Modules/`, `Labs/` ni `Apps/LaboratoryManager/` vacíos; incorporarlos solo con artefactos funcionales.

## Arquitectura propuesta

- **SineOS Core:** Debian 13/XFCE, seguridad, backups/Restic, snapshots, Mantenimiento, Podman, monitoreo.
- **SDE:** experiencia visual y escritorio, independiente del catálogo SLDE.
- **SLDE:** catálogo, manifiestos, perfiles por recursos, orquestación de instaladores, comprobaciones de salud, limpieza y recuperación.
- **Ejecución nativa:** aplicaciones ligeras/GUI, toolchains, CLI vía repositorios confiables de Debian u opciones verificadas.
- **Podman rootless:** stacks compatibles de servicios bajo demanda, sin exponer puertos a LAN por defecto.
- **VM aislada QEMU/KVM:** redes privilegiadas, routers, Active Directory, hipervisores de práctica, pruebas ofensivas autorizadas, Kubernetes cuando proceda.
- **Servidor externo/remoto:** Ceph real, Proxmox real, múltiples nodos, cargas de IA/GPU y monitoreo grande.
- **No duplicar:** reutilizar PostgreSQL, Ollama y otras instalaciones existentes, tras inventariar sus versiones, puertos y datos.

La plataforma de referencia es la Gateway GWTN141-10 (Intel i5-1135G7, 16 GB RAM, Intel Iris Xe, SSD 512 GB). Los presupuestos de CPU/RAM/disco de SLDE deberán **medirse**; no hay consumo certificado por módulo.

## Inventario congelado del alcance propuesto

| # | Dominio | Herramientas/capacidades propuestas | Estrategia inicial |
|---|---|---|---|
| 01 | Redes | GNS3, Containerlab, Mininet, Wireshark, nmap, BIND, DHCP, VPN, OPNsense | Herramientas ligeras locales; emulación y redes privilegiadas en VM aislada |
| 02 | Sistemas operativos | Plantillas VM, Samba AD, FreeIPA, systemd, kernel, snapshots | VM QEMU/KVM; evitar alterar dominio, autenticación o kernel del host |
| 03 | Bases de datos | PostgreSQL, MySQL, MongoDB, Redis, DBeaver, pgAdmin, réplicas | PostgreSQL existente; adicionales optativos rootless; clientes locales |
| 04 | Desarrollo | Python, Java, C/C++, JavaScript/Node, Go, Rust, VS Code, JetBrains, Git | Local con versiones/entornos por proyecto |
| 05 | Ingeniería de software | Redmine, Taiga, OpenProject, PlantUML, Mermaid, Kanban | Diagramación local; gestores como stacks bajo demanda |
| 06 | Ciberseguridad | Metasploit, Burp, ZAP, OpenVAS/Greenbone, Wazuh, DVWA, Juice Shop | VM/laboratorios autorizados, aislados, sin atacar terceros |
| 07 | Cloud y DevOps | k3s, MicroK8s, Helm, Terraform, Ansible, LocalStack, Prometheus, Grafana | CLI local; control planes/servicios en VM o remoto bajo demanda |
| 08 | Virtualización y servidores | Proxmox, Ceph, MinIO, Nextcloud, Jellyfin, Gitea | Proxmox/Ceph en laboratorio remoto/dedicado; otros optativos |
| 09 | Matemáticas y estadística | Jupyter, NumPy, pandas, R, Octave, Maxima, LaTeX | Entornos locales separados |
| 10 | Electrónica y hardware | Arduino, KiCad, Fritzing, ESP32, Raspberry Pi, IoT | Editores locales; placas externas cuando correspondan |
| 11 | Ofimática | LibreOffice, OnlyOffice, Zotero, OCR | Escritorio local; OnlyOffice servidor opcional |
| 12 | Comunicación | Matrix, Jitsi, Mumble, Wiki.js, BookStack | Clientes nativos; servidores optativos y preferentemente remotos |
| 13 | Ciencia de datos | pandas, Polars, scikit-learn, PyTorch, Spark, MLflow, Airflow, Superset, LLMs, RAG | Local ligero; clústeres/entrenamiento pesado remoto |
| 14 | Procesamiento de imágenes | OpenCV, YOLO, MMDetection, SAM, CVAT, Stable Diffusion, MONAI, Open3D, TensorRT | Pruebas CPU pequeñas; GPU remota cuando sea necesaria |
| 15 | Certificaciones | LPIC, CCNA, AWS, Azure, CompTIA, TensorFlow, Databricks | Contenido, simuladores, seguimiento y laboratorios por demanda |
| 16 | IA local | Ollama, LocalAI, Whisper, LangChain, Qdrant, ComfyUI | Mantener Ollama existente; agregar componentes optativos según RAM/GPU |

**Reutilización entre dominios:** pandas sirve a 09/13; Python a 04/09/13/14; PostgreSQL a 03/07; Ollama a 13/16; Wireshark a 01/06. No se crean instalaciones paralelas por cada módulo.

## Reglas técnicas y de seguridad

1. **Ninguna instalación automática antes del gate Seguridad → SDE.** El simple registro de SLDE no añade paquetes, contenedores, bridges o servicios.
2. Usar componentes compatibles con Debian 13 y documentar licencias, fuente confiable, versiones y compatibilidad.
3. Privilegios mínimos: no forzar Podman rootless para Containerlab/Mininet si la tecnología necesita administración de red. Ejecutar en VM de laboratorio; no elevar permanentemente el host.
4. Segregar redes de laboratorio y tráfico de prácticas del host productivo; preservar nftables, VPN, DNSCrypt y NetworkManager.
5. Por defecto usar loopback para puertos de servicio; exposiciones LAN explícitas, revisadas y limitadas por política.
6. Laboratorios de seguridad exclusivamente en objetivos propios/autorizados; DVWA/Juice Shop no deben exponerse fuera de entornos controlados.
7. No transformar el host Debian/XFCE en Proxmox; Ceph y clústeres requieren dimensionamiento y preferentemente nodos dedicados.
8. MicroK8s es candidato catalogado, **no recomendado por defecto** dado que SineOS evita Snap. Evaluar k3s sobre VM o remoto.
9. TensorRT necesita hardware/ecosistema NVIDIA compatible; la GPU Intel Iris Xe no cumple ese perfil local. No presentar como disponible sin entorno compatible.
10. Python, Node y otros SDK usan entornos aislados por proyecto; evitar romper dependencias de sistema.
11. Aplicar cuotas/alertas de RAM, disco y CPU y desactivar recursos temporales fuera de uso; evitar «16 módulos residentes».
12. Guardar datos y secretos fuera de Git; manifests y `.env.example` nunca contienen secretos. Incorporar backup/restore según criticidad.
13. La desinstalación limpia conserva datos hasta decisión explícita del usuario; debe existir rollback documentado y verificado.
14. No certificar instalaciones, beneficios ni requisitos de rendimiento sin pruebas del equipo real.

## Futuro LaboratoryManager (conceptual, no construido)

- Catálogo de herramientas con búsqueda, categoría, estado y dependencias.
- Detectar instalación existente, evitar conflictos y duplicaciones.
- Preparar plan de instalación con vista previa de paquetes, servicios, privilegios, puertos, consumo estimado y ruta de datos.
- Instalar sólo bajo aprobación explícita; verificar integridad/fuente.
- Iniciar/detener servicios bajo demanda y detectar fallos.
- Mostrar CPU/RAM/disco/puertos reales, consumo del módulo y compatibilidad.
- Exportar/importar manifiestos para laboratorios reproducibles.
- Actualización/version pin, snapshot o respaldo previo a cambios de riesgo.
- Desinstalar, revertir y limpiar archivos temporales de forma controlada.
- Reportar fallos en logs privados con datos sensibles saneados.

### Contrato mínimo por herramienta

En la implementación futura, cada ficha/manifiesto declarará: `id`, `version`, `module`, `source`, `license`, `execution_mode`, `dependencies`, `privileges`, `ports`, `volumes`, `resource_limits`, `install`, `validate`, `start`, `stop`, `backup`, `restore`, `uninstall`, `rollback` y `tested_on`. Es un **borrador** de esquema, todavía sin formato definitivo.

## Prioridad de entrega (después de SDE y reproducibilidad)

- **SLDE-0:** especificación, manifiesto, seguridad, perfiles de recursos y diseño del gestor.
- **SLDE-1:** MVP de catálogo y un módulo piloto de baja complejidad, con validación y desinstalación reales.
- **SLDE-2:** módulos 04, 09, 11, 15.
- **SLDE-3:** módulos 03, 05, 12.
- **SLDE-4:** módulos 01, 02, 06, 07, 08, 10 con VM/red aislada y autorización.
- **SLDE-5:** módulos 13, 14, 16 con limitación/medición de recursos y posible cómputo remoto.

## Criterio de aceptación por herramienta

- [ ] Requisitos y compatibilidad verificables.
- [ ] Instalación opcional, reproducible e idempotente.
- [ ] Privilegios, puertos y redes revisados.
- [ ] Recursos limitados, medidos y observables.
- [ ] Prueba funcional aislada y evidencia versionada sin secretos.
- [ ] Persistencia/restauración cuando proceda.
- [ ] Reversión y desinstalación sin romper SineOS Core o SDE.
- [ ] Documentación, troubleshooting y estado «validado» sólo después de pruebas.

**Regla final:** primero seguridad; luego escritorio SDE; después catálogo modular. La propuesta SLDE no reabre ni modifica el alcance congelado de SDE 1.0.
