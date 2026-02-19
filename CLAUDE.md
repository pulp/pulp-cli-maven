# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`pulp-cli-maven` is a Python CLI plugin for the [Pulp content management system](https://pulpproject.org/) that adds Maven repository management commands. The repo contains two packages:

- **`pulp-cli-maven`** (`pulpcore/cli/maven/`) — Click-based CLI commands, registered as a `pulp_cli.plugins` entry point
- **`pulp-glue-maven`** (`pulp-glue-maven/pulp_glue/maven/`) — Version-agnostic API wrapper (context classes) that the CLI commands use

## Common Commands

```bash
# Build both packages
make build

# Format code
make format

# Run all linting (shellcheck, ruff, mypy)
make lint

# Run unit/help-page tests (no live Pulp server required)
make unittest

# Run integration tests against a live server
make livetest

# Run integration tests in parallel
make paralleltest

# Run a single pytest test by keyword
python -m pytest tests/ -k "test_help"
```

## Architecture

### Two-Package Design

The split between `pulp-cli-maven` and `pulp-glue-maven` mirrors the broader pulp-cli ecosystem pattern:

- **Glue** (`pulp_glue/maven/context.py`): Context classes that wrap Pulp REST API calls. They extend base classes from `pulp-glue` (e.g., `PulpContentContext`, `PulpDistributionContext`, `PulpRemoteContext`, `PulpRepositoryContext`). All API interactions happen here.
- **CLI** (`pulpcore/cli/maven/`): Click command groups that use glue context classes. Commands are registered via `mount()` in `pulpcore/cli/maven/__init__.py`.

### Plugin Registration

The CLI plugin is registered via the `pulp_cli.plugins` entry point in `pyproject.toml`. The `mount()` function in `__init__.py` attaches `repository`, `remote`, and `distribution` command groups to the main `pulp` CLI.

### Context Class Pattern

Glue context classes define:
- `ENDPOINT` — the Pulp API endpoint path
- `CAPABILITIES` — list of capability strings with version requirements (e.g., `"add-cached-content"` requires `pulp_maven>=0.5.0.dev`)
- `preprocess_entity()` — transforms CLI parameters before sending to API (e.g., `PulpMavenDistributionContext` converts `version` + repository to a `repository_version` URL)

### Testing

- **Help page tests** (`tests/test_help_pages.py`): Validates all CLI help screens render without a live server. Marked `help_page`.
- **Shell integration tests** (`tests/scripts/pulp_maven/`): Bash scripts using helper functions (`expect_succ`, `expect_fail`) from `tests/scripts/config.source`. Marked `script` and `pulp_maven`.
- Live tests require a `tests/cli.toml` config (see `tests/cli.toml.example`).

### Versioning

Both packages share the same version (`0.5.0.dev`). Version is managed via bumpversion and updated in four files: both `pyproject.toml` files and both `__init__.py` files. Changelogs use towncrier (fragments go in `CHANGES/`).

### Type Checking

Both packages use strict mypy. The `pulp-cli` and `click` types must be compatible — `check_click_for_mypy.py` in `.ci/scripts/` validates this.
