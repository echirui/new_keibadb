from django.db.models import Q
from kdb.models import Horse

def run():
    horse_keys = Horse.objects.filter(Q(father_key__isnull=True) | Q(mother_key__isnull=True)).values_list('horse_key', flat=True)
    for key in horse_keys:
        print(key)