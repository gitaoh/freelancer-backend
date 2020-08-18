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
	@echo Code Coverage
	coverage run -m pytest
	coverage erase
	coverage html
super:
	@echo Create superuser
	python manage.py createsuperuser

setup:
	@echo project setup
	@echo Setting up conda env
	conda create -n freelacer python=3.8
	@echo Activating conda env
	conda activate freelacer
	@echo Installing dependencies
	pip install -r requrements.txt
