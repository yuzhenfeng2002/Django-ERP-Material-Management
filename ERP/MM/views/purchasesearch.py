import json
from django.core import serializers
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.decorators import login_required
from django import forms
import datetime
from django.views.decorators.csrf import csrf_exempt


from ..models import EUser, Material, MaterialItem, Stock,PurchaseRequisition,RequisitionItem
from .auxiliary import *



class PurchaseOrderForm(forms.Form):
    mid = forms.CharField(label="物料编码", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    plant = forms.CharField(label="工厂编码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    itemId = forms.CharField(label="条目编码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    estimatedPrice = forms.CharField(label="预估价格", max_length=256,widget=forms.TextInput(attrs={'class': 'form-control'}))
    deliveryDate = forms.CharField(label="送货时间", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    currency = forms.CharField(label="货币", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    quantity= forms.CharField(label="数量", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))



class modifypr(forms.Form):
    text = forms.CharField(label="备注", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))



def search(request):
    if request.method == "GET":
        requisitionItems = RequisitionItem.objects.all()
        PurchaseOrder_form = PurchaseOrderForm()
        print(requisitionItems)# 获取我们的数据库信息到names里
        return render(request, '../templates/purchaserequisition/search.html', locals())
    if request.method == "POST":
        PurchaseOrder_form = PurchaseOrderForm(request.POST)





"""
重写方法
"""
from datetime import date, datetime

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)



def getdata(request):
    search_kw = request.GET.get('search_kw')
    search_kw_1 = request.GET.get('search_kw_1')
    print(222)
    page_size = int(request.GET['pageSize'])
    page_number = int(request.GET['pageNumber'])
    print("page_size:",page_size)
    print("page_number:",page_number)
    print("number:",page_number)
    print('search_kw的值为：%s' % search_kw)
    print('search_kw_1的值为：%s' % search_kw_1)
    if search_kw=="" and search_kw_1=="":
        requisitionItems = RequisitionItem.objects.all()
        requisitionItems_json_1= RequisitionItem.objects.all()[(page_number-1)*page_size:page_number*page_size].values("id","itemId", "estimatedPrice", "currency",
                                                                "deliveryDate",
                                                                "meterial_id","pr_id","status")
        print(requisitionItems.count())
        print("reque:",requisitionItems_json_1)
        datalist = {
            "total": requisitionItems.count(),
            "rows": list(requisitionItems_json_1)
        }
        print("datalist:",datalist)
        return HttpResponse(json.dumps(datalist, cls=ComplexEncoder))
    else:
        requisitionItems = RequisitionItem.objects.filter(pr_id = search_kw,itemId=search_kw_1)
        requisitionItems_json_1= RequisitionItem.objects.filter(pr_id = search_kw,itemId=search_kw_1)[(page_number-1)*page_size:page_number*page_size].values("id","itemId", "estimatedPrice", "currency",
                                                                "deliveryDate",
                                                                "meterial_id","pr_id","status")
        print(requisitionItems.count())
        print("reque:",requisitionItems_json_1)
        datalist = {
            "total": requisitionItems.count(),
            "rows": list(requisitionItems_json_1)
        }
        print("datalist:",datalist)
        return HttpResponse(json.dumps(datalist, cls=ComplexEncoder))



@csrf_exempt
def query_article(request):
    id = request.POST['id']
    print("id:",id)
    requisitionItems = RequisitionItem.objects.all()
    reque = RequisitionItem.objects.get(pr_id = id)
    print(reque)
    print(requisitionItems)
    data = {
        'ret': True,
        'data': {
            'title': " ",
            'content': " "
        }
    }

    return HttpResponse(json.dumps(data), content_type='application/json')






"""
3.1.2
查找采购申请与物料信息
"""
def modifygetdata(request: HttpRequest, pk):

    reque = RequisitionItem.objects.filter(pr_id=pk).values("itemId", "estimatedPrice", "currency",
                                                            "deliveryDate",
                                                            "meterial_id", "pr_id", "status","meterial__materialitem__sloc"
                                                            ,"meterial__materialitem__stock_id")
    reque = list(reque)
    return HttpResponse(reque)




"""
3.1.2
修改采购单
"""
def modify_pr(request: HttpRequest, pk):
    if request.method == "GET":
        PurchaseOrder_form = modifypr()
        reque = PurchaseRequisition.objects.filter(id=pk).values()
        reque = list(reque)
        return render(request, '../templates/purchaserequisition/modify2.html', locals())
    if request.method == "POST":
        PurchaseOrder_form = modifypr()
        PurchaseOrderinfo = modifypr(request.POST)
        print(PurchaseOrderinfo)
        if PurchaseOrderinfo.is_valid():
            text = PurchaseOrderinfo.cleaned_data['text']
            pr= PurchaseRequisition.objects.filter(id=pk).update(text = text)
            if pr:
                message = "修改成功"
                return render(request, '../templates/purchaserequisition/modify2.html', locals())
            else:
                message = "修改失败"
                return render(request, '../templates/purchaserequisition/modify2.html', locals())






"""
3.1.2
修改采购申请(请购条目)
"""
def modify_item(request: HttpRequest, pk):
    if request.method == "GET":
        pk = str(int(pk))
        print("pk:", pk)
        reque = RequisitionItem.objects.filter(id=pk).values("itemId", "estimatedPrice", "currency",
                                                            "deliveryDate",
                                                            "meterial_id","pr_id","status")
        datalist = {
            "total": 1,
            "rows": list(reque)
        }
        print(datalist)
        reque = list(reque)
        return render(request, '../templates/purchaserequisition/modify.html', locals())
    if request.method == "POST":
        mid = request.POST.get("mid")
        plant = request.POST.get("plant")
        itemId = request.POST.get("itemId")
        estimatedPrice = request.POST.get("estimatedPrice")
        currency = request.POST.get("currency")
        quantity = request.POST.get("quantity")
        deliveryDate = request.POST.get("deliveryDate")
        quotation = RequisitionItem.objects.filter(id=pk).update(
            meterial_id=mid,
            estimatedPrice=estimatedPrice,
            currency=currency,
            quantity=quantity,
            itemId=itemId,
            deliveryDate=deliveryDate)
        if quotation:
            message = "修改成功"
            return render(request, '../templates/purchaserequisition/modify.html', locals())
        else:
            message = "修改失败"
            return render(request, '../templates/purchaserequisition/modify.html', locals())
    else:
        return render(request, '../templates/purchaserequisition/modify.html', locals())


