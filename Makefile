.PHONY: clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"
LOCALE_DIR := src/django_powerbank/locale

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint: ## check style with flake8
	flake8 django_powerbank tests

test: ## run tests quickly with the default Python
	python runtests.py tests

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source django_powerbank runtests.py tests
	coverage report -m
	coverage html
	open htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/django-powerbank.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ django_powerbank
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

locale-create:  ## create locale file for supported languages
	# http://babel.edgewall.org/wiki/BabelDjango#CreatingandUpdatingTranslationsCatalogs
	pybabel init -D django -i $(LOCALE_DIR)/django.pot -d locale -l pl

locale-update: ## generate locale files
	mkdir -p .tmp
	pybabel extract -F $(LOCALE_DIR)/babel.cfg -o $(LOCALE_DIR)/django.pot --no-wrap --sort-output .
	pybabel update -D django -i $(LOCALE_DIR)/django.pot -d $(LOCALE_DIR) --previous --no-wrap

locale-compile: ## generate locale files
	pybabel compile -D django -d $(LOCALE_DIR) --statistics

trans: locale-update locale-compile ## update and compile locales

sync: ## Sync master and develop branches in both directions
	git checkout develop
	git pull origin develop --verbose
	git checkout master
	git pull origin master --verbose
	git checkout develop
	git merge master --verbose
	git checkout master
	git merge develop --verbose
	git checkout develop

publish: clean ## package and upload a release
	python setup.py sdist upload -r pypi
	python setup.py bdist_wheel upload -r pypi

sdist: clean ## package
	python setup.py sdist
	ls -l dist

bump: ## increment version number
	bumpversion patch

release: sync test-all bump publish ## package and upload a release
	git checkout develop
	git merge master --verbose
	git push origin develop --verbose
	git push origin master --verbose
