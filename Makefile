PYLINTRC='./.pylintrc'
TEST_PYLINTRC='./test/.pylintrc'

# VERSION=$(shell python lib.py version)
TOKEN=$(shell python tasks/gettoken.py)

# developer
DEFAULT_TEST_PORT="8000"
DEFAULT_CALL_URL="http://127.0.0.1:$(DEFAULT_TEST_PORT)/api/$(TOKEN)/"
DEFAULT_CALL_ID="172862922"
DEFAULT_CALL_TEXT="test"

# PYVERSION=$(shell which python3.5 || echo python)

ifneq ('$(PYVERSION)','python')
	PYVERSION='python3.5'
endif

ifeq ('$(DEV_CALL_ID)','')
	DEV_CALL_ID=$(DEFAULT_CALL_ID)
endif

ifeq ('$(DEV_CALL_URL)','')
	DEV_CALL_URL=$(DEFAULT_CALL_URL)
endif

ifeq ('$(CALL_TEXT)','')
	CALL_TEXT=$(DEFAULT_CALL_TEXT)
endif

# NEXT='$(shell python lib.py $(SEMVER) next-version)'

# lint:
# 	pylint --rcfile=$(PYLINTRC) bobot
# 	pylint --rcfile=$(TEST_PYLINTRC) test

publish:
	git push heroku master

call:
	./tasks/call.sh $(DEV_CALL_URL) $(DEV_CALL_ID) "$(CALL_TEXT)"

run:
	python3.5 manage.py runserver