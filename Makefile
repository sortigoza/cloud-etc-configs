# REPOSITORY=TBD
# VERSION=latest

.PHONY: help
help: ## Display this help screen
	@echo "Please use \`make <target>' where <target> is one of"
	@grep -E '^[a-zA-Z_-][a-zA-Z_\-\/]+[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\t\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "make sure to populate your env with \`source bin/env' before using this tool"

.PHONY: all
all: validate build container/build container/run ## validate, executes local and container build then run container

# ------------------------
# Local + CI
# ------------------------
.PHONY: run
run: ## run main.py file
	@python main.py

.PHONY: build
build: validate ## build package
	@echo "Build binary"
	@python setup.py build

.PHONY: validate
validate: lint test ## run linter and tests

.PHONY: test
test: install ## run tests
	@echo "Running tests"
	@python -m pytest --cov=cloud_etc_configs --cov-append --cov-report term-missing -v tests/

.PHONY: fmt
fmt: ## format files
	autoflake --in-place --remove-all-unused-imports -r .
	isort **/*.py
	black .

.PHONY: metrics
metrics: ## code metrics
	radon cc . --total-average -s
	radon mi .

.PHONY: lint
lint: ## run lint
	@echo "Running linters"
	black --check .

.PHONY: install
install: ## install package
	@echo "Installing package"
	@python setup.py install -f

.PHONY: clean
clean: ## clean directories
	@rm -rf build/
	@rm -rf dist/
	@rm -rf cloud_etc_configs.egg-info/
	@rm -rf .pytest_cache/
