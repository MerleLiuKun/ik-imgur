# test for project

all: isort lint test

.PHONY: all

isort:
	sh -c "isort --skip=migrations/ --recursive ."

lint:
	flake8 --ignore w504,E501 --exclude migrations,.git,__pycache__,var

test:
	py.test --verbose --color=yes