VERSION := $(shell python -c "import noipy; print 'v%s' % noipy.__version__")

.PHONY: all
all: clean tests dist
	@echo "=> All set up."
	@echo "=> execute *make publish* to upload to PyPI repository."

dist: clean
	@echo "=> Building packages"
	python setup.py sdist bdist_wheel

devdeps:
	@echo "=> Installing dev dependencies"
	pip install -r dev-requirements.txt

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
