from django.db import models
from django.conf import settings



class UserJapaneseLevel(models.Model):
    """
    Nadeshiko users scores logs
    """
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    scores_level1 = models.CharField(max_length=100, default="0-0-0-0-1")
    scores_level2 = models.CharField(max_length=100, default="0-0-0-0-0")
    scores_level3 = models.CharField(max_length=100, default="0-0-0-0-0")

    class Meta:
        managed = True
        db_table = 'user_japanese_level'


class Hiragana(models.Model):
    """
    First level data
    """
    id = models.IntegerField(primary_key=True)
    char_jp = models.CharField(max_length=10)
    char_fr = models.CharField(max_length=10)
    level = models.IntegerField(default=1)

    class Meta:
        managed = True
        db_table = 'nadeshiko_hiragana'


class Katakana(models.Model):
    """
    Second level data
    """
    id = models.IntegerField(primary_key=True)
    char_jp = models.CharField(max_length=10)
    char_fr = models.CharField(max_length=10)
    level = models.IntegerField(default=2)

    class Meta:
        managed = True
        db_table = 'nadeshiko_katakana'


class LessonScan(models.Model):
    """
    Files uploaded for scans
    """
    description = models.CharField(max_length=255, blank=True)
    image = models.FileField(upload_to='scans/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Vocabulary(models.Model):
    """
    Main vocabulary table with levels
    """
    voc_jp = models.CharField(max_length=200)
    voc_fr = models.CharField(max_length=200)
    level = models.IntegerField(default=3)
    voc_type = models.CharField(max_length=200)


    class Meta:
        managed = True
        db_table = 'nadeshiko_vocabulary'


