from django.contrib import admin
from habits.models import Habit, DailyRecord

# Register your models here.
admin.site.register(Habit)
admin.site.register(DailyRecord)

