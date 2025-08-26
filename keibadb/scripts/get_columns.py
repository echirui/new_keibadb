from kdb.models import Horse

def run():
    for f in Horse._meta.fields:
        print(f.name)