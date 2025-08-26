from kdb.models import Stallion
import os
import django
from django.db.models import Q
from django.core.management import call_command

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "keibadb.settings")
django.setup()


def fill_missing_parent_data():
    # Query for horses with null father_key or mother_key
    horses_to_process = Stallion.objects.filter(
        Q(father_key__isnull=True) | Q(mother_key__isnull=True)
    )
    total_horses = horses_to_process.count()

    print(f"Found {total_horses} horses with missing parent data.")

    if total_horses == 0:
        print("No horses to process. Exiting.")
        return

    processed_count = 0
    for horse in horses_to_process:
        try:
            print(f"Processing horse_key: {horse.horse_key}")
            call_command(
                "scrape_horse", horse_id=horse.horse_key
            )  # scrape_horse expects horse_id
            processed_count += 1

            if processed_count % 100 == 0:
                percentage = (processed_count / total_horses) * 100
                print(
                    f"Processed {
                        processed_count}/{total_horses} horses ({percentage:.2f}% complete)"
                )

        except Exception as e:
            print(f"Error processing horse_key {horse.horse_key}: {e}")

    print(f"Finished processing. Total horses processed: {processed_count}")


if __name__ == "__main__":
    fill_missing_parent_data()
