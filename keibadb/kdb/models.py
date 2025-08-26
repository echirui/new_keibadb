from django.db import models
from datetime import date

# Create your models here.


class Race(models.Model):
    race_id = models.CharField(max_length=12)
    race_name = models.CharField(max_length=255)
    date = models.DateField()
    details = models.TextField()
    debut = models.BooleanField(default=False)
    race_class = models.CharField(max_length=255)
    surface = models.CharField(max_length=255)
    distance = models.IntegerField()
    direction = models.CharField(max_length=255)
    track_condition = models.CharField(max_length=255)
    weather = models.CharField(max_length=255)
    start_at = models.CharField(max_length=255, blank=True)
    venue_code = models.CharField(max_length=255)
    venue = models.CharField(max_length=255, db_index=True)
    lap = models.CharField(max_length=255)
    pace = models.CharField(max_length=255)

    def __str__(self):
        return self.race_name

    class Meta:
        db_table = 'kdb_race'


class Jockey(models.Model):
    name = models.CharField(max_length=255)
    birth_year = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'kdb_jockey'


class Horse(models.Model):
    horse_key = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    birth_year = models.CharField(max_length=12, null=True, blank=True)
    coat_color = models.CharField(max_length=255, null=True, blank=True)
    father_key = models.CharField(max_length=10, null=True, blank=True)
    mother_key = models.CharField(max_length=10, null=True, blank=True)
    relatives = models.CharField(max_length=255, null=True, blank=True)
    prize = models.CharField(max_length=255, null=True, blank=True)
    owner_name = models.CharField(max_length=255, null=True, blank=True)
    owner_key = models.CharField(max_length=8, null=True, blank=True)
    farm_name = models.CharField(max_length=255, null=True, blank=True)
    farm_key = models.CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'kdb_horse'


class Odds(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    win_odds = models.JSONField(null=True, blank=True)
    show_odds = models.JSONField(null=True, blank=True)
    quinella_odds = models.JSONField(null=True, blank=True)
    quinella_place_odds = models.JSONField(null=True, blank=True)
    trio_odds = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'kdb_odds'


class Stallion(models.Model):
    horse_key = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    father_key = models.CharField(max_length=10, null=True, blank=True)
    mother_key = models.CharField(max_length=10, null=True, blank=True)
    birth_year = models.CharField(max_length=12, null=True, blank=True)
    sex = models.CharField(max_length=255, null=True, blank=True)
    prize = models.CharField(max_length=255, null=True, blank=True)
    trainer_name = models.CharField(max_length=255, null=True, blank=True)
    trainer_key = models.CharField(max_length=7, null=True, blank=True)
    owner_name = models.CharField(max_length=255, null=True, blank=True)
    owner_key = models.CharField(max_length=8, null=True, blank=True)
    farm_name = models.CharField(max_length=255, null=True, blank=True)
    farm_key = models.CharField(max_length=7, null=True, blank=True)
    race_text = models.CharField(max_length=255, null=True, blank=True)
    relatives = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'kdb_stallion'


class HorseRacing(models.Model):
    race_id = models.CharField(max_length=12, default='')
    horse = models.ForeignKey(Horse, on_delete=models.CASCADE)
    horse_key = models.CharField(max_length=10, default='')
    jockey = models.ForeignKey(Jockey, on_delete=models.CASCADE)
    horse_number = models.IntegerField(default=0)
    running_time = models.CharField(max_length=255, default='')
    odds = models.FloatField(default=0.0)
    passing_order = models.CharField(max_length=255, db_index=True, default='')
    finish_position = models.IntegerField(db_index=True, default=0)
    weight = models.IntegerField(blank=True, null=True)
    weight_change = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=255, default='')
    age = models.IntegerField(default=0)
    handicap = models.FloatField(default=0.0)
    final_600m_time = models.FloatField(blank=True, null=True)
    popularity = models.IntegerField(default=0)
    race_name = models.CharField(max_length=255, default='')
    date = models.DateField(default=date.today)
    details = models.TextField(default='')
    debut = models.BooleanField(default=False)
    race_class = models.CharField(max_length=255, default='')
    surface = models.CharField(max_length=255, default='')
    distance = models.IntegerField(default=0)
    direction = models.CharField(max_length=255, default='')
    track_condition = models.CharField(max_length=255, default='')
    weather = models.CharField(max_length=255, default='')
    start_at = models.CharField(max_length=255, blank=True, default='')
    venue_code = models.CharField(max_length=255, default='')
    venue = models.CharField(max_length=255, db_index=True, default='')
    lap = models.CharField(max_length=255, default='')
    pace = models.CharField(max_length=255, default='')
    training_center = models.CharField(max_length=4, default='')
    trainer_name = models.CharField(max_length=255, default='')
    owner = models.CharField(max_length=255, default='')
    farm = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'kdb_horseracing'
