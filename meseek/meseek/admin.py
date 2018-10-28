from django.contrib import admin

# Register your models here.

from chat.models import Rappel
from nadeshiko.models import UserJapaneseLevel, Hiragana, Katakana, LessonScan, Vocabulary
from handmade.models import UserWeeklyBasketScore

admin.site.register(Rappel)
admin.site.register(UserJapaneseLevel)
admin.site.register(Hiragana)
admin.site.register(Katakana)
admin.site.register(LessonScan)
admin.site.register(Vocabulary)
admin.site.register(UserWeeklyBasketScore)
