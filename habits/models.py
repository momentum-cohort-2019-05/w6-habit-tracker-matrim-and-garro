from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Habit(models.Model):
    # label = models.CharField(max_length=200)
    # description = models.TextField(max_length=1000)
    verb = models.CharField(max_length=200)
    over = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        if self.over == True:
            over_str = "over"
        else:
            over_str = "under"
        return f'{self.verb} {over_str} {self.quantity} {self.unit} per day'
    
    def last_update(self):
        """returns the DailyRecord object of the last update"""
        return self.dailyrecord_set.order_by('-date').first()


class DailyRecord(models.Model):
    date = models.DateField(default=date.today)
    quantity = models.PositiveIntegerField(default=0)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.date}|{self.quantity}|{self.habit}"

class Comment(models.Model):
    pass

class Observer(models.Model):
    pass

