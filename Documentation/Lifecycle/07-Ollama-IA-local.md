# 07 — Ollama e IA local

**Estado:** VALIDADO

## Papel en SineOS

Ollama ejecuta modelos locales. No es memoria, Knowledge Vault ni índice semántico.

Versión validada durante la construcción:

```text
Ollama 0.34.0
```

## Instalación

El mecanismo oficial utilizado para Linux es:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Este instalador obtiene la versión disponible en ese momento; por ello no debe confundirse con una instalación reproducible fijada a `0.34.0`.

Registrar siempre la versión obtenida:

```bash
ollama --version
```

## Modelos seleccionados

```bash
ollama pull qwen3.5:2b
ollama pull qwen2.5-coder:3b-instruct
ollama list
```

Los pesos de los modelos no se almacenan en Git.

## Servicio

La arquitectura validada usa un servicio `systemd --user`.

Comprobar:

```bash
systemctl --user status ollama --no-pager
```

## Acceso desde contenedores

Se configuró un override con:

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

Crear/editar override:

```bash
systemctl --user edit ollama
```

Después:

```bash
systemctl --user daemon-reload
systemctl --user restart ollama
systemctl --user status ollama --no-pager
```

## Validar API

```bash
ss -ltn | grep ':11434'
curl -s http://127.0.0.1:11434/api/tags | jq .
```

## Seguridad

Ollama escucha en todas las interfaces para permitir el acceso desde contenedores rootless mediante `host.containers.internal`. Esa decisión depende del firewall nftables para impedir exposición no deseada.

Por ello no debe configurarse esta escucha antes de tener claro el modelo de red de SineOS.

## Validación de modelo

```bash
ollama run qwen3.5:2b "Responde únicamente: SineOS OK"
```

## Decisión de hardware

En el equipo actual se priorizan modelos pequeños y CPU. Las pruebas con la GPU Intel Iris Xe no justificaron forzar aceleración Vulkan.

## Documentación

`Documentation/Operations/Ollama.md`