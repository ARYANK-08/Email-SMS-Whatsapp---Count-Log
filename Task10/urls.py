from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.send_email, name='send_email'),
    path('add_email/', views.add_email_ids, name='add_email'),
    path('add_email1/' , views.email_count, name='count_email_ids'),
    path('log/', views.send_email , name='logmail'),
    path('send-sms/', views.send_sms, name='send_sms'),

]