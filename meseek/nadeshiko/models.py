from django.db import models
from django.conf import settings

# Nadeshiko users scores logs
class UserJapaneseLevel(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    scores_level1 = models.CharField(max_length=100, default="1-0-0-0-0")
    scores_level2 = models.CharField(max_length=100, default="0-0-0-0-0")
    scores_level3 = models.CharField(max_length=100, default="0-0-0-0-0")

    class Meta:
        managed = True
        db_table = 'user_japanese_level'

class Hiragana(models.Model):
    id = models.IntegerField(primary_key=True)
    char_jp = models.CharField(max_length=10)
    char_fr = models.CharField(max_length=10)
    level = models.IntegerField(default=1)

    class Meta:
        managed = True
        db_table = 'nadeshiko_hiragana'

class Katakana(models.Model):
    id = models.IntegerField(primary_key=True)
    char_jp = models.CharField(max_length=10)
    char_fr = models.CharField(max_length=10)
    level = models.IntegerField(default=2)

    class Meta:
        managed = True
        db_table = 'nadeshiko_katakana'