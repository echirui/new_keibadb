from django.core.management.base import BaseCommand
from kdb.models import Stallion

class Command(BaseCommand):
    help = 'Displays N generations of a stallion\'s pedigree in a tree structure.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--horse_key',
            type=str,
            help='The horse_key of the stallion to display pedigree for.',
            required=True
        )
        parser.add_argument(
            '--generations',
            type=int,
            help='Number of generations to display.',
            default=3
        )

    def handle(self, *args, **options):
        horse_key = options['horse_key']
        generations = options['generations']

        pedigree_data = {}

        def fetch_pedigree(key, current_generation):
            if not key or current_generation > generations:
                return None

            if key in pedigree_data:
                return pedigree_data[key]

            try:
                stallion = Stallion.objects.get(horse_key=key)
                data = {
                    'name': stallion.name,
                    'key': key,
                    'father': fetch_pedigree(stallion.father_key, current_generation + 1),
                    'mother': fetch_pedigree(stallion.mother_key, current_generation + 1)
                }
                pedigree_data[key] = data
                return data
            except Stallion.DoesNotExist:
                return None
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error fetching pedigree for {key}: {e}"))
                return None

        def print_pedigree(key, prefix="", is_last=False, is_father=False):
            if not key or key not in pedigree_data or not pedigree_data[key]:
                return

            horse = pedigree_data[key]
            connector = "└── " if is_last else "├── "
            
            if prefix: # Only add "Father:" or "Mother:" for subsequent generations
                if is_father:
                    self.stdout.write(f"{prefix}{connector}Father: {horse['name']} ({key})")
                else:
                    self.stdout.write(f"{prefix}{connector}Mother: {horse['name']} ({key})")
            else: # This is the root stallion
                self.stdout.write(f"{horse['name']} ({key})")

            child_prefix = prefix + ("    " if is_last else "│   ")
            
            # Fetch and print father
            if horse['father']:
                print_pedigree(horse['father']['key'], child_prefix, is_last=False, is_father=True)
            # Fetch and print mother
            if horse['mother']:
                print_pedigree(horse['mother']['key'], child_prefix, is_last=True, is_father=False)


        # Start fetching from Deep Impact
        deep_impact_key = '2002100816'
        self.stdout.write(f"Fetching pedigree for {deep_impact_key} for {generations} generations...")
        fetch_pedigree(deep_impact_key, 1)
        
        self.stdout.write("\n--- Pedigree Tree ---")
        print_pedigree(deep_impact_key)