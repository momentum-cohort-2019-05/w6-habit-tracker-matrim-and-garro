from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('habit-manager/<int:pk>', views.habit_manager, name="habit-manager"),
    path('social/', views.social, name='social'),
    path('habit-detail/<int:pk>', views.habit_detail, name="habit-detail"),

]
