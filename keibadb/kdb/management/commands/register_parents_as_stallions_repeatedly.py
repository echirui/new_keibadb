from django.core.management.base import BaseCommand
from django.core.management import call_command
from kdb.models import Stallion

class Command(BaseCommand):
    help = 'Registers the father and mother of each existing stallion as new stallions repeatedly.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to register parents as stallions repeatedly...'))

        processed_parent_keys = set() # To avoid processing the same parent_key multiple times across iterations

        for iteration in range(1, 21): # Repeat 20 times
            self.stdout.write(self.style.SUCCESS(f'--- Iteration {iteration}/20 ---'))
            
            all_stallions = Stallion.objects.all()
            total_stallions_in_iteration = all_stallions.count()
            self.stdout.write(f'Found {total_stallions_in_iteration} existing stallions for this iteration.')

            current_iteration_processed_count = 0
            for stallion in all_stallions:
                father_key = stallion.father_key
                mother_key = stallion.mother_key

                if father_key and father_key not in processed_parent_keys:
                    try:
                        self.stdout.write(f'Attempting to register father_key: {father_key} (father of {stallion.name})')
                        call_command('register_stallion', horse_key=father_key)
                        processed_parent_keys.add(father_key)
                        current_iteration_processed_count += 1
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f'Error processing father_key {father_key}: {e}'))
                
                if mother_key and mother_key not in processed_parent_keys:
                    try:
                        self.stdout.write(f'Attempting to register mother_key: {mother_key} (mother of {stallion.name})')
                        call_command('register_stallion', horse_key=mother_key)
                        processed_parent_keys.add(mother_key)
                        current_iteration_processed_count += 1
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f'Error processing mother_key {mother_key}: {e}'))
            
            self.stdout.write(self.style.SUCCESS(f'Finished iteration {iteration}. Processed {current_iteration_processed_count} new unique parent keys in this iteration.'))

        self.stdout.write(self.style.SUCCESS(f'Finished all 20 iterations. Total unique parents processed across all iterations: {len(processed_parent_keys)}'))
