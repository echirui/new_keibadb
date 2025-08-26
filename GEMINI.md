# Python Package Management with `uv`

This project uses `uv` for efficient Python package management.

## Installation

If you don't have `uv` installed, you can install it using pip:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Basic Usage

### Installing dependencies from `requirements.txt`

To install all dependencies listed in `requirements.txt`:

```bash
uv pip install -r requirements.txt
```

### Adding a new package

To add a new package (e.g., `requests`):

```bash
uv pip install requests
```

### Upgrading packages

To upgrade all installed packages:

```bash
uv pip install --upgrade --all
```

### Running a command with `uv`'s environment

To run a Python script or command within the `uv` managed environment:

```bash
uv run python your_script.py
```

# Project Overview

This project is a Django application.
