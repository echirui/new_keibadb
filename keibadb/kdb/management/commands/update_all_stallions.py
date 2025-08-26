from django.core.management.base import BaseCommand
from django.core.management import call_command
from kdb.models import Stallion

class Command(BaseCommand):
    help = 'Updates all Stallion records by re-scraping their information from netkeiba.com.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to update all Stallion records...'))

        all_stallions = Stallion.objects.all()
        total_stallions = all_stallions.count()

        if total_stallions == 0:
            self.stdout.write(self.style.SUCCESS("No Stallion records found to update. Exiting."))
            return

        self.stdout.write(f"Found {total_stallions} Stallion records to process.")

        processed_count = 0
        for stallion in all_stallions:
            try:
                self.stdout.write(f"Processing stallion_key: {stallion.horse_key}")
                # Call the register_stallion command for each stallion
                call_command('register_stallion', horse_key=stallion.horse_key, force_update=True)
                processed_count += 1

                if processed_count % 100 == 0:
                    percentage = (processed_count / total_stallions) * 100
                    self.stdout.write(f"Processed {processed_count}/{total_stallions} stallions ({percentage:.2f}% complete)")

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error processing stallion_key {stallion.horse_key}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Finished updating all Stallion records. Total stallions processed: {processed_count}"))
