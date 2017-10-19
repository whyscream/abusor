ifdef TRAVIS
	PYENV = ~/virtualenv/python$(TRAVIS_PYTHON_VERSION)
else
	PYENV = env
endif

PYTHON = $(PYENV)/bin/python


.PHONY: runserver
runserver: requirements/base.txt.done
	$(PYTHON) manage.py runserver


.PHONY: test
test: requirements/development.txt.done
	$(PYENV)/bin/pytest


requirements/development.txt.done: $(PYENV) requirements/development.txt
ifeq ($(PIP_UPGRADE),no)
	$(PYTHON) -m pip install -r requirements/development.txt
else
	$(PYTHON) -m pip install --upgrade -r requirements/development.txt
endif
	touch $@


requirements/base.txt.done: $(PYENV) requirements/base.txt
ifeq ($(PIP_UPGRADE),no)
	$(PYTHON) -m pip install -r requirements/base.txt
else
	$(PYTHON) -m pip install --upgrade -r requirements/base.txt
endif
	touch $@


$(PYENV):
	virtualenv -p $(shell which python3) $@


.PHONY: clean
clean:
	rm -f requirements/*.done
	rm -f -r .cache

.PHONY: realclean
realclean: clean
	rm -rf $(PYENV)
