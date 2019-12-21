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
	$(PYTHON) -m manage migrate
	$(PYTHON) -m manage runserver


.PHONY: run-uwsgi
run-uwsgi: develop
	$(PYTHON) -m pip install uwsgi
	$(VENVDIR)/bin/uwsgi --virtualenv=$(VENVDIR) --module=abusor.wsgi:application --check-static=$(PWD) --http :8000


.PHONY: test
test: develop
	$(PYTHON) -m pip install --editable .[test]
	$(PYTHON) -m pytest

.PHONY: requirements.txt
requirements.txt:
	$(PYTHON) -m pip install pip-tools
	$(VENVDIR)/bin/pip-compile --generate-hashes --output-file $@


clean:
	rm -rf $(VENVDIR)
	find .  -type d -name __pycache__ -print0 | xargs --null rm -rf
	rm -rf abusor.egg-info
