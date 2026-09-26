# Programas propios de SineOS

Este directorio contiene programas creados específicamente para resolver necesidades de SineOS.

Un programa propio no es equivalente a un script auxiliar. Puede tener interfaz, estado persistente, integración con el escritorio, lógica operativa y un ciclo de instalación/actualización propio.

## Catálogo actual

| Programa | Tecnología | Estado | Propósito | Documentación |
|---|---|---|---|---|
| NetworkPrivacy | Python 3 + GTK3/PyGObject | Operativo | Administrar DNSCrypt por perfil, detectar Proton VPN y restaurar DNS original | `Documentation/Operations/NetworkPrivacy.md` |
| Maintenance | Python 3 + GTK3/PyGObject | Operativo | Coordinar salud trimestral, respaldo externo certificado, validaciones, recordatorios y sincronización segura con GitHub | `Documentation/Operations/Maintenance.md` |

## NetworkPrivacy

Archivos:

```text
Apps/NetworkPrivacy/
├── sineos-network-privacy.py
└── network_policy.py
```

`sineos-network-privacy.py` implementa la interfaz GTK3 y la experiencia de usuario.

`network_policy.py` contiene la lógica para leer, modificar, validar y restaurar la política DNS mediante NetworkManager.

La instalación e integración con XFCE se realiza desde:

```text
Scripts/NetworkPrivacy/install-network-privacy.sh
```

## Regla

Todo futuro programa creado específicamente para SineOS debe registrarse en este archivo y cumplir, cuando corresponda:

- `Documentation/Architecture/Native-Applications.md`;
- `Documentation/Architecture/Documentation-Standard.md`;
- política de seguridad y privacidad documental;
- instalador o procedimiento reproducible;
- validación funcional;
- actualización y desinstalación;
- rollback o recuperación cuando la función pueda alterar el sistema.

## Software externo

Ollama, Open WebUI, Miyo, PostgreSQL, Stirling PDF, Uptime Kuma, Podman y Obsidian forman parte de SineOS, pero no son programas desarrollados por SineOS. Su configuración e integración sí forman parte del proyecto.