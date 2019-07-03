from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('habit-manager/<int:pk>', views.habit_manager, name="habit-manager"),
    path('social/', views.social, name='social'),
    path('create-daily-record/<int:pk>', views.create_daily_record, name='create-daily-record'),
    path('edit-daily-record/<int:pk>', views.edit_daily_record, name='edit-daily-record'),
    path('habit-detail/<int:pk>', views.habit_detail, name="habit-detail"),
    path('create-habit/<int:pk>', views.create_habit, name='create-habit'),
]
