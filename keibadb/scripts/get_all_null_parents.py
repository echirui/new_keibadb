import os
import django
from django.db.models import Q
from kdb.models import Horse

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keibadb.settings')
django.setup()

def run():
    horse_keys = Horse.objects.filter(Q(father_key__isnull=True) | Q(mother_key__isnull=True)).values_list('horse_key', flat=True).distinct()
    for key in horse_keys:
        print(key)

if __name__ == "__main__":
    run()
