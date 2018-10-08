from django.db import models
from django.conf import settings

# Create your models here.
class UserWeeklyBasketScore(models.Model):
    """
    Weekly basket score
    """
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    success = models.IntegerField(default=0)
    fails = models.IntegerField(default=0)
    
    class Meta:
        managed = True
        db_table = 'user_weekly_basket'

class UserBasketScoreLog(models.Model):
    """
    All time basket scores
    """
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    date = models.IntegerField(default=0)
    
    class Meta:
        managed = True
        db_table = 'user_weekly_basket'