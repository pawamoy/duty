.DEFAULT_GOAL := help
SHELL := bash

DUTY = $(shell [ -n "${VIRTUAL_ENV}" ] || echo poetry run) duty
PYTHON_VERSIONS ?= 3.6 3.7 3.8

BASIC_DUTIES = \
	changelog \
	clean \
	combine \
	coverage \
	docs \
	docs-deploy \
	docs-regen \
	docs-serve \
	format \
	release

QUALITY_DUTIES = \
	check \
	check-code-quality \
	check-dependencies \
	check-docs \
	check-types \
	test

.PHONY: help
help:
	@$(DUTY) --list

.PHONY: setup
setup:
	@env PYTHON_VERSIONS="$(PYTHON_VERSIONS)" bash scripts/setup.sh

.PHONY: $(BASIC_DUTIES)
$(BASIC_DUTIES):
	@$(DUTY) $@

.PHONY: $(QUALITY_DUTIES)
$(QUALITY_DUTIES):
	@env PYTHON_VERSIONS="$(PYTHON_VERSIONS)" bash scripts/multirun.sh duty $@
