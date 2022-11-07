install-prod:
	poetry --version && poetry install --no-root --without test

install:
	poetry --version && poetry install --no-root

make-migrations:
	python support/manage.py makemigrations

migrate:
	python support/manage.py migrate

run-app:
	python support/manage.py runserver 0.0.0.0:8000

code-style-checks:
	flake8 support/ tests/

drf-tests:
	poetry run pytest --color=yes tests/

full-migrate-and-run:
	python support/manage.py makemigrations userauth && \
    python support/manage.py migrate userauth && \
	python support/manage.py makemigrations ticket && \
    python support/manage.py migrate ticket && \
    python support/manage.py makemigrations && \
    python support/manage.py migrate && \
    python support/manage.py runserver 0.0.0.0:8000

# fake-migrate:
# 	python support/manage.py migrate --fake


# code-style-checks:
# 	flake8 support/ tests/ && \
# 	# isort --check-only support/ tests/ && \
# 	# black --check support/ tests/

# unit-tests:
# 	....

# api-tests:
# 	....
