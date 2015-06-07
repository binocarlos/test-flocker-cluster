.PHONY: boot install test test-install

install:
	@python setup.py install

boot:
	@bash boot.sh

test:
	@tox

test-install:
	@tox -r