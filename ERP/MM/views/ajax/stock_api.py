from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.forms.models import model_to_dict
from ...models import Stock
import json
import pandas as pd

@login_required
def getByName(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponse(status=405)
    if request.method == 'POST':
        stock_name = request.POST['name']
        init = {'companyCode':'', 'pOrg':'', 'pGrp':''}
        if stock_name == '':
            return HttpResponse(json.dumps([{'fields': init}]))
        stocks = Stock.objects.filter(name__exact=stock_name)
        if len(stocks) != 1:
            return HttpResponse(json.dumps([{'message': '暂无该工厂相关数据，请重新确认！', 'fields': init}]))
        else:
            return HttpResponse(serializers.serialize('json', list(stocks)))
