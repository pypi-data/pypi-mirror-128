.PHONY: build install dev-install dist sdist clean clean-build clean-pyc clean-top-package uninstall

pip_name := strmprivacy-schemas-strmprivacy-demo
pip_version := 1.0.2

build: clean
	python3 build.py build

clean: clean-build clean-pyc clean-top-package

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-top-package:
	python3 -m pip install -r requirements.txt
	python3 -m pip install -r requirements-dev.txt
	python3 build.py clean

dist: clean build ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: dist
	python3 -m pip install .

dev-install: dist
	python3 -m pip install -e .

uninstall:
	python3 -m pip uninstall -y ${pip_name}==${pip_version}

release: dist ## package and upload a release
	twine upload dist/*

release-test: dist
	twine upload --repository testpypi dist/*
