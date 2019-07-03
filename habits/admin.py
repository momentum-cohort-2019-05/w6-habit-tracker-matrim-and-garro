from django.contrib import admin
from habits.models import Habit, DailyRecord, Comment

# Register your models here.
admin.site.register(Habit)
admin.site.register(DailyRecord)
admin.site.register(Comment)

