SRC_DIR = llb3d
GENERATED = build dist *.egg-info

all : test lint pep257 dist

twine : dist
	twine upload dist/*

clean :
	rm -rf $(GENERATED)

dist :
	python setup.py sdist bdist_egg bdist_wheel

test :
	py.test $(SRC_DIR)

cov :
	py.test --cov $(SRC_DIR)

lint :
	pylint $(SRC_DIR)

pep257 :
	pep257 $(SRC_DIR)

install :
	python setup.py build install

develop :
	python setup.py develop
