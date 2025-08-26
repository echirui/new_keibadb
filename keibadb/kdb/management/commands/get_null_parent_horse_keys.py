from django.core.management.base import BaseCommand
from django.db.models import Q
from kdb.models import Horse

class Command(BaseCommand):
    help = 'Lists horse_keys for Horse records with null father_key or mother_key.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Fetching horse_keys with missing parent data...'))
        horse_keys = Horse.objects.filter(Q(father_key__isnull=True) | Q(mother_key__isnull=True)).values_list('horse_key', flat=True).distinct()
        
        if not horse_keys:
            self.stdout.write(self.style.SUCCESS("No horse_keys found with missing parent data."))
            return

        for key in horse_keys:
            self.stdout.write(key)
        
        self.stdout.write(self.style.SUCCESS(f"Found {len(horse_keys)} horse_keys with missing parent data."))
