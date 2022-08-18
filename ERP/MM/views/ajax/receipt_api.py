from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.db.models import QuerySet, Sum, Count, F, Avg
from django.utils import timezone
import pytz
import json
import datetime

from ...models import *
from ..auxiliary import *

@login_required
def search_receipt(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponse(status=405)
    post = request.POST
    pk = post.get('pk')
    if pk == '' or pk is None:
        uid = getPk(post.get('uid'), 'U')
        date = post.get('date')
        if date == '':
            results: QuerySet = GoodReceipt.objects.filter(
                euser__uid__regex=uid
            )
        else:
            dateInfo = date.split('. ')
            # return HttpResponse(str(dateInfo))
            startDate = datetime.datetime(
                year=int(dateInfo[2]), month=int(dateInfo[0]), day=int(dateInfo[1]),
                hour=0,minute=0,second=0, tzinfo=pytz.UTC
            )
            endDate = datetime.datetime(
                year=int(dateInfo[2]), month=int(dateInfo[0]), day=int(dateInfo[1]),
                hour=23,minute=59,second=59, tzinfo=pytz.UTC
            )
            results: QuerySet = GoodReceipt.objects.filter(
                euser__uid__regex=uid, time__range=[startDate, endDate]
            )
        results_list = json.loads(serializers.serialize('json', list(results)))
        for i, r in enumerate(results):
            user: EUser = EUser.objects.get(pk__exact=r.euser.pk)
            orderItem: OrderItem = OrderItem.objects.get(pk__exact=r.orderItem.id)
            po: PurchaseOrder = PurchaseOrder.objects.get(pk__exact=orderItem.po.id)
            materialItem: MaterialItem = get_object_or_404(MaterialItem, id__exact=orderItem.meterialItem.id)
            stock: Stock = get_object_or_404(Stock, id__exact=materialItem.stock.id)
            material: Material = get_object_or_404(Material, id__exact=materialItem.material.id)
            results_list[i]['user'] = model_to_dict(user)
            results_list[i]['orderItem'] = model_to_dict(orderItem)
            results_list[i]['po'] = model_to_dict(po)
            results_list[i]['stock'] = model_to_dict(stock)
            results_list[i]['material'] = model_to_dict(material)
        return HttpResponse(json.dumps({'status':1, 'message':"商品收据检索成功！", 'gr':results_list}, default=str))
    else:
        pk = getPkExact(pk, 'GR')
        results: QuerySet = GoodReceipt.objects.filter(pk__exact=pk)
        if len(results) != 1:
            return HttpResponse(json.dumps({'status':0, 'message':"商品收据相关信息错误！"}))
        else:
            results_list = json.loads(serializers.serialize('json', list(results)))
            for i, r in enumerate(results):
                r: GoodReceipt
                user: EUser = EUser.objects.get(pk__exact=r.euser.pk)
                orderItem: OrderItem = OrderItem.objects.get(pk__exact=r.orderItem.id)
                po: PurchaseOrder = PurchaseOrder.objects.get(pk__exact=orderItem.po.id)
                materialItem: MaterialItem = get_object_or_404(MaterialItem, id__exact=orderItem.meterialItem.id)
                stock: Stock = get_object_or_404(Stock, id__exact=materialItem.stock.id)
                material: Material = get_object_or_404(Material, id__exact=materialItem.material.id)
                results_list[i]['user'] = model_to_dict(user)
                results_list[i]['orderItem'] = model_to_dict(orderItem)
                results_list[i]['po'] = model_to_dict(po)
                results_list[i]['stock'] = model_to_dict(stock)
                results_list[i]['material'] = model_to_dict(material)
            return HttpResponse(json.dumps({'status':1, 'message':"商品收据检索成功！", 'gr':results_list}, default=str))
