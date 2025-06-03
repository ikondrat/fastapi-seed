.PHONY: install
install:
	@echo "Installing with optional dependencies..."
	uv sync --all-groups


.PHONY: test
test:
	@echo "Running tests..."
	uv run pytest

.PHONY: lint
lint:
	@echo "Linting project with ruff..."
	uv run ruff check

.PHONY: type-check
type-check:
	@echo "Checking types with mypy..."
	uv run mypy --explicit-package-bases fastapi_seed

.PHONY: format-check
format-check:
	@echo "Checking format with ruff..."
	uv run ruff format --check

.PHONY: static-checks
static-checks: lint type-check format-check

.PHONY: format
format:
	@echo "Formatting project with ruff..."
	uv run ruff format
	uv run ruff check --fix

.PHONY: lint-fix
lint-fix:
	uv run ruff check --fix

