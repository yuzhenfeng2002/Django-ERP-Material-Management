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
            # startDate = datetime.datetime(
            #     year=int(dateInfo[2]), month=int(dateInfo[0]), day=int(dateInfo[1]),
            #     hour=0,minute=0,second=0, tzinfo=pytz.UTC
            # )
            # endDate = datetime.datetime(
            #     year=int(dateInfo[2]), month=int(dateInfo[0]), day=int(dateInfo[1]),
            #     hour=23,minute=59,second=59, tzinfo=pytz.UTC
            # )
            results: QuerySet = GoodReceipt.objects.filter(
                euser__uid__regex=uid, time__year=int(dateInfo[2]), 
                time__month=int(dateInfo[0]), time__day=int(dateInfo[1])
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

@login_required
def create_receipt(request: HttpRequest):
    post = request.POST
    po_id = getPkExact(post.get('po_id'), 'PO')
    oi_itemId = getPkExact(post.get('oi_id'), 'OI')
    actualQnty = int(post.get('actualQnty'))
    sType = post.get('sType')
    qualityScore = post.get('qualityScore')
    serviceScore = post.get('serviceScore')
    postTime = getDate(post.get('postTime'))
    time = getDate(post.get('time'))
    
    orderItem: OrderItem = OrderItem.objects.get(po__id__exact=po_id, itemId=oi_itemId)
    euser = EUser.objects.get(pk__exact=request.user.id)
    new_gr = GoodReceipt(
        actualQnty=actualQnty, sType=sType, time=time, postTime=postTime, orderItem=orderItem, euser=euser
    )
    try:
        new_gr.full_clean()
    except ValidationError as e:
        error_fields = list(e.error_dict.keys())
        return HttpResponse(json.dumps({'status':0, 'message':"表单填写错误！", 'fields':error_fields}))
    new_gr.save()
    orderItem.status = '1'
    orderItem.qualityScore = int(qualityScore) * 20
    orderItem.serviceScore = int(serviceScore) * 20
    orderItem.quantityScore = actualQnty / orderItem.quantity * 100
    dif = (time - orderItem.deliveryDate).days
    score = 0
    if dif <= 0: score=100
    elif 0 < dif < 7: score=80
    elif 7 <= dif < 15: score=60
    elif 15 <= dif < 30: score=40
    else: score= 20
    orderItem.ontimeScore = score
    orderItem.save()
    materialItem: MaterialItem = MaterialItem.objects.get(pk__exact=orderItem.meterialItem.id)

    new_stockHistory = StockHistory(
        item=materialItem, type='1', unrestrictUse=materialItem.unrestrictUse,
        blocked=materialItem.blocked, qltyInspection=materialItem.qltyInspection,
        time=time, 
    )
    try:
        new_stockHistory.full_clean()
    except ValidationError as e:
        error_fields = list(e.error_dict.keys())
        return HttpResponse(json.dumps({'status':0, 'message':"表单填写错误！", 'fields':error_fields}))
    if sType=='1': materialItem.blocked += actualQnty
    elif sType=='2': materialItem.qltyInspection += actualQnty
    elif sType=='3': materialItem.unrestrictUse += actualQnty
    materialItem.save()
    new_account = Account(
        sumAmount=orderItem.price * actualQnty, JEType='WE', postDate=postTime
    )
    try:
        new_account.full_clean()
    except ValidationError as e:
        error_fields = list(e.error_dict.keys())
        return HttpResponse(json.dumps({'status':0, 'message':"表单填写错误！", 'fields':error_fields}))
    new_account.save()
    accountDetail1 = AccountDetail(
        glAccount='200200', type='0', amount=orderItem.price * actualQnty, je=new_account
    )
    accountDetail2 = AccountDetail(
        glAccount='310000', type='1', amount=orderItem.price * actualQnty,
        gr=new_gr, je=new_account
    )
    try:
        accountDetail1.full_clean()
        accountDetail2.full_clean()
    except ValidationError as e:
        error_fields = list(e.error_dict.keys())
        return HttpResponse(json.dumps({'status':0, 'message':"表单填写错误！", 'fields':error_fields}))
    accountDetail1.save()
    accountDetail2.save()
    return HttpResponse(json.dumps({'status':1, 'message':"商品收据创建成功！收据编号为"+str(new_gr.id)+"。"}))
