from django.shortcuts import render
from habits.models import Habit, DailyRecord
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    return render(request, "home.html", {

    })

@login_required
def habit_manager(request, pk):
    list_of_habits = Habit.objects.filter(owner__pk=pk)



    return render(request, "habit_manager.html", {
        "list_of_habits": list_of_habits
    })

def social(request):
    return render(request, "social.html", {

    })
