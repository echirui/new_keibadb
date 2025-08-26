from django.db.models import Q
from kdb.models import Horse

def run():
    null_parents_count = Horse.objects.filter(Q(father_key__isnull=True) | Q(mother_key__isnull=True)).count()
    total_horses_count = Horse.objects.count()

    if total_horses_count > 0:
        percentage = (null_parents_count / total_horses_count) * 100
        print(f"Records with null father_key or mother_key: {null_parents_count}")
        print(f"Total records in Horse table: {total_horses_count}")
        print(f"Percentage of records with null parents: {percentage:.2f}%")
    else:
        print("No records found in Horse table.")