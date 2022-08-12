from django import views
from django.contrib import admin
from django.urls import path, include
from pip import main

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('', include('main.urls'))   # Отслеживаем главную страницу 
                           # Когда мы прописываем к примекру main.urls мы делегируем все полномочия этому файлу (То есть в данном случае он будет отвечать за главную страницу)
]
