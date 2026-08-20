STACK_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

COMPOSE := podman-compose -f $(STACK_DIR)compose.yaml --env-file $(STACK_DIR).env

.PHONY: help config pull up down restart ps logs health

help:
	@echo "SineOS PostgreSQL"
	@echo
	@echo "Targets:"
	@echo "  make config   Validar configuración"
	@echo "  make pull     Descargar/actualizar imagen"
	@echo "  make up       Crear e iniciar PostgreSQL"
	@echo "  make down     Detener y eliminar contenedor"
	@echo "  make restart  Reiniciar PostgreSQL"
	@echo "  make ps       Mostrar estado"
	@echo "  make logs     Mostrar logs"
	@echo "  make health   Consultar healthcheck"

config:
	$(COMPOSE) config

pull:
	$(COMPOSE) pull

up:
	@container="$$(sed -n 's/^POSTGRES_CONTAINER_NAME=//p' $(STACK_DIR).env | head -n1)"; \
	container="$${container:-sineos-postgres}"; \
	if podman container exists "$$container"; then \
		if [ "$$(podman inspect "$$container" --format '{{.State.Status}}')" = "running" ]; then \
			echo "PostgreSQL ya está ejecutándose: $$container"; \
		else \
			echo "Iniciando contenedor existente: $$container"; \
			podman start "$$container"; \
		fi; \
	else \
		$(COMPOSE) up -d; \
	fi

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) restart

ps:
	$(COMPOSE) ps

logs:
	$(COMPOSE) logs --tail=100

health:
	@container="$$(sed -n 's/^POSTGRES_CONTAINER_NAME=//p' $(STACK_DIR).env | head -n1)"; \
	container="$${container:-sineos-postgres}"; \
	podman inspect "$$container" \
		--format 'Status={{.State.Status}} Health={{.State.Health.Status}}'
