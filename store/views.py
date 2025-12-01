from django.shortcuts import render
from django.http import HttpResponse

def product_list(request):
    return HttpResponse("<h1>Інтернет-магазин комп'ютерних комплектуючих</h1>")