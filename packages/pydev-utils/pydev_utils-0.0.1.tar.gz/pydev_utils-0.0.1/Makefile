.PHONY: test test-format format build

test:
	@pylint --rcfile=pyproject.toml pydev_utils
	@coverage run --rcfile=pyproject.toml --source=pydev_utils -m pytest
	@coverage report --rcfile=pyproject.toml

test-format:
	ufmt check .

format:
	ufmt format .

build:
	python -m build
