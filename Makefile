# If you have `direnv` loaded in your shell, and allow it in the repository,
# the `make` command will point at the `scripts/make` shell script.
# This Makefile is just here to allow auto-completion in the terminal.

default: help
	@echo
	@echo 'Enable direnv in your shell to use the `make` command: `direnv allow`'
	@echo 'Or use `python scripts/make ARGS` to run the commands/tasks directly.'

.DEFAULT_GOAL: default

actions = \
	allrun \
	changelog \
	check \
	check-api \
	check-docs \
	check-quality \
	check-types \
	clean \
	coverage \
	docs \
	docs-deploy \
	format \
	help \
	multirun \
	release \
	run \
	setup \
	test \
	vscode

.PHONY: $(actions)
$(actions):
	@python scripts/make "$@"
