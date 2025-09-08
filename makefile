.PHONY: run test sync

run:
	uv run python main.py

sync:
	uv sync --locked

# Run all tests
test:
	export PYTHONPATH=$PWD/src
	uv run python -m pytest

# Run a single test by name passed as a variable
test_n:
	export PYTHONPATH=$PWD/src
	@if [ -z "$(NAME)" ]; then \
		echo "Please pass NAME=<test_name>"; \
		exit 1; \
	fi
	uv run -- python -m pytest -k "$(NAME)"
