from django.shortcuts import render
from django.http import HttpResponse
from .ajax import material_api

# Create your views here.

def test(request):
    return material_api.search_stock_history(request=request)
