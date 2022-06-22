## Variables used in target commands
SHELL := /bin/bash
ENV ?= Local
SETTINGS ?= $(shell echo $(ENV) | tr '[:upper:]' '[:lower:]')
DBUSER ?= user
DBPASSWORD ?= password
HOST ?= "127.0.0.1"

## Variables to make targets more readable
COMMAND = docker exec -i django-app bash -c
MANAGE = python manage.py
DOCKER_FILE = docker-compose -f ./Docker/${ENV}/docker-compose.yml
SETTINGS_FLAG = --settings=Project.settings.django.${SETTINGS}_settings
TEST_SETTINGS = SETTINGS=test
PING_DB = docker exec database mysqladmin --user=${DBUSER} --password=${DBPASSWORD} --host ${HOST} ping

## Settings used in target commands
IGNORE_WARNINGS = -W ignore::django.utils.deprecation.RemovedInDjango41Warning
PYTEST_SETTINGS = --reuse-db --ds=Project.settings.django.test_settings ${IGNORE_WARNINGS} -p no:cacheprovider
COVERAGE_SETTINGS = --cov --cov-config=.coveragerc
COVERAGE_WITH_HTML_SETTINGS = ${COVERAGE_SETTINGS} --cov-report=html
BLACK_SETTINGS = --config="./Project/settings/pyproject.toml"
ISORT_SETTINGS = --settings-path="./Project/settings/pyproject.toml"
BLACK_LOCAL_SETTINGS = --config="./App/Project/settings/pyproject.toml"
ISORT_LOCAL_SETTINGS = --settings-path="./App/Project/settings/pyproject.toml"
STYLE = {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2} ## Prints the target in a nice format


.PHONY: all
all: ## Main command, just needed to type `make`. Is equivalent to `make up`.
	@make up

.PHONY: help
help:	## Show this help which show all the possible make targets and its description.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / ${STYLE}' $(MAKEFILE_LIST)

.PHONY: up
up: ## Start the containers running the app.
	@${DOCKER_FILE} up

.PHONY: upd
upd: ## Start the containers detached.
	@${DOCKER_FILE} up -d

.PHONY: ps
ps: ## Show the containers status.
	@${DOCKER_FILE} ps

.PHONY: stop
stop: ## Stop the containers.
	@${DOCKER_FILE} stop

.PHONY: bash
bash: ## Open a bash shell in the django container.
	@${DOCKER_FILE} exec app /bin/bash

.PHONY: shell
shell: ## Open the shell_plus of django. You can modify the environment with SETTINGS parameter.
	@${COMMAND} "${MANAGE} shell_plus ${SETTINGS_FLAG}"

.PHONY: migrate
migrate: ## Creates and applies the django migrations. You can modify the environment with SETTINGS parameter.
	@${COMMAND} "${MANAGE} makemigrations ${SETTINGS_FLAG}"
	@${COMMAND} "${MANAGE} migrate ${SETTINGS_FLAG}"

.PHONY: populate
populate: ## Populates the database with dummy data. You can modify the number of instances created with INSTANCES parameter.
ifeq (${INSTANCES},)
	@${COMMAND} "${MANAGE} populate_db -i 50 ${SETTINGS_FLAG}"
else
	@${COMMAND} "${MANAGE} populate_db -i $(INSTANCES) ${SETTINGS_FLAG}"
endif

.PHONY: flush
flush: ## Flush the database. You can modify the environment with SETTINGS parameter.
	@${COMMAND} "${MANAGE} flush ${SETTINGS_FLAG}"

.PHONY: show_urls
show_urls: ## Show the urls of the app. You can modify grep a string with GREP parameter.
ifeq (${GREP},)
	@${COMMAND} "${MANAGE} show_urls"
else
	@${COMMAND} "${MANAGE} show_urls | grep ${GREP}"
endif

.PHONY: recreate
recreate: ## Recreate the the database with dummy data.
	@make flush
	@make migrate
	@make populate

.PHONY: create-test-db
create-test-db: ## Create a test database.
	@${COMMAND} "${MANAGE} create_test_db"

.PHONY: test-migrate
test-migrate: ## Creates and applies the django migrations for tests.
	@${TEST_SETTINGS} make migrate

.PHONY: test-populate
test-populate: ## Populates the database with dummy data for tests.
	@${TEST_SETTINGS} make populate

.PHONY: test-flush
test-flush: ## Flush the database for tests.
	@${TEST_SETTINGS} make flush

.PHONY: test-recreate
test-recreate: ## Recreate the the database with dummy data for tests.
	@make test-flush
	@make create-test-db
	@make test-migrate
	@make test-populate

.PHONY: test
test: ## Run the tests. You can modify the app that will be tested with APP parameter.
	@make create-test-db
ifeq (${APP},)
	@${COMMAND} "pytest ${APP} ${PYTEST_SETTINGS}"
else
	@${COMMAND} "pytest ${APP} -s ${PYTEST_SETTINGS}"
endif

.PHONY: cover-test
cover-test: ## Run the tests with coverage.
	@make create-test-db
	@${COMMAND} "pytest ${APP} ${PYTEST_SETTINGS} ${COVERAGE_SETTINGS}"

.PHONY: html-test
html-test: ## Run the tests with coverage and html report.
	@make create-test-db
	@${COMMAND} "pytest ${APP} ${PYTEST_SETTINGS} ${COVERAGE_WITH_HTML_SETTINGS}"

.PHONY: fast-test
fast-test: ## Run the tests in parallel
	@${COMMAND} "pytest ${APP} ${PYTEST_SETTINGS} -n auto"

.PHONY: database
database: ## Access the mysql in the database container. You can modify user/password with DBUSER and DBPASSWORD parameters.
	@${DOCKER_FILE} exec database mysql -u${DBUSER} -p${DBPASSWORD}

.PHONY: lint
lint: ## Run the linter
	@${COMMAND} "black . ${BLACK_SETTINGS}"

.PHONY: check-lint
check-lint: ## Check for linting errors.
	@${COMMAND} "black . ${BLACK_SETTINGS} --check"

.PHONY: check-lint-local
check-lint-local: ## Check for linting errors in local, useful for CI.
	@black . ${BLACK_LOCAL_SETTINGS} --check

.PHONY: sort-imports
sort-imports: ## Sort the imports
	@${COMMAND} "isort . ${ISORT_SETTINGS}"

.PHONY: check-imports
check-imports: ## Check for errors on imports ordering.
	@${COMMAND} "isort . ${ISORT_SETTINGS} --check"

.PHONY: check-imports-local
check-imports-local:  ## Check for errors on imports ordering in local, useful for CI.
	@isort . ${ISORT_LOCAL_SETTINGS} --check

.PHONY: wait-db
wait-db: ## Wait until the database is ready, useful for CI. You can modify the host with HOST parameter.
	@while [[ @true ]] ; do \
		if ${PING_DB} --silent &> /dev/null; then\
			echo "Database is up!" && break ; \
		fi ; \
		echo "Waiting for the database to be up" && sleep 1 ; \
	done
