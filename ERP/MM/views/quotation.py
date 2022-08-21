import json
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.decorators import login_required
from django import forms
import datetime

from django.views.decorators.csrf import csrf_exempt

from ..models import EUser, Material, MaterialItem, Stock,PurchaseRequisition,RequisitionItem,Quotation,Vendor,OrderItem
from .auxiliary import *


class QuotationForm(forms.Form):
    euserid = forms.CharField(label="创建者ID", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    vendorvid = forms.CharField(label="供应商ID", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    riid = forms.CharField(label="参考请购条目ID", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mid = forms.CharField(label="物料条目", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    deadline = forms.CharField(label="截止日期", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    quantity = forms.CharField(label="数量", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    deliveryDate = forms.CharField(label="送货时间", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    collNo = forms.CharField(label="集合码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.CharField(label="报价", max_length=256,widget=forms.TextInput(attrs={'class': 'form-control'}))
    currency = forms.CharField(label="货币", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    validTime = forms.CharField(label="报价有效期", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))




class ModifyquotationForm(forms.Form):
    price = forms.CharField(label="报价", max_length=256,widget=forms.TextInput(attrs={'class': 'form-control'}))
    currency = forms.CharField(label="货币", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    validTime = forms.CharField(label="报价有效期", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))




class VendormodifyquotationForm(forms.Form):
    deadline = forms.CharField(label="截止日期", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    quantity = forms.CharField(label="数量", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    deliveryDate = forms.CharField(label="送货时间", max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    collNo = forms.CharField(label="集合码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    rej = forms.CharField(label="拒绝情况", max_length=1, widget=forms.TextInput(attrs={'class': 'form-control'}))



class searchquotationForm(forms.Form):
    collNo = forms.CharField(label="集合码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    riid = forms.CharField(label="参考请购条目ID", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mid = forms.CharField(label="物料条目", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))




def get_material(request):
    if request.method == "GET":
        PurchaseOrder_form = QuotationForm()
        return render(request, '../templates/quotation/insert.html',locals())
    if request.method == "POST":
        Quotation_form = QuotationForm()
        mid = request.POST.get("wuliao")
        plant = request.POST.get("factory")
        try:
            materials = MaterialItem.objects.get(
                material=mid, stock=plant
            )
            print(materials.id)
            id = materials.id
            return render(request, '../templates/quotation/insert.html', locals())
        except ObjectDoesNotExist:
            memessage = "信息不存在"
            return render(request, '../templates/quotation/insert.html', locals())




"""
3.3.1 1. FUNCTION(筛选询价单2)
"""
def search(request):
    if request.method == "GET":
        Quotation_form= searchquotationForm()
        return render(request, '../templates/quotation/search.html',locals())
    if request.method == "POST":
        Quotation_form = searchquotationForm()
        quotation_form = searchquotationForm(request.POST)
        if quotation_form.is_valid():
            riid = request.POST.get("riid")
            mid = request.POST.get("mid")
            collNo = request.POST.get("collNo")
            quotation = Quotation.objects.filter(ri_id=riid,collNo=collNo).values()
            quotation = list(quotation)
            material = MaterialItem.objects.filter(id=mid).values()
            print(quotation)
            print(material)
            return render(request, '../templates/quotation/search.html', locals())




"""
3.3.1  2. FUNCTION(根据集合码查找询价单)
"""
def getquotebycol(request: HttpRequest, pk):
    if request.method == "GET":
        pk = str(int(pk))
        print("pk:", pk)
        quotation = Quotation.objects.filter(collNo=pk).values("id","rej")
        quotation = list(quotation)
        return render(request, '../templates/quotation/getquotebycol.html',locals())






def get_requisitionItem(request):
    if request.method == "GET":
        PurchaseOrder_form = QuotationForm()
        return render(request, '../templates/quotation/insert.html',locals())
    if request.method == "POST":
        Quotation_form = QuotationForm()
        mid = request.POST.get("qinggou")
        plant = request.POST.get("tiaomu")
        try:
            materials = RequisitionItem.objects.get(
                pr_id=mid, itemId=plant
            )
            reid = materials.id
            return render(request, '../templates/quotation/insert.html', locals())
        except ObjectDoesNotExist:
            remessage = "信息不存在"
            return render(request, '../templates/quotation/insert.html', locals())




"""
FUNCTION(创建询价单)
"""

def insert(request):
    if request.method == "GET":
        return render(request, '../templates/quotation/insert.html',locals())
    if request.method == "POST":
        euserid = request.POST.get("euserid")
        vendorvid = request.POST.get("vendorvid")
        riid = request.POST.get("riid")
        mid = request.POST.get("mid")
        collNo = request.POST.get("collNo")
        deadline = request.POST.get("deadline")
        quantity = request.POST.get("quantity")
        deliveryDate = request.POST.get("deliveryDate")
        price = request.POST.get("price")
        currency = request.POST.get("currency")
        validTime = request.POST.get("validTime")
        now_time = datetime.datetime.now()
        quotation = Quotation.objects.create(deadline=deadline,
                                             quantity=quantity,
                                             ri_id=riid,
                                             vendor_id=vendorvid,
                                             euser_id=euserid,
                                             time=now_time,
                                             validTime=validTime,
                                             currency=currency,
                                             price=price,
                                             collNo=collNo,
                                             deliveryDate=deliveryDate,
                                             rej=0
                                             )
        if quotation:
            insertmessage = "创建成功"
            return render(request, '../templates/quotation/insert.html', locals())
        else:
            insertmessage = "创建失败"
            return render(request, '../templates/quotation/insert.html', locals())







"""

"""
def selectone(request: HttpRequest, pk):
    if request.method == "GET":
        pk = str(int(pk))
        print("pk:", pk)
        requisitionItems_json_1= Quotation.objects.all()
        return render(request, '../templates/quotation/insert.html',locals())




"""
录入供应商报价
"""
def modify_item(request: HttpRequest, pk):
    if request.method == "GET":
        pk = str(int(pk))
        print("pk:", pk)
        reque = Quotation.objects.filter(id=pk).values("id","quantity","price","currency")
        reque = list(reque)
        print(reque)
        return render(request, '../templates/quotation/modify.html', locals())
    if request.method == "POST":
        pk = str(int(pk))
        print("pk:", pk)
        reque = Quotation.objects.filter(id=pk).values("id", "quantity", "price", "currency")
        reque = list(reque)
        price = request.POST.get("price")
        currency = request.POST.get("currency")
        validTime = request.POST.get("validTime")
        quotation = Quotation.objects.filter(id=pk).update(price=price, currency=currency, validTime=validTime)
        if quotation:
            insertmessage = "修改成功"
            return render(request, '../templates/quotation/modify.html', locals())
        else:
            insertmessage = "修改失败"
            return render(request, '../templates/quotation/modify.html', locals())


"""
3.2.3
评价供应商报价
"""

def review(request: HttpRequest, pk):
    if request.method == "GET":
        pk = str(int(pk))
        print("pk:", pk)
        quotation= Quotation.objects.filter(collNo = pk).values()
        vendorid = quotation[0]['vendor_id']
        orderitem = OrderItem.objects.filter(po__vendor=vendorid).values()
        orderitem = list(orderitem)
        print(orderitem)
        sum = 0
        ontimeScore = 0
        quantityScore =0
        serviceScore =0
        qualityScore =0
        for i in orderitem:
            sum+=i['price']*i['quantity']
        for i in orderitem:
            quanzhong = i['price']*i['quantity']/sum
            ontimeScore+=i['ontimeScore']*quanzhong
            quantityScore+=i['quantityScore']*quanzhong
            serviceScore+=i['serviceScore']*quanzhong
            qualityScore+=i['qualityScore']*quanzhong
        pingjia = {'qualityScore':qualityScore,
                   'serviceScore':serviceScore,
                   'quantityScore':quantityScore,
                   'ontimeScore':ontimeScore,
                   'sum':sum}
        pingjia = json.dumps(pingjia)
        return render(request, '../templates/quotation/review.html',locals())


"""
评价供应商报价
"""
def vendor_modify_item(request: HttpRequest, pk):
    if request.method == "GET":
        Quotation_form = VendormodifyquotationForm()
        pk = str(int(pk))
        print("pk:", pk)
        reque = Quotation.objects.filter(id=pk).values("id","quantity","price","currency")
        reque = list(reque)
        print(reque)
        return render(request, '../templates/quotation/vendormodify.html', locals())
    if request.method == "POST":
        pk = str(int(pk))
        print("pk:", pk)
        collNo = request.POST.get("collNo")
        deadline = request.POST.get("deadline")
        quantity = request.POST.get("quantity")
        deliveryDate = request.POST.get("deliveryDate")
        vendorvid = request.POST.get("vendorvid")
        rej = request.POST.get("rej")
        quotation = Quotation.objects.filter(id=pk).update(deadline=deadline, quantity=quantity,
                                                           deliveryDate=deliveryDate, collNo=collNo, rej=rej)
        if quotation:
            message = "修改成功"
            return render(request, '../templates/quotation/vendormodify.html', locals())
        else:
            message = "修改失败"
            return render(request, '../templates/quotation/vendormodify.html', locals())




@csrf_exempt
def makebyrq(request: HttpRequest, pk):
    if request.method == "GET":
        reque = RequisitionItem.objects.filter(id = pk).values("id",
                                                               "itemId",
                                                               "meterial__id",
                                                               "meterial__stock",
                                                               "meterial__sloc")
        return render(request, '../templates/quotation/RFQ-create.html', locals())
    if request.method =="POST":
        collNo = request.POST.get("collNo")
        deadline = request.POST.get("deadline")
        quantity = request.POST.get("quantity")
        deliveryDate = request.POST.get("deliveryDate")
        vendorvid = request.POST.get("vendorvid")
        print(quantity)
        euser =RequisitionItem.objects.filter(id = pk).values("id","pr__euser_id",
                                                               "itemId",
                                                               "meterial__id",
                                                               "meterial__stock",
                                                               "meterial__sloc")
        euserid = euser[0]['pr__euser_id']
        now_time = datetime.datetime.now()
        quotation = Quotation.objects.create(deadline=deadline,
                                             quantity=quantity,
                                             ri_id=pk,
                                             vendor_id=vendorvid,
                                             euser_id=euserid,
                                             time=now_time,
                                             collNo=collNo,
                                             deliveryDate=deliveryDate,
                                             rej=1
                                             )
        if quotation:
            print("111111c")
        return render(request, '../templates/quotation/RFQ-create.html', locals())




@csrf_exempt
def getall(request):
    if request.method == "GET":
        quoatations = Quotation.objects.all().values()
        quoatations = list(quoatations)
        return render(request, '../templates/quotation/RFQ.html',locals())
    if request.method == "POST":
        id = request.POST.get("id")
        euserid = request.POST.get("euserid")
        vendorvid = request.POST.get("vendorvid")
        riid = request.POST.get("riid")
        collNo = request.POST.get("collNo")
        quoatations = Quotation.objects.filter(id = id,
                                             ri_id=riid,
                                             vendor_id=vendorvid,
                                             euser_id=euserid,
                                             collNo=collNo
                                             ).values()
        if quoatations:
            quoatations = list(quoatations)
            return render(request, '../templates/quotation/RFQ.html', locals())
        else:
            insertmessage = "创建失败"
            return render(request, '../templates/quotation/RFQ.html', locals())



@csrf_exempt
def searchqinggou(request):
    if request.method == "GET":
        quoatations = PurchaseRequisition.objects.all().values()
        quoatations = list(quoatations)
        return render(request, '../templates/quotation/RFQ-create_search.html', locals())
    if request.method == "POST":
        id = request.POST.get("id")
        euserid = request.POST.get("euserid")
        mid = request.POST.get("materialid")
        quoatations = PurchaseRequisition.objects.filter(id=id,
                                           euser_id=euserid,requisitionitem__meterial__id=mid
                                             ).values()
        quoatations = list(quoatations)
        if quoatations:
            quoatations = list(quoatations)
            return render(request, '../templates/quotation/RFQ-create_search.html', locals())
        else:
            insertmessage = "创建失败"
            return render(request, '../templates/quotation/RFQ-create_search.html', locals())





@csrf_exempt
def rfqinfo(request: HttpRequest, pk):
    if request.method == "GET":
        quoatations = PurchaseRequisition.objects.filter(id = pk).values()

        quoatations = list(quoatations)

        rq = RequisitionItem.objects.filter(pr_id=pk).values("meterial__stock__id","meterial__id",
                                                             "itemId","meterial__sloc")

        rq = list(rq)
        return render(request, '../templates/quotation/RFQ-create_info.html', locals())




@csrf_exempt
def rfqinfo2(request: HttpRequest, pk):
    if request.method == "GET":
        quoatations = Quotation.objects.filter(id=pk).values("id","euser_id","ri_id",
                                                             "deadline","time","rej","vendor_id","collNo")

        quoatations = list(quoatations)
        riid = quoatations[0]['ri_id']
        viid = quoatations[0]['vendor_id']
        colno = quoatations[0]['collNo']
        caigou = RequisitionItem.objects.filter(id=riid).values("quotation__vendor__pOrg", "meterial__stock__pGrp",
                                                             "meterial__id", "meterial__sloc","quantity",
                                                                "deliveryDate","meterial__stock__name")


        vendor =Vendor.objects.filter(vid=viid).values("score","vid","vname","city",
                                                       "address","postcode")


        vendor = list(vendor)



        caigou = list(caigou)
        for i in caigou:
            i['collNo'] = colno
        print(caigou)
        while len(caigou)!=1:
            caigou.pop()
        baojia = Quotation.objects.filter(id=pk).values("price","deadline")
        baojia = list(baojia)
        return render(request, '../templates/quotation/RFQ-info.html', locals())




@csrf_exempt
def searchquo(request):
    if request.method == "GET":
        quoatations = Quotation.objects.all().values()
        quotattions1 = Quotation.objects.all().values("ri__status")
        quoatations = list(quoatations)
        quotattions1 = list(quotattions1)
        for i in range(len(quoatations)):
            quoatations[i]['ri__status'] = quotattions1[i]['ri__status']
        print(quoatations)
        return render(request, '../templates/quotation/vq-modify_search.html', locals())
    if request.method == "POST":
        id = request.POST.get("id")
        euserid = request.POST.get("euserid")
        vendorid = request.POST.get("vendorid")
        collno = request.POST.get("collNo")
        quotation = Quotation.objects.filter(id=id,
                                           euser_id=euserid,vendor_id=vendorid,collNo=collno
                                             ).values()
        print(quotation)
        quoatations = list(quotation)
        if quotation:
            quoatations = list(quotation)
            return render(request, '../templates/quotation/vq-modify_search.html', locals())
        else:
            insertmessage = "创建失败"
            return render(request, '../templates/quotation/vq-modify_search.html', locals())



@csrf_exempt
def pcs(request):
    if request.method == "GET":
        quoatations = Quotation.objects.all().values("ri__meterial__material_id","id",
                                                     "ri_id","quantity","collNo","price",
                                                     "currency","rej")
        quoatations = list(quoatations)
        return render(request, '../templates/purchaseorder/po-create_search.html',locals())
    if request.method == "POST":
        id = request.POST.get("id")
        mete= request.POST.get("mete")
        collNo = request.POST.get("collNo")
        quoatations = Quotation.objects.filter(ri__meterial__material_id=mete,id = id,
                                               collNo=collNo).values("ri__meterial__material_id","id",
                                                     "ri_id","quantity","collNo","price",
                                                     "currency","rej")
        if quoatations:
            quoatations = list(quoatations)
            return render(request, '../templates/purchaseorder/po-create_search.html', locals())
        else:
            insertmessage = "创建失败"
            return render(request, '../templates/purchaseorder/po-create_search.html', locals())



