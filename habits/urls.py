from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('habit-manager/', views.habit_manager, name="habit-manager"),
    path('social/', views.social, name='social')
]