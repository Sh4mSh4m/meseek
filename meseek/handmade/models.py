from django.db import models
from django.conf import settings

# Create your models here.

class BasketPlayers(models.Model):
    """
    Basket players table reset by referee every week
    """
    id = models.IntegerField(primary_key=True)
    player = models.CharField(max_length=100)
    models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

class UserWeeklyBasketScore(models.Model):
    """
    Weekly basket score
    """
    id = models.IntegerField(primary_key=True)
    player = models.ForeignKey(BasketPlayers,models.DO_NOTHING)
    success = models.IntegerField(default=0)
    fails = models.IntegerField(default=0)
    score_ratio = models.IntegerField(default=0)
    
    class Meta:
        managed = True
        db_table = 'user_weekly_basket'

class UserBasketScoreLogs(models.Model):
    """
    All time basket scores
    """
    id = models.IntegerField(primary_key=True)
    scoretable = models.TextField() 
    date = models.DateField(auto_now=True)
    
    class Meta:
        managed = True
        db_table = 'user_scorelog_basket'