# Makefile for personal website in html, css, js

# Set the default goal
.DEFAULT_GOAL := push

# List of PHONY targets
.PHONY: push help

# Push to remote
COMMIT_MSG=
push:
	git add .
	if [ -z "$(COMMIT_MSG)" ]; then git commit -m "Ran make"; else git commit -m "$(COMMIT_MSG)"; fi
	git push

# Default - Help message
help:
	@echo "Makefile for website"
	@echo "Usage:"
	@echo "  make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  push [COMMIT_MSG=\"<msg>\"]  Add, commit, push"
	@echo "  help          Show this help message (default)"
