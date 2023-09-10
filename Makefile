up:
	docker-compose up

run-backend:
	docker-compose exec django sh -c "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py init_data && uvicorn --host 0.0.0.0 --reload main.asgi:application"

.migrate:
	docker-compose exec django python manage.py migrate

migrate:
	docker-compose exec django python manage.py migrate $(filter-out $@,$(MAKECMDGOALS))

.migrations:
	docker-compose exec django python manage.py makemigrations

migrations:
	docker-compose exec django python manage.py makemigrations $(filter-out $@,$(MAKECMDGOALS))

migrations-migrate: .migrations .migrate

shell:
	docker-compose exec django sh -c "mkdir -p ~/.ipython/profile_default"
	docker-compose exec django sh -c "echo \"c.InteractiveShellApp.exec_lines = ['%autoreload 2']\nc.InteractiveShellApp.extensions = ['autoreload']\" > ~/.ipython/profile_default/ipython_config.py"
	docker-compose exec django python manage.py shell_plus

build-backend:
	docker-compose build django celery-worker celery-beat

build: build-backend

init-data:
	docker-compose exec django python manage.py init_data $(filter-out $@,$(MAKECMDGOALS))

pip-compile:
	docker-compose exec django sh -c "pip install pip-tools && pip-compile"

.stop-db-related:
	docker-compose stop django celery-worker celery-beat

.drop-create-db: run-postgres
	docker-compose exec postgres dropdb -U postgres --if-exists management_db
	docker-compose exec postgres createdb -U postgres management_db
	docker-compose up -d django celery-worker celery-beat

.start-db-related:
	docker-compose up -d django celery-worker celery-beat

reset-db: .stop-db-related .drop-create-db .start-db-related

reset-init-db: reset-db migrations-migrate init-db

delete-migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -delete

reset-migrations: delete-migrations reset-db migrations-migrate

lint-backend:
	docker-compose exec django pylint main

reformat-backend:
	docker-compose exec django pip install yapf
	docker-compose exec django yapf -ipr --exclude "**/migrations/*" main

reformat: reformat-backend

test-backend:
	docker-compose exec django python manage.py test $(filter-out test,$(filter-out $@,$(MAKECMDGOALS))) --parallel

test-backend-no-parallel:
	docker-compose exec django python manage.py test $(filter-out test,$(filter-out $@,$(MAKECMDGOALS)))

test: test-django

messages:
	docker-compose exec django python manage.py makemessages -l th

compilemessages:
	docker-compose exec django python manage.py compilemessages -l th

down:
	docker-compose down --remove-orphans

%:
	@:
