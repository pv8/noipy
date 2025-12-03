# SPDX-FileCopyrightText: 2015 Pablo V <noipy@pv8.dev>
#
# SPDX-License-Identifier: Apache-2.0

VERSION := $(shell python -c "from __future__ import print_function; import noipy; print('v{}'.format(noipy.__version__))")

.PHONY: all
all: clean tests dist
	@echo "=> All set up."
	@echo "=> execute *make publish* to upload to PyPI repository."

dist: clean
	@echo "=> Building packages"
	python setup.py sdist bdist_wheel

devdeps:
	@echo "=> Installing dev dependencies"
	pip install -e ".[tests,lint]"

.PHONY: tests
tests: devdeps
	@echo "=> Running tests"
	tox

.PHONY: clean
clean:
	@echo "=> Cleaning..."
	find . -type f -name "*.pyc" -delete
	rm -rf dist/
	rm -rf build/

.PHONY: publish
publish: dist
	@echo "=> Publishing [noipy $(VERSION)] on PyPI test repository"
	twine upload -r test dist/*
	@echo "=> execute *twine upload -r test dist/* to upload to PyPI repository."
