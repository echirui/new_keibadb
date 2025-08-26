# Codebase Structure

The project is a standard Django application with the following structure:

*   `keibadb/`: The main Django project directory.
    *   `kdb/`: The core Django application.
        *   `models.py`: Defines the database models.
        *   `management/commands/`: Contains custom Django management commands for tasks like importing data and scraping.
    *   `keibadb/`: Contains the project-level settings, URLs, etc.
*   `csv_data/`: Contains CSV files with horse racing data, likely for import.
*   `scripts/`: Contains various helper scripts.