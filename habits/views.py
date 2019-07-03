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
    last_week_dates = []
    DAYS = 7
    counter = 0
    while counter < DAYS:
        last_week_dates.append(date.today()-timedelta(days=counter))
        counter += 1
    last_week_of_records = []
    for day in last_week_dates:
        try:
            day_record = list_of_records.get(date=day)
            last_week_of_records.append(day_record)
        except:
            last_week_of_records.append(DailyRecord(date=day, quantity=(-1)))
        #     day.record = day_record
        # except:
        #     day.record = None
    # breakpoint()
        
    return render(request, "habit_detail.html", {
        'list_of_records' : list_of_records,
        'last_week_dates' : last_week_dates,
        'habit' : habit,
        'last_week_of_records' : last_week_of_records,
    })

@login_required
def create_daily_record(request, pk):
    """creates a daily record using the pk of the parent habit"""
    habit = Habit.objects.get(pk=pk)
    today = datetime.today()
    today_url_arg = f"{today.year}-{today.month}-{today.day}"
    date_url_arg = request.GET.get('date', default=today_url_arg)
    # breakpoint()
    ymd_list = date_url_arg.split("-")
    create_date = date(int(ymd_list[0]),int(ymd_list[1]),int(ymd_list[2]))

    if request.method == "POST":
        form = CreateDailyRecord(request.POST)
        # breakpoint()
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            new_record = DailyRecord(date=create_date, quantity=quantity, habit=habit)
            new_record.save()
        return redirect(to='habit-detail', pk=habit.pk)
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
    daily_record = DailyRecord.objects.get(pk=pk)
    # today = datetime.today()
    # today_url_arg = f"{today.year}-{today.month}-{today.day}"
    # date_url_arg = request.GET.get('date', default=today_url_arg)
    date_url_arg = request.GET.get('date')
    # breakpoint()
    ymd_list = date_url_arg.split("-")
    edit_date = date(int(ymd_list[0]),int(ymd_list[1]),int(ymd_list[2]))

    if request.method == "POST":
        form = EditDailyRecord(request.POST)
        # breakpoint()
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            daily_record.quantity = quantity
            daily_record.save()
        return redirect(to='habit-detail', pk=daily_record.habit.pk)
    else:
        form = EditDailyRecord()
        return render(request, "edit_daily_record.html", {
            'edit_date' : edit_date,
            'form' : form,
            'daily_record' : daily_record,
        })

def social(request):
    return render(request, "social.html", {
    })
