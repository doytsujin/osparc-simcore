.DEFAULT_GOAL := help

ROOT_DIR  = $(abspath $(CURDIR)/../../)
VENV_DIR ?= $(abspath $(ROOT_DIR)/.venv)
UPGRADE_OPTION := $(if $(upgrade),--upgrade-package $(upgrade),--upgrade)


.PHONY: all
all: install tests

.PHONY: reqs
requirements.txt: requirements.in
	# pip compiling $<
	@$(VENV_DIR)/bin/pip-compile $(UPGRADE_OPTION) --build-isolation --output-file $@ $<

reqs: requirements.txt ## alias to compile requirements.txt

.PHONY: install
install: $(VENV_DIR) requirements.txt ## installs dependencies
	# installing requirements
	@$</bin/pip3 install -r requirements.txt


.PHONY: tests
tests: ## runs all tests [DEV]
	# running unit tests
	@$(VENV_DIR)/bin/pytest -vv -x --ff --pdb $(CURDIR)


.PHONY: help
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## this colorful help
	@echo "Recipes for tests/swarm-deploy:"
	@echo ""
	@awk --posix 'BEGIN {FS = ":.*?## "} /^[[:alpha:][:space:]_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
