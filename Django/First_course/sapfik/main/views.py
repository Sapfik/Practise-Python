from django.shortcuts import render
from django.http import HttpResponse   #Импортируем это, для того, чтобы у нас корректно отображался файл
# Здесь будет, основной материал (html, css)

# def index(request):   #Передаем обязательно парамерт request, иначе программа работать не будет
#     return HttpResponse('<h4>Проверка работы</h4>')

# def about(request):
#     return HttpResponse('<h4>Страница about</h4>')

# def filters(request):
#     return HttpResponse('<h4>Страница filters</h4>')

def index(request):   #Передаем обязательно парамерт request, иначе программа работать не будет
    return render(request, 'main/index.html')    

def about(request):
    return HttpResponse('<h4>Страница about</h4>')

def filters(request):
    return HttpResponse('<h4>Страница filters</h4>')