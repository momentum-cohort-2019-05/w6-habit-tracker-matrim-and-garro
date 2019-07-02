from django import forms
from habits.models import Habit, DailyRecord

class CreateDailyRecord(forms.Form):
    quantity = forms.IntegerField()

class EditDailyRecord(forms.Form):
    quantity = forms.IntegerField()
