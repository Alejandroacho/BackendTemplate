ENV ?= Local
SETTINGS ?= $(shell echo $(ENV) | tr '[:upper:]' '[:lower:]')
DBUSER ?= user
DBPASSWORD ?= password
HOST ?= "127.0.0.1"
COMMAND = docker exec -i django-app bash -c
MANAGE = python manage.py
DOCKER_FILE = docker-compose -f ./Docker/${ENV}/docker-compose.yml
DOCKER_FILE_TEXT = docker-compose -f ./Docker/<ENV>/docker-compose.yml
EQUALS = is equivalent to
SETTINGS_FLAG = --settings=App.settings.django.${SETTINGS}_settings
TEST_SETTINGS = SETTINGS=test
SETTINGS_FLAG_TEXT = --settings=App.settings.django.<SETTINGS>_settings
PYTEST_SETTINGS = --reuse-db --ds=App.settings.django.test_settings -W ignore::django.utils.deprecation.RemovedInDjango41Warning -p no:cacheprovider
COVERAGE_SETTINGS = --cov --cov-config=.coveragerc
COVERAGE_WITH_HTML_SETTINGS = ${COVERAGE_SETTINGS} --cov-report=html
OITNB_SETTINGS = --exclude="/migrations/*" --icons --line-length=79
ISORT_SETTINGS = --known-local-folder=App/ --skip-glob="**/migrations/*" --skip-glob="**/.env/*" --lai=2 --sl --use-parentheses --trailing-comma --force-grid-wrap=0 --multi-line=3
PING_DB = docker exec database mysqladmin --user=user --password=password --host ${HOST} ping
SHELL := /bin/bash

all:
	@make up

up:
	${DOCKER_FILE} up

upd:
	${DOCKER_FILE} up -d

stop:
	${DOCKER_FILE} stop

ps:
	${DOCKER_FILE} ps

bash:
	${DOCKER_FILE} exec app /bin/bash

shell:
	${COMMAND} "${MANAGE} shell_plus ${SETTINGS_FLAG}"

startapp:
	${COMMAND} "${MANAGE} startapp ${APP}"

createsuperuser:
	${COMMAND} "${MANAGE} createsuperuser"

migrate:
	${COMMAND} "${MANAGE} makemigrations ${SETTINGS_FLAG}"
	${COMMAND} "${MANAGE} migrate ${SETTINGS_FLAG}"

populate:
ifeq (${INSTANCES},)
	${COMMAND} "${MANAGE} populate_db -i 50 ${SETTINGS_FLAG}"
else
	${COMMAND} "${MANAGE} populate_db -i $(INSTANCES) ${SETTINGS_FLAG}"
endif

flush:
	${COMMAND} "${MANAGE} flush ${SETTINGS_FLAG}"

show_urls:
ifeq (${GREP},)
	${COMMAND} "${MANAGE} show_urls"
else
	${COMMAND} "${MANAGE} show_urls | grep ${GREP}"
endif

recreate:
	make flush
	make migrate
	make populate

create-test-db:
	${COMMAND} "${MANAGE} create_test_db"

test:
	make create-test-db
ifeq (${COVER}, yes)
	${COMMAND} "pytest ${APP} ${PYTEST_SETTINGS} ${COVERAGE_SETTINGS}"
else ifeq (${COVERHTML}, yes)
	${COMMAND} "pytest ${APP} ${PYTEST_SETTINGS} ${COVERAGE_WITH_HTML_SETTINGS}"
else ifeq (${APP},)
	${COMMAND} "pytest ${APP} ${PYTEST_SETTINGS}"
else
	${COMMAND} "pytest ${APP} -s ${PYTEST_SETTINGS}"
endif

fast-test:
	${COMMAND} "pytest ${APP} ${PYTEST_SETTINGS} -n auto"

test-migrate:
	${TEST_SETTINGS} make migrate

test-populate:
	${TEST_SETTINGS} make populate

test-flush:
	${TEST_SETTINGS} make flush

test-recreate:
	make test-flush
	make create-test-db
	make test-migrate
	make test-populate

freeze:
	${COMMAND} "pip freeze"

logs:
	${DOCKER_FILE} logs -f

database:
	${DOCKER_FILE} exec database mysql -u${DBUSER} -p${DBPASSWORD}

lint:
	${COMMAND} "oitnb . ${OITNB_SETTINGS}"

check-lint:
	${COMMAND} "oitnb --check . ${OITNB_SETTINGS}"

check-lint-local:
	oitnb --check . ${OITNB_SETTINGS}

sort-imports:
	${COMMAND} "isort . ${ISORT_SETTINGS}"

check-sort-imports:
	${COMMAND} "isort . ${ISORT_SETTINGS} --check"

check-sort-imports-local:
	isort . ${ISORT_SETTINGS} --check

wait-db:
	@while [[ @true ]] ; do \
		if ${PING_DB} --silent &> /dev/null; then\
			echo "Database is up!" && break ; \
		fi ; \
		echo "Waiting for the database to be up" && sleep 1 ; \
	done

help:
	@echo ""
	@echo "USAGE: make [command]"
	@echo "You can pass APP, ENV or SETTINGS variable to command likae that:"
	@echo "ENV=Local make up"
	@echo "Note that <ENV> must be capitalized and that <SETTINGS> will be <ENV> in lowercase"
	@echo ""
	@echo "---------------------------------------------------------------------------------"
	@echo "Commands:"
	@echo ""
	@echo " • up: Start the containers"
	@echo "   ↳ ${EQUALS} < ${DOCKER_FILE_TEXT} up >"
	@echo ""
	@echo " • upd: Start the containers"
	@echo "   ↳ ${EQUALS} < ${DOCKER_FILE_TEXT} up -d >"
	@echo ""
	@echo " • stop: Stop the containers"
	@echo "   ↳ ${EQUALS} < ${DOCKER_FILE_TEXT} stop >"
	@echo ""
	@echo " • ps: Show the running containers"
	@echo "   ↳ ${EQUALS} < ${DOCKER_FILE_TEXT} ps >"
	@echo ""
	@echo " • bash: Open a bash shell in the app container"
	@echo "   ↳ ${EQUALS} < ${DOCKER_FILE_TEXT} exec app /bin/bash >"
	@echo ""
	@echo " • shell: Open a Django shell_plus in the app container"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} shell_plus ${SETTINGS_FLAG_TEXT}' >"
	@echo ""
	@echo " • startapp: Create a new app"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} startapp <APP>' >"
	@echo ""
	@echo " • createsuperuser: Create a superuser"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} createsuperuser' >"
	@echo ""
	@echo " • migrate: Run migrations"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} makemigrations ${SETTINGS_FLAG_TEXT}' >"
	@echo "                      < ${COMMAND} '${MANAGE} migrate ${SETTINGS_FLAG_TEXT}' >"
	@echo ""
	@echo " • populate: Populate the database"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} populate_db -i 50 ${SETTINGS_FLAG_TEXT}' >"
	@echo ""
	@echo " • INSTANCES=<int> populate: Populate the database with a number of instances"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} populate_db -i <INSTANCES> ${SETTINGS_FLAG_TEXT}' >"
	@echo ""
	@echo " • flush: Flush the database"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} flush ${SETTINGS_FLAG_TEXT}' >"
	@echo ""
	@echo " • show_urls: Show the urls of django project"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} show_urls' >"
	@echo ""
	@echo " • GREP=<str> show_urls: Show the urls of django project making a grep"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} show_urls | grep <GREP>' >"
	@echo ""
	@echo " • recreate: Recreated the database"
	@echo "   ↳ ${EQUALS} < make flush >"
	@echo "                      < make migrate >"
	@echo "                      < make populate >"
	@echo ""
	@echo " • create-test-db: Create a test database"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} create_test_db' >"
	@echo ""
	@echo " • test: Run tests"
	@echo "   ↳ ${EQUALS} < make create-test-db >"
	@echo "                      < ${COMMAND} 'pytest <APP>"
	@echo "                        ${PYTEST_SETTINGS}' >"
	@echo ""
	@echo " • COVER=yes test: Run tests"
	@echo "   ↳ ${EQUALS} < make create-test-db >"
	@echo "                      < ${COMMAND} 'pytest <APP>"
	@echo "                        ${PYTEST_SETTINGS}"
	@echo "                        ${COVERAGE_SETTINGS}' >"
	@echo ""
	@echo " • COVERHTML=yes test: Run tests"
	@echo "   ↳ ${EQUALS} < make create-test-db >"
	@echo "                      < ${COMMAND} 'pytest <APP>"
	@echo "                        ${PYTEST_SETTINGS}"
	@echo "                        ${COVERAGE_SETTINGS}"
	@echo "                        --cov-report=html' >"
	@echo ""
	@echo " • fast-test: Run tests faster with x-dist pytest extension"
	@echo "   ↳ ${EQUALS} < make create-test-db >"
	@echo "                      < ${COMMAND} 'pytest <APP>"
	@echo "                        ${PYTEST_SETTINGS} -n auto' >"
	@echo ""
	@echo " • test-migrate: Run migrations for test environment"
	@echo "   ↳ ${EQUALS} < ${TEST_SETTINGS} make migrate >"
	@echo ""
	@echo " • test-populate: Populate the testing database"
	@echo "   ↳ ${EQUALS} < ${TEST_SETTINGS} make populate>"
	@echo ""
	@echo " • test-flush: Flush the database for tests"
	@echo "   ↳ ${EQUALS} < ${TEST_SETTINGS} make flush>"
	@echo ""
	@echo " • test-recreate: Run recreate for tests"
	@echo "   ↳ ${EQUALS} < make test-flush >"
	@echo "                      < make create_test_db >"
	@echo "                      < make test-migrate >"
	@echo "                      < make test-populate >"
	@echo ""
	@echo " • freeze: Freeze the requirements"
	@echo "   ↳ ${EQUALS} < ${COMMAND} 'pip freeze'>"
	@echo ""
	@echo " • logs: Show the logs"
	@echo "   ↳ ${EQUALS} < ${DOCKER_FILE} logs -f>"
	@echo ""
	@echo " • database: Open a mysql shell"
	@echo "   ↳ ${EQUALS} < ${DOCKER_FILE} exec database mysql -u<DBUSER> -p<DBPASSWORD> >"
	@echo ""
	@echo " • lint: Format the code"
	@echo "   ↳ ${EQUALS} < ${COMMAND} 'oitnb . ${OITNB_SETTINGS}' >"
	@echo ""
	@echo " • check-lint: Check the code for formatting"
	@echo "   ↳ ${EQUALS} < ${COMMAND} 'oitnb --check . ${OITNB_SETTINGS}' >"
	@echo ""
	@echo " • sort-imports: Sort the imports according PEP 8 and PEP 328"
	@echo "   ↳ ${EQUALS} < ${COMMAND} 'isort . ${ISORT_SETTINGS}' >"
	@echo ""
	@echo " • check-sort-imports: Check the order of the imports according PEP 8 and PEP 328"
	@echo "   ↳ ${EQUALS} < ${COMMAND} 'isort . ${ISORT_SETTINGS} --check' >"
	@echo ""
	@echo " • help: Show this help"
	@echo ""
	@echo "---------------------------------------------------------------------------------"
