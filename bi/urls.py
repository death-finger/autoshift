"""bi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AutoShift import views

urlpatterns = [
    path('', views.Schedule.as_view()),
    path('admin/', admin.site.urls),
    path('schedules/', views.Schedule.as_view()),
    path('arranges/', views.Arrange.as_view()),
    path('vacations/', views.Vacation.as_view()),
    path('shifts/', views.Shift.as_view()),
    path('staffs/', views.Staff.as_view()),
    path('vacations/', views.Vacation.as_view()),
    path('ajax_shift_mod/', views.ajax_shift_mod),
    path('ajax_shift_del/', views.ajax_shift_del),
    path('ajax_vacation_mod/', views.ajax_vacation_mod),
    path('ajax_vacation_del/', views.ajax_vacation_del),
    path('ajax_arrange_submit/', views.ajax_arrange_submit),
    path('ajax_staff_mod/', views.ajax_staff_mod),
    path('ajax_staff_del/', views.ajax_staff_del),
]
