PYENV = env
PYTHON = $(PYENV)/bin/python


.PHONY: runserver
runserver: requirements/base.txt.done
	$(PYTHON) manage.py runserver


.PHONY: test
test: requirements/development.txt.done
	$(PYENV)/bin/pytest


requirements/development.txt.done: env
	$(PYTHON) -m pip install --upgrade -r requirements/development.txt
	touch $@


requirements/base.txt.done: env
	$(PYTHON) -m pip install --upgrade -r requirements/base.txt
	touch $@


env:
	virtualenv -p $(shell which python3) env


.PHONY: clean
clean:
	rm -f requirements/*.done


.PHONY: realclean
realclean: clean
	rm -rf $(PYENV)
