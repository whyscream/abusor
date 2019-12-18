ifdef TRAVIS
	VENVDIR = ~/virtualenv/python$(TRAVIS_PYTHON_VERSION)
else
	VENVDIR = .venv
endif

PYTHON_VERSION := 3.7

PYTHON = $(VENVDIR)/bin/python


$(VENVDIR):
	$(shell which python$(PYTHON_VERSION)) -m venv $@
	$(PYTHON) -m pip install --upgrade pip setuptools


.PHONY: develop
develop: abusor.egg-info  # alias
abusor.egg-info: $(VENVDIR)
	$(PYTHON) -m pip install --editable .


.PHONY: run
run: develop
	$(PYTHON) -m abusor.manage migrate
	$(PYTHON) -m abusor.manage runserver


.PHONY: test
test: develop
	$(PYTHON) -m pip install --editable .[test]
	$(PYTHON) -m pytest

clean:
	rm -rf $(VENVDIR)
	find .  -type d -name __pycache__ -print0 | xargs --null rm -rf
	rm -rf abusor.egg-info
