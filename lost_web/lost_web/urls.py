# lost_web/urls.py
from django.contrib import admin
from django.urls import path
from found.views import (
    home_redirect, home, index, signup, login_view, submit_login,
    logout_view, report_view, listings, edit_report, delete_report,
    dashboard, delete_item
)

urlpatterns = [
    path('', home_redirect, name='home_redirect'),
    path('home/', home, name='home'),
    path('index/', index, name='index'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('submit_login/', submit_login, name='submit_login'),
    path('logout/', logout_view, name='logout'),
    path('report/', report_view, name='report'),
    path('listings/', listings, name='listings'),
    path('edit/<int:id>/', edit_report, name='edit_report'),
    path('delete/<int:id>/',delete_report, name='delete_report'),
     path('dashboard/',dashboard, name='dashboard'),
     path('delete/<int:item_id>/',delete_item, name='delete_item')
]
