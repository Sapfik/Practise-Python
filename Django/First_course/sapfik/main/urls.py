from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),  #Если пользователь перешел на главную страницу, то мы обращаемся к такому то методы в файле views.py
    path('about', views.about),   #Если пользователь перешел на страницу about, то мы выводим какой-то html
    path('about/filters', views.filters)  #Если пользователь перешел на страницу about/filters, то мы выводим какой-то html
]
