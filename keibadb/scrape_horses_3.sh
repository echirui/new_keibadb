#!/bin/bash
uv run python manage.py scrape_horse --horse_id 1987102284 && sleep 0.05
uv run python manage.py scrape_horse --horse_id 1987104204 && sleep 0.05
# ... (and so on for all 1000 horse keys) ...
uv run python manage.py scrape_horse --horse_id 1987103716 && sleep 0.05
