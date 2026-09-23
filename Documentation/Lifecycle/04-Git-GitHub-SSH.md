# 04 — Git, GitHub y SSH

**Estado:** VALIDADO

## Instalar herramientas

```bash
sudo apt update
sudo apt install -y git openssh-client
```

## Crear clave dedicada

Usar una clave dedicada para SineOS:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_sineos -C "SineOS"
```

Proteger la clave con passphrase.

## Configuración SSH

Editar `~/.ssh/config` y mantener una entrada equivalente a:

```text
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_sineos
    IdentitiesOnly yes
```

Después:

```bash
chmod 600 ~/.ssh/config
cat ~/.ssh/id_ed25519_sineos.pub
```

Agregar únicamente la clave pública a GitHub.

## Cargar en ssh-agent

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_sineos
ssh-add -l
```

## Validar GitHub

```bash
ssh -T git@github.com
```

La respuesta correcta confirma autenticación aunque GitHub no proporcione shell.

## Clonar SineOS

```bash
mkdir -p ~/Workspace
git clone git@github.com:ArgenisPadill/SineOS.git ~/Workspace/SineOS
cd ~/Workspace/SineOS
git status
```

## Sincronización segura

```bash
git fetch origin
git status
git pull --ff-only origin main
```

Se evita `reset --hard`, `clean`, force-push o rebase automático sin revisar primero el estado local.