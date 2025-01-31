.PHONY: clean test build dist environment install uninstall reinstall test

clean:
	rm -rf *.o *.out *.log
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

test:
	pytest

build:
	python -m build

dist:
	make build
	twine upload dist/*

environment:
	mamba create -y -n modland python=3.11 jupyter pykdtree

install:
	pip install -e .[dev]

uninstall:
	pip uninstall -y modland

reinstall:
	make uninstall
	make install

test:
	pytest
