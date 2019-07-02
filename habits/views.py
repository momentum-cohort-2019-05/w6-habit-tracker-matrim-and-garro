from django.shortcuts import get_object_or_404, redirect, render
from habits.models import Habit, DailyRecord
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from datetime import datetime, timedelta
from habits.forms import CreateDailyRecord, EditDailyRecord

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

@login_required
def create_daily_record(request, pk):
    """creates a daily record using the pk of the parent habit"""
    habit = Habit.objects.get(pk=pk)
    today = datetime.today()
    today_url_arg = f"{today.year}-{today.month}-{today.day}"
    date_url_arg = request.GET.get('date', default=today_url_arg)
    ymd_list = date_url_arg.split("-")
    create_date = datetime(int(ymd_list[0]),int(ymd_list[1]),int(ymd_list[2]))

    if request.method == "POST":
        form = CreateDailyRecord(request.POST)
        # breakpoint()
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            new_record = DailyRecord(date=create_date, quantity=quantity, habit=habit)
            new_record.save()
        return redirect(to=habit_manager, pk=habit.owner.pk)
    else:
        form = CreateDailyRecord()
        return render(request, "create_daily_record.html", {
            'create_date' : create_date,
            'form' : form,
            'habit' : habit,
        })

@login_required
def edit_daily_record(request, pk):
    """edits a daily record using the pk of the DailyRecord object"""
    return render(request, "edit_daily_record.html", {})

def social(request):
    return render(request, "social.html", {
    })
