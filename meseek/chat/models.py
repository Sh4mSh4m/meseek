from django.db import models

# Create your models here.


class Rappel(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    rappel = models.TextField()
    class Meta:
        managed = True
        db_table = 'rappel'