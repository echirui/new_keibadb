from django.core.management.base import BaseCommand
from django.db.models import Q
from django.core.management import call_command
from kdb.models import Stallion


class Command(BaseCommand):
    help = "Fills missing father_key or mother_key for Stallion records by scraping horse data."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                "Starting to fill missing stallion parent data...")
        )

        stallions_to_process = Stallion.objects.filter(
            Q(father_key__isnull=True) | Q(mother_key__isnull=True)
        )
        total_stallions = stallions_to_process.count()

        self.stdout.write(
            f"Found {total_stallions} stallions with missing parent data."
        )

        if total_stallions == 0:
            self.stdout.write(self.style.SUCCESS(
                "No stallions to process. Exiting."))
            return

        processed_count = 0
        for stallion in stallions_to_process:
            try:
                self.stdout.write(f"Processing stallion_key: {
                                  stallion.horse_key}")
                call_command("register_stallion", horse_key=stallion.horse_key)
                processed_count += 1

                if processed_count % 100 == 0:
                    percentage = (processed_count / total_stallions) * 100
                    self.stdout.write(
                        f"Processed {processed_count}/{total_stallions} stallions ({
                            percentage:.2f}% complete)"
                    )

            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(
                        f"Error processing stallion_key {
                            stallion.horse_key}: {e}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Finished processing. Total stallions processed: {
                    processed_count}"
            )
        )
