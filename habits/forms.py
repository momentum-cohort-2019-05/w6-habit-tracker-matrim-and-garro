from django import forms
from habits.models import Habit, DailyRecord

class CreateDailyRecord(forms.Form):
    quantity = forms.IntegerField()

class EditDailyRecord(forms.Form):
    quantity = forms.IntegerField()

class CreateHabit(forms.Form):
    verb = forms.CharField(max_length=50)
    over = forms.BooleanField(required=False)
    quantity = forms.IntegerField()
    unit = forms.CharField(max_length=50)

class AddBuddy(forms.Form):
    buddy = forms.CharField(max_length=100)
