.PHONY: help lint
.DEFAULT_GOAL := help

SHELL := /bin/bash


help: ## show target summary
	@grep -E '^\S+:.* ## .+$$' $(MAKEFILE_LIST) | sed 's/##/#/' | while IFS='#' read spec help; do \
	  tgt=$${spec%%:*}; \
	  printf "\n%s: %s\n" "$$tgt" "$$help"; \
	  awk -F ': ' -v TGT="$$tgt" '$$1 == TGT && $$2 ~ "=" { print $$2 }' $(MAKEFILE_LIST) | \
	  while IFS='#' read var help; do \
	    printf "  %s  :%s\n" "$$var" "$$help"; \
	  done \
	done


.pip: requirements/base.txt ## install dependencies
	python3 -m pip install -t .pip -r requirements/base.txt -r requirements/cli.txt
	touch .pip


test: ## run test suite
	PYTHONPATH=.:.pip python3 -m pytest tests


build: Dockerfile Dockerfile.jq xibbaz ## build docker images
	docker build -t xibbaz .
	docker build -t xibbaz:jq -f Dockerfile.jq .
