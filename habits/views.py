from django.shortcuts import get_object_or_404, redirect, render
from habits.models import Habit, DailyRecord, Comment
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from datetime import datetime, timedelta
from habits.forms import CreateDailyRecord, EditDailyRecord, CreateHabit, AddBuddy, AddComment
from django.contrib.auth.models import User


# Create your views here.

@login_required
def home(request):
    return render(request, "home.html", {

    })

@login_required
def habit_manager(request, pk):
    yesterday = date.today() - timedelta(days=1)
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
        'updated_today' : updated_today,
        'yesterday' : yesterday,
    })

@login_required
def habit_detail(request, pk):
    interval_str = request.GET.get('interval', default='7')
    habit = Habit.objects.get(id=pk)
    list_of_records = habit.dailyrecord_set.all().order_by('-date')
    last_week_dates = []
    DAYS = int(interval_str)

    # data aggregations 
    # AREA FOR IMPROVEMENT - should be in database
    # all time best day
    if habit.over:
        all_time_best = habit.dailyrecord_set.all().order_by('-quantity').first()
    else:
        all_time_best = habit.dailyrecord_set.all().order_by('quantity').first()
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
    #avg day this interval
    total = 0
    for day_record in last_week_of_records:
        if day_record.quantity > 0:
            total += day_record.quantity
    interval_average = round((total / DAYS),2)

    return render(request, "habit_detail.html", {
        'list_of_records' : list_of_records,
        'last_week_dates' : last_week_dates,
        'habit' : habit,
        'last_week_of_records' : last_week_of_records,
        'all_time_best' : all_time_best,
        'interval_average' : interval_average,
        'DAYS' : DAYS,
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

@login_required
def create_habit(request, pk):
    """creates a new habit for the owner at pk"""
    owner = User.objects.get(pk=pk)

    if request.method == "POST":
        form = CreateHabit(request.POST)
        # breakpoint()
        if form.is_valid():
            verb = form.cleaned_data['verb']
            over = form.cleaned_data['over']
            quantity = form.cleaned_data['quantity']
            unit = form.cleaned_data['unit']
            new_habit = Habit(owner=owner, verb=verb, over=over, quantity=quantity, unit=unit)
            new_habit.save()
        return redirect(to='habit-manager', pk=request.user.pk)
    else:
        form = CreateHabit()
        return render(request, "create_habit.html", {
            'owner' : owner,
            'form' : form
        })

@login_required
def add_buddy(request,pk):
    habit = Habit.objects.get(pk=pk)
    current_buddies = habit.buddies.all()
    message = ''
    if request.method == 'POST':
        form = AddBuddy(request.POST)
        if form.is_valid():
            username = form.cleaned_data['buddy']
            try:
                buddy_user = User.objects.get(username=username)
                if buddy_user in current_buddies:
                    message = f"{username} is already a buddy for this habit."
                elif buddy_user != request.user:
                    habit.buddies.add(buddy_user)
                    habit.save()
                    current_buddies = habit.buddies.all()
                    message = f'{username} added sucessfully.'
                else:
                    message = "You can't be your own buddy."
            except:
                message = f'{username} not found.'
        return render(request, "add_buddy.html", {
            'habit' : habit,
            'form' : form,
            'message' : message,
            'current_buddies' : current_buddies
        })
    else:
        form = AddBuddy()
        return render(request, "add_buddy.html", {
            'habit' : habit,
            'form' : form,
            'message' : message,
            'current_buddies' : current_buddies
        })

@login_required
def social(request,pk):
    user = User.objects.get(pk=pk)
    habit_buddy_list = user.habits.all()
    # breakpoint()
    return render(request, "social.html", {
        'user' : user,
        'habit_buddy_list' : habit_buddy_list,
    })

@login_required
def add_comment(request,pk):
    daily_record = DailyRecord.objects.get(pk=pk)
    habit = daily_record.habit
    if request.method == 'POST':
        form = AddComment(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            new_comment = Comment(user=request.user,content=content,target_record=daily_record)
            new_comment.save()
        return redirect(to='habit-detail', pk=habit.pk)
    else:
        form = AddComment()
        return render(request, "add_comment.html", {
            'daily_record' : daily_record,
            'form' : form,
            'habit' : habit,
        })


@login_required
def delete_record(request, pk):
    record = DailyRecord.objects.get(id=pk)
    if request.user == record.habit.owner:
        record.delete()
    return redirect(to="habit-detail", pk=habit.pk)

@login_required
def delete_habit(request,pk):
    """deletes a habit"""
    habit = Habit.objects.get(pk=pk)
    if request.user == habit.owner:
        habit.delete()
    return redirect(to='habit-manager', pk=request.user.pk)
