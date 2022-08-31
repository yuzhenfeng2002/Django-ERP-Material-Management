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
def search_invoice(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponse(status=405)
    post = request.POST
    pk = post.get('pk')
    if pk == '' or pk is None:
        uid = getPk(post.get('uid'), 'U')
        date = post.get('date')
        if date == '':
            results: QuerySet = Invoice.objects.filter(
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
            results: QuerySet = Invoice.objects.filter(
                euser__uid__regex=uid, postDate__year=int(dateInfo[2]), 
                postDate__month=int(dateInfo[0]), postDate__day=int(dateInfo[1])
            )
        results_list = json.loads(serializers.serialize('json', list(results)))
        for i, r in enumerate(results):
            user: EUser = EUser.objects.get(pk__exact=r.euser.pk)
            orderItem: OrderItem = OrderItem.objects.get(pk__exact=r.orderItem.id)
            po: PurchaseOrder = PurchaseOrder.objects.get(pk__exact=orderItem.po.id)
            materialItem: MaterialItem = get_object_or_404(MaterialItem, id__exact=orderItem.meterialItem.id)
            stock: Stock = get_object_or_404(Stock, id__exact=materialItem.stock.id)
            material: Material = get_object_or_404(Material, id__exact=materialItem.material.id)
            gr: GoodReceipt = GoodReceipt.objects.filter(orderItem__id__exact=orderItem.id).first()
            # results_list[i]['user'] = model_to_dict(user)
            results_list[i]['orderItem'] = model_to_dict(orderItem)
            results_list[i]['po'] = model_to_dict(po)
            results_list[i]['stock'] = model_to_dict(stock)
            results_list[i]['material'] = model_to_dict(material)
            results_list[i]['goodReceipt'] = model_to_dict(gr)
        return HttpResponse(json.dumps({'status':1, 'message':"发票检索成功！", 'gr':results_list}, default=str))
    else:
        pk = getPkExact(pk, 'GR')
        results: QuerySet = Invoice.objects.filter(pk__exact=pk)
        if len(results) != 1:
            return HttpResponse(json.dumps({'status':0, 'message':"发票编号错误！"}))
        else:
            results_list = json.loads(serializers.serialize('json', list(results)))
            for i, r in enumerate(results):
                r: Invoice
                user: EUser = EUser.objects.get(pk__exact=r.euser.pk)
                orderItem: OrderItem = OrderItem.objects.get(pk__exact=r.orderItem.id)
                po: PurchaseOrder = PurchaseOrder.objects.get(pk__exact=orderItem.po.id)
                materialItem: MaterialItem = get_object_or_404(MaterialItem, id__exact=orderItem.meterialItem.id)
                stock: Stock = get_object_or_404(Stock, id__exact=materialItem.stock.id)
                material: Material = get_object_or_404(Material, id__exact=materialItem.material.id)
                gr: GoodReceipt = GoodReceipt.objects.filter(orderItem__id__exact=orderItem.id).first()
                results_list[i]['user'] = model_to_dict(user)
                results_list[i]['orderItem'] = model_to_dict(orderItem)
                results_list[i]['po'] = model_to_dict(po)
                results_list[i]['stock'] = model_to_dict(stock)
                results_list[i]['material'] = model_to_dict(material)
                results_list[i]['goodReceipt'] = model_to_dict(gr)
            return HttpResponse(json.dumps({'status':1, 'message':"发票检索成功！", 'gr':results_list}, default=str))

@login_required
def create_invoice(request: HttpRequest):
    post = request.POST
    po_id = getPkExact(post.get('po_id'), 'PO')
    oi_itemId = int(post.get('oi_id'))
    sumAmount = int(post.get('sumAmount'))
    fiscal = post.get('fiscal')
    currency = post.get('currency')
    text = post.get('text')
    postDate = getDate(post.get('postDate'))
    invoiceDate = getDate(post.get('invoiceDate'))
    
    orderItems: QuerySet = OrderItem.objects.filter(po__id__exact=po_id, itemId__exact=oi_itemId)
    orderItem = orderItems.last()
    euser = EUser.objects.get(pk__exact=request.user.id)
    goodReceipts: QuerySet = GoodReceipt.objects.filter(orderItem__id=orderItem.id)
    goodReceipt = goodReceipts.last()
    actualAmount = goodReceipt.actualQnty * orderItem.price
    if sumAmount != actualAmount:
        return HttpResponse(json.dumps({'status':0, 'message':"表单总价填写错误，应为"+str(actualAmount)+"。", 'fields':['sumAmount']}))
    new_invoice = Invoice(
        fiscal=fiscal, sumAmount=sumAmount, currency=currency, text=text, invoiceDate=invoiceDate, postDate=postDate, orderItem=orderItem, euser=euser
    )
    try:
        new_invoice.full_clean()
    except ValidationError as e:
        error_fields = list(e.error_dict.keys())
        return HttpResponse(json.dumps({'status':0, 'message':"表单填写错误！", 'fields':error_fields}))
    new_invoice.save()
    orderItem.status = '2'
    orderItem.save()
    new_account = Account(
        sumAmount=sumAmount, JEType='KR', postDate=postDate
    )
    try:
        new_account.full_clean()
    except ValidationError as e:
        error_fields = list(e.error_dict.keys())
        return HttpResponse(json.dumps({'status':0, 'message':"表单填写错误！", 'fields':error_fields}))
    new_account.save()
    accountDetail1 = AccountDetail(
        glAccount='300000', type='1', amount=sumAmount, je=new_account
    )
    accountDetail2 = AccountDetail(
        glAccount='310000', type='0', amount=sumAmount, invoice=new_invoice, je=new_account
    )
    try:
        accountDetail1.full_clean()
        accountDetail2.full_clean()
    except ValidationError as e:
        error_fields = list(e.error_dict.keys())
        return HttpResponse(json.dumps({'status':0, 'message':"表单填写错误！", 'fields':error_fields}))
    accountDetail1.save()
    accountDetail2.save()
    return HttpResponse(json.dumps({'status':1, 'message':"发票创建成功!发票编号为"+str(new_invoice.id)+"。"}))

@login_required
def search_unpaied_invoice(request: HttpRequest):
    post = request.POST
    vid = getPkExact(post.get('vid'), 'V')
    status = post.get('status')
    status = 2
    invoices: QuerySet = Invoice.objects.filter(orderItem__status=status, orderItem__po__vendor__vid=vid)
    results_list = json.loads(serializers.serialize('json', list(invoices)))
    for i, r in enumerate(invoices):
        r: Invoice
        user: EUser = EUser.objects.get(pk__exact=r.euser.pk)
        orderItem: OrderItem = OrderItem.objects.get(pk__exact=r.orderItem.id)
        po: PurchaseOrder = PurchaseOrder.objects.get(pk__exact=orderItem.po.id)
        vendor: Vendor = get_object_or_404(Vendor, vid__exact=orderItem.po.vendor.vid)
        
        # results_list[i]['user'] = model_to_dict(user)
        results_list[i]['orderItem'] = model_to_dict(orderItem)
        results_list[i]['po'] = model_to_dict(po)
        results_list[i]['vendor'] = model_to_dict(vendor)
    if len(results_list) == 0:
        return HttpResponse(json.dumps({'status':0, 'message':"无相关发票！", 'gr':results_list}, default=str))
    return HttpResponse(json.dumps({'status':1, 'message':"发票检索成功！", 'gr':results_list}, default=str))

@login_required
def pay(request: HttpRequest):
    post = request.POST
    postDate = getDate(post.get('postDate'))
    invoiceIDList: str = post.get('invoiceIDList')
    invoiceIDList = invoiceIDList.lstrip('[').rstrip(',]')
    invoiceIDList = invoiceIDList.split(',')
    # return HttpResponse(str(invoiceIDList))
    account = Account(
        JEType='KZ', sumAmount=0, postDate=postDate
    )
    try:
        account.full_clean()
    except ValidationError as e:
        error_fields = list(e.error_dict.keys())
        return HttpResponse(json.dumps({'status':0, 'message':"表单填写错误！", 'fields':error_fields}))
    account.save()
    sum = 0
    for id in invoiceIDList:
        id = int(id)
        invoice: Invoice = Invoice.objects.get(id__exact=id)
        orderItem: OrderItem = OrderItem.objects.get(pk__exact=invoice.orderItem.id)
        orderItem.status = '3'
        orderItem.save()
        sum += invoice.sumAmount
        accountDetail1 = AccountDetail(
            glAccount='300000', type='0', amount=invoice.sumAmount, je=account, invoice=invoice
        )
        try:
            accountDetail1.full_clean()
        except ValidationError as e:
            error_fields = list(e.error_dict.keys())
            return HttpResponse(json.dumps({'status':0, 'message':"表单填写错误！", 'fields':error_fields}))
        accountDetail1.save()
    account.sumAmount = sum
    account.save()
    accountDetail2 = AccountDetail(
        glAccount='100000', type='1', amount=sum, je=account
    )
    try:
        accountDetail2.full_clean()
    except ValidationError as e:
        error_fields = list(e.error_dict.keys())
        return HttpResponse(json.dumps({'status':0, 'message':"表单填写错误！", 'fields':error_fields}))
    accountDetail2.save()
    return HttpResponse(json.dumps({'status':1, 'message':"付款成功！"}, default=str))