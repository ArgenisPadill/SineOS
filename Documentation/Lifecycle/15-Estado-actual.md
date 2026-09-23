# 15 — Estado actual de SineOS

**Checkpoint documental:** 23-09-2026

## Componentes validados

```text
Debian 13 / XFCE
Btrfs
Git + GitHub SSH
Podman rootless
PostgreSQL 18
Ollama
Qwen local
Open WebUI
Obsidian / Knowledge Vault
Miyo
Stirling PDF
Uptime Kuma
nftables
Proton VPN
DNSCrypt
NetworkPrivacy
auditor SineOS
configuración XFCE reproducible
monitoreo local
```

## Programas propios

```text
NetworkPrivacy
```

## Automatizaciones versionadas

```text
Scripts/Audit/sineos-audit.sh
Scripts/Desktop/sineos-xfce-macos.sh
Scripts/Monitoring/check-open-webui.sh
Scripts/Monitoring/check-postgresql.sh
Scripts/NetworkPrivacy/install-network-privacy.sh
Containers/stacks/postgres/Makefile
```

## Huecos de reproducibilidad detectados por esta guía

1. procedimiento exacto de particionado/instalación inicial de Debian;
2. verificación/documentación de LUKS;
3. instalación reproducible de Podman Desktop;
4. instalación reproducible completa de Obsidian;
5. instalación reproducible completa de Miyo;
6. unidades systemd de los timers de monitoreo aún no versionadas;
7. ruleset nftables operativo aún no versionado;
8. gestión formal de secretos;
9. backups y restore;
10. Disaster Recovery;
11. portabilidad del auditor;
12. hardening pendiente de Open WebUI;
13. revisión nftables/Podman/netavark;
14. auditoría AppArmor;
15. decisión final sobre Tor.

## Fuente de verdad

Para saber qué está realmente en el repositorio:

```bash
cd "$HOME/Workspace/SineOS"
git status
git log -1 --oneline --decorate
git ls-files | sort
```

Para comprobar el estado operativo:

```bash
systemctl --failed --no-pager
podman ps -a
nmcli connection show --active
sudo nft list ruleset
ss -tulpn
```

## Próximo ciclo

El siguiente avance debe cerrar huecos en este orden aproximado:

```text
inventario de programas/scripts locales no versionados
    ↓
recuperar timers y firewall como código
    ↓
gestión de secretos
    ↓
backup PostgreSQL + restore probado
    ↓
backup Knowledge Vault
    ↓
snapshots / recuperación
    ↓
Disaster Recovery
```

## Regla de actualización de esta guía

Cuando una etapa cambie, debe modificarse su archivo numerado y, si afecta el estado global, este documento.

La guía no debe convertirse en un registro histórico infinito; debe representar el camino vigente y reproducible para llegar al estado actual.