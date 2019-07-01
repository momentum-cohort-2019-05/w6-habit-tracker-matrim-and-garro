from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "home.html", {

    })

def habit_manager(request):
    return render(request, "habit_manager.html", {

    })

def social(request):
    return render(request, "social.html", {

    })
