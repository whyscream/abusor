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


.PHONY: travis-prepare
travis-prepare:
	echo "SECRET_KEY='secret'" >> abusor/custom_settings.py


requirements/development.txt.done: $(PYENV)
	$(PYTHON) -m pip install --upgrade -r requirements/development.txt
	touch $@


requirements/base.txt.done: $(PYENV)
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
