from django.contrib import admin
from .models import Race
from .models import Jockey
from .models import Horse
from .models import Odds
from .models import Stallion
from .models import HorseRacing

# Register your models here.
admin.site.register(Race)
admin.site.register(Jockey)
admin.site.register(Horse)
admin.site.register(Odds)
admin.site.register(Stallion)
# admin.site.register(HorseRacing)
