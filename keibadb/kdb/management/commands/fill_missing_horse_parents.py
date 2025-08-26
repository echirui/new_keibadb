from django.core.management.base import BaseCommand
from django.db.models import Q
from django.core.management import call_command
from kdb.models import Horse

class Command(BaseCommand):
    help = 'Fills missing father_key or mother_key for Horse records by scraping horse data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to fill missing horse parent data...'))

        horses_to_process = Horse.objects.filter(Q(father_key__isnull=True) | Q(mother_key__isnull=True))
        total_horses = horses_to_process.count()

        self.stdout.write(f"Found {total_horses} horses with missing parent data.")

        if total_horses == 0:
            self.stdout.write(self.style.SUCCESS("No horses to process. Exiting."))
            return

        processed_count = 0
        for horse in horses_to_process:
            try:
                self.stdout.write(f"Processing horse_key: {horse.horse_key}")
                call_command('scrape_horse', horse_id=horse.horse_key)
                processed_count += 1

                if processed_count % 100 == 0:
                    percentage = (processed_count / total_horses) * 100
                    self.stdout.write(f"Processed {processed_count}/{total_horses} horses ({percentage:.2f}% complete)")

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error processing horse_key {horse.horse_key}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Finished processing. Total horses processed: {processed_count}"))
