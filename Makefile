PROJECT_NAME ?= todolistapi

DEV_PROJECT := $(PROJECT_NAME)-dev

DEV_COMPOSE_FILE := docker/dev/docker-compose.yml

INFO := @bash -c 'echo "=> $$1";' VALUE

# Get an exit code of a docker-compose task
INSPECT := $$(docker-compose -p $$1 -f $$2 ps -q $$3 | xargs -I ARGS docker inspect -f "{{ .State.ExitCode }}" ARGS)

# Check if docker compose test run successfully
CHECK := @bash -c '\
  if [[ $(INSPECT) -ne 0 ]]; \
  then exit $(INSPECT); fi' VALUE

.PHONY: test devserver clean

test:
	${INFO} "Pulling latest images..."
	@ docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) pull
	${INFO} "Building images..."
	@ docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) build --pull app
	${INFO} "Waiting while database is ready..."
	@ docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) run --rm db_probe
	${INFO} "Running tests..."
	@ docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) up app
	${CHECK} $(DEV_PROJECT) $(DEV_COMPOSE_FILE) app
	${INFO} "Testing completed"

devserver:
	${INFO} "Pulling latest images..."
	@ docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) pull
	${INFO} "Building images..."
	@ docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) build --pull app
	${INFO} "Waiting while database is ready..."
	@ docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) run --rm db_probe
	${INFO} "Running server..."
	@ docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) run --rm -p 8000:8000 app sh
	${CHECK} $(DEV_PROJECT) $(DEV_COMPOSE_FILE) app
	${INFO} "Done"

clean:
	${INFO} "Cleaning environment..."
	@ docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) down -v
	@ docker images -q -f dangling=true -f label=application=$(PROJECT_NAME) | xargs -I ARGS docker rmi -f ARGS
	${INFO} "Clean complete"
