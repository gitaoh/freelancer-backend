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
	python manage.py test

server:
	@echo Running Server
	python manage.py runserver

db:
	@echo Makemigrations
	python manage.py makemigrations
	@echo Migrate
	python manage.py migrate

cov:
	@echo Running code coverage
	coverage erase
	coverage run -m pytest
	coverage html

setup:
	@echo Project setup
	@echo Setting up conda env
	conda create -n freelacer python=3.8
	@echo Activating conda env
	conda activate freelacer
	@echo Installing dependencies
	pip install -r requrements.txt

view:
	@echo Open Project in the browser
	gh repo view --web

dump:
	@echo Flush database
	python manage.py flush

super:
	@echo Making a superuser
	python manage.py createsuperuser --username=joseph --email=joseph@example.com

shell:
	@echo shell
	python manage.py shell
