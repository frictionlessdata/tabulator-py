.PHONY: all install list test version


PACKAGE := $(shell grep '^PACKAGE =' setup.py | cut -d "'" -f2)
VERSION := $(shell head -n 1 $(PACKAGE)/VERSION)


all: list

install:
	pip install --upgrade -e .[datapackage,develop,ods]

list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

readme:
	pip install md-toc
	md_toc -p README.md github --header-levels 5
	sed -i '/(#$(PACKAGE)-py)/,+2d' README.md

test:
	tox

version:
	@echo $(VERSION)
