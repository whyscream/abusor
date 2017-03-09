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
	$(PYTHON) -m pip install --upgrade -r requirements/development.txt
	touch $@


requirements/base.txt.done: $(PYENV) requirements/base.txt
	$(PYTHON) -m pip install --upgrade -r requirements/base.txt
	touch $@


$(PYENV):
	virtualenv -p $(shell which python3) $@


.PHONY: clean
clean:
	rm -f requirements/*.done


.PHONY: realclean
realclean: clean
	rm -rf $(PYENV)
