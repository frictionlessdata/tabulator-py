.PHONY: all list install test review coverage

PKG := tabulator

all: test coverage review

# http://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs

install:
	pip install --upgrade -e .
	pip install --upgrade -r tests_require

test:
	PACKAGE=$(PKG) tox

review:
	pylint $(PKG)

coverage:
	coveralls
