import subprocess
import sys

for year in range(1990, 2026):
    print(f"--- Importing {year}.csv ---", flush=True)
    command = f"uv run python manage.py import_race_csv --csv_file ../csv_data/{year}.csv"
    
    try:
        # Using subprocess.run to get better control over output
        result = subprocess.run(
            command,
            shell=True,
            check=True,  # Raises CalledProcessError for non-zero exit codes
            capture_output=True,
            # text=True,  # Removed
            # encoding='utf-8' # Removed
        )
        # Print stdout line by line to avoid partial writes
        print(result.stdout.decode('utf-8', errors='ignore'), flush=True)
        if result.stderr:
            print("--- Stderr ---", flush=True)
            print(result.stderr.decode('utf-8', errors='ignore'), flush=True)

    except subprocess.CalledProcessError as e:
        print(f"--- ERROR: Failed to import {year}.csv ---", flush=True)
        print(e.stdout.decode('utf-8', errors='ignore'), flush=True)
        print(e.stderr.decode('utf-8', errors='ignore'), flush=True)
        # Decide whether to continue or break on error. Continuing for now.

print("--- All imports finished. ---", flush=True)
