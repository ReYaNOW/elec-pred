PORT ?= 8080


install:
	poetry install
	poetry run pre-commit install

dev:
	poetry run python manage.py runserver 0.0.0.0:$(PORT)

start:
	poetry run gunicorn -b 0.0.0.0:$(PORT) elec_pred.wsgi:application

shell:
	poetry run python3 manage.py shell_plus --ipython

lint:
	poetry run ruff check

lint_fix:
	poetry run ruff check --fix

format:
	poetry run ruff format

start_db:
	docker compose start db

enter_db:
	docker compose exec -it db psql -U pguser -d pgdb psql

messages:
	poetry run django-admin makemessages -l ru

compilemessages:
	poetry run django-admin compilemessages --ignore=.venv || true

migrations:
	poetry run python3 manage.py makemigrations

migrate:
	poetry run python3 manage.py migrate

compile_static:
	python3 manage.py collectstatic
