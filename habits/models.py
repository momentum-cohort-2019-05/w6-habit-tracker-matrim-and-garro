from django.db import models
from datetime import date

class Habit(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    

class Record(models.Model):
    pass

class Comment(models.Model):
    pass

class Observer(models.Model):
    pass

