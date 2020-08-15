default: help

help:
	@echo Django App Make Commands:
	@echo Usage:
	@echo     make test            Run tests
	@echo     make server          Run django server
	@echo     make db          	   Make database migrations
	@echo     make super           Create superuser

test:
	@echo Running Tests
	python manage.py test --pattern="test_*.py" --verbosity 3

server:
	@echo Running Server
	python manage.py runserver --force-color

db:
	@echo Makemigrations
	python manage.py makemigrations
	@echo Migrate
	python manage.py migrate

super:
	@echo Create superuser
	python manage.py createsuperuser