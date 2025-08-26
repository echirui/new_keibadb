# Suggested Commands

## Package Management (uv)

*   Install dependencies: `uv pip install -r requirements.txt`
*   Add a new package: `uv pip install <package_name>`
*   Upgrade all packages: `uv pip install --upgrade --all`

## Development

*   Run the development server: `python manage.py runserver`
*   Run tests: `python manage.py test`

## Custom Management Commands

The `keibadb/kdb/management/commands` directory contains several custom management commands for data import and processing. Use `python manage.py <command_name>` to run them.