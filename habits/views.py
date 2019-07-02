from django.shortcuts import render
from habits.models import Habit, DailyRecord
from django.contrib.auth.decorators import login_required
from datetime import date
from datetime import datetime, timedelta


# Create your views here.

@login_required
def home(request):
    return render(request, "home.html", {

    })

@login_required
def habit_manager(request, pk):
    list_of_habits = Habit.objects.filter(owner__pk=pk)
    today = date.today()
    updated_today = {}
    for habit in list_of_habits:
        if habit.last_update() is None:
            habit.updated_today = False
        elif habit.last_update().date == today:
            habit.updated_today = True
        else:
            habit.updated_today = False
    
    return render(request, "habit_manager.html", {
        'list_of_habits' : list_of_habits,
        'updated_today' : updated_today
    })

@login_required
def habit_detail(request, pk):
    habit = Habit.objects.get(id=pk)
    list_of_records = habit.dailyrecord_set.all().order_by('-date')
    # last_week = []
    # from_date = datetime.date.today() - datetime.timedelta(days=7)
    # orders = Order.objects.filter(created_at=from_date, dealer__executive__branch__user=user)
    # orders = orders.annotate(count=Count('id')).values('created_at').order_by('created_at')
    # if len(orders) < 7:
    #     orders_list = list(orders)
    #     dates = set([(datetime.date.today() - datetime.timedelta(days=i)) for i in range(6)])
    #     order_set = set([ord['created_at'] for ord in orders])
    #     for dt in (order_set - dates):
    #         orders_list.append({'created_at': dt, 'count': 0})
    #     orders_list = sorted(orders_list, key=lambda item: item['-created_at'])
    # else:
    # orders_list = orders
        
    return render(request, "habit_detail.html", {
        'list_of_records' : list_of_records,


    })


def social(request):
    return render(request, "social.html", {
    })
