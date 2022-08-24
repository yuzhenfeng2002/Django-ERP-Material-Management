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

from ..models import EUser, Material, MaterialItem, Stock, PurchaseRequisition, RequisitionItem, Quotation, Vendor, \
    PurchaseOrder, OrderItem
from .auxiliary import *







class selectpurchaseOrderForm(forms.Form):
    prid = forms.CharField(label="请购单编码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    itemId = forms.CharField(label="条目编码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))




class PurchaseOrderForm(forms.Form):
    euser__id = forms.CharField(label="用户ID", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(label="用户ID", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))



class RequisitionItemform(forms.Form):
    mid = forms.CharField(label="物料编码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    plant = forms.CharField(label="工厂编码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    prid = forms.CharField(label="请购单编码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    itemId = forms.CharField(label="条目编码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    estimatedPrice = forms.CharField(label="预估价格", max_length=256,
                                     widget=forms.TextInput(attrs={'class': 'form-control'}))
    deliveryDate = forms.CharField(label="送货时间", max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    currency = forms.CharField(label="货币", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    quantity = forms.CharField(label="数量", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))



""""
创建请购单
"""

def requeinsert(request):
    if request.method == "GET":
        return render(request, '../templates/purchaserequisition/create.html', locals())
    if request.method == "POST":
        prid = request.POST.get("prid")
        mid = request.POST.get("mid")
        plant = request.POST.get("plant")
        itemId = request.POST.get("itemId")
        estimatedPrice = request.POST.get("estimatedPrice")
        currency = request.POST.get("currency")
        quantity = request.POST.get("quantity")
        deliveryDate = request.POST.get("deliveryDate")
        materials = MaterialItem.objects.filter(
            material=mid, stock=plant
        )
        if materials:
            materialtem = MaterialItem.objects.get(material=mid, stock=plant)
            material_id = materialtem.id
            material = Material.objects.get(id=material_id)
            requision = PurchaseRequisition.objects.get(id=prid)
            requisitionitem = RequisitionItem.objects.create(pr=requision,
                                                             meterial=material,
                                                             estimatedPrice=estimatedPrice,
                                                             currency=currency,
                                                             quantity=quantity,
                                                             status="1",
                                                             itemId=itemId,
                                                             deliveryDate=deliveryDate)
            content = 100000 + requision.id
            remessages = "创建成功"
            if requisitionitem:
                PurchaseOrder_form = PurchaseOrderForm()
                return render(request, '../templates/purchaserequisition/create.html', locals())
        else:
            remessages = "创建失败"
            return render(request, '../templates/purchaserequisition/create.html', locals())
    return render(request, '../templates/purchaserequisition/create.html', locals())




""""
创建请购条目
"""
def insert(request):
    if request.method == "GET":
        return render(request, '../templates/purchaserequisition/create.html', locals())
    if request.method == "POST":
        euser__id = request.POST.get("euserid")
        text = request.POST.get("text")
        now_time = datetime.datetime.now()
        requision = PurchaseRequisition.objects.create(time=now_time, euser_id=euser__id, text=text)
        id = requision.id
        if requision:
            PurchaseOrder_form = PurchaseOrderForm()
            messages = "创建成功"
            return render(request, '../templates/purchaserequisition/create.html', locals())
        else:
            messages = "创建失败"




"""
3.1.2
5. FUNCTION(删除采购订单条目)
"""
def deletereque(request):
    if request.method == "GET":
        return render(request, '../templates/purchaserequisition/delete.html', locals())
    if request.method == "POST":
        prid = request.POST.get("prid")
        itemId = request.POST.get("itemId")
        reque = RequisitionItem.objects.filter(pr_id=prid, itemId=itemId).delete()
        if reque:
            message = "删除成功"
            return render(request, '../templates/purchaserequisition/delete.html', locals())
        else:
            message = "删除失败"
            return render(request, '../templates/purchaserequisition/delete.html', locals())



def getpq(request):
    if request.method == "GET":
        purc = PurchaseRequisition.objects.all().values()
        purc = list(purc)
        print(purc)
        return render(request, '../templates/purchaserequisition/purchase_request.html', locals())
    if request.method == "POST":
        id = request.POST.get("id")
        euserid = request.POST.get("euserid")
        purchaser = PurchaseRequisition.objects.filter(id = id,euser_id=euserid).values()
        purc = list(purchaser)
        print(purc)
        return render(
            request=request,
            template_name='../templates/purchaserequisition/purchase_request.html',
            context={'purc': purc}
        )





def getpqinfo(request: HttpRequest, pk):
    if request.method == "GET":
        purchaseRequisition = PurchaseRequisition.objects.filter(id = pk).values()
        reuqe = RequisitionItem.objects.filter(pr_id=pk).values("itemId", "estimatedPrice", "currency",
                                                            "deliveryDate","quantity",
                                                            "meterial__id", "pr_id", "status","meterial__sloc","meterial__material__mname"
                                                            ,"meterial__stock__id","meterial__stock__name")
        reuqe = list(reuqe)
        for i in reuqe:
            if i['status']=='0':
                i['status'] = "已创建采购申请"
            if i['status']=='1':
                i['status'] = "已创建采购订单"
        purchaseRequisition = list(purchaseRequisition)
        print(reuqe)
        return render(
            request=request,
            template_name='../templates/purchaserequisition/pr-info.html',
            context={'reuqe': reuqe,'purchaseRequisition':purchaseRequisition}
        )




def getpqinfo2(request: HttpRequest, pk):
    if request.method == "GET":
        purchaseRequisition = PurchaseRequisition.objects.filter(id = pk).values()
        reuqe = RequisitionItem.objects.filter(pr_id=pk).values("itemId", "estimatedPrice", "currency",
                                                            "deliveryDate","quantity",
                                                            "meterial__id", "pr_id", "status","meterial__sloc","meterial__material__mname"
                                                            ,"meterial__stock__id","meterial__stock__name")
        reuqe = list(reuqe)
        for i in reuqe:
            if i['status']=='0':
                i['status'] = "已创建采购申请"
            if i['status']=='1':
                i['status'] = "已创建采购订单"
        purchaseRequisition = list(purchaseRequisition)
        print(reuqe)
        return render(
            request=request,
            template_name='../templates/invoice/po-info.html',
            context={'reuqe': reuqe,'purchaseRequisition':purchaseRequisition}
        )




def getpqinfo3(request: HttpRequest, pk):
    if request.method == "GET":
        purchaseRequisition = PurchaseRequisition.objects.filter(id = pk).values()
        reuqe = RequisitionItem.objects.filter(pr_id=pk).values("itemId", "estimatedPrice", "currency",
                                                            "deliveryDate","quantity",
                                                            "meterial__id", "pr_id", "status","meterial__sloc","meterial__material__mname"
                                                            ,"meterial__stock__id","meterial__stock__name")
        reuqe = list(reuqe)
        for i in reuqe:
            if i['status']=='0':
                i['status'] = "已创建采购申请"
            if i['status']=='1':
                i['status'] = "已创建采购订单"
        purchaseRequisition = list(purchaseRequisition)
        print(reuqe)
        return render(
            request=request,
            template_name='../templates/receipt/po-info.html',
            context={'reuqe': reuqe,'purchaseRequisition':purchaseRequisition}
        )






@csrf_exempt
def getmodifyinfo(request: HttpRequest, pk):
    if request.method == "GET":
        purchaseRequisition = PurchaseRequisition.objects.filter(id=pk).values()
        reuqe = RequisitionItem.objects.filter(pr_id=pk).values("itemId", "estimatedPrice", "currency",
                                                                "deliveryDate", "quantity",
                                                                "meterial__id", "pr_id", "status",
                                                                "meterial__sloc", "meterial__material__mname"
                                                                , "meterial__stock__id")
        reuqe = list(reuqe)
        for i in reuqe:
            if i['status']=='0':
                i['status'] = "已创建采购申请"
            if i['status']=='1':
                i['status'] = "已创建采购订单"
        purchaseRequisition = list(purchaseRequisition)
        print(reuqe)
        return render(
            request=request,
            template_name='../templates/purchaserequisition/pr-modify(1).html',
            context={'reuqe': reuqe, 'purchaseRequisition': purchaseRequisition}
        )
    if request.method == "POST":
        beizhu = request.POST.get("beizhu")
        PurchaseRequisition.objects.filter(id=pk).update(text = beizhu)
        message = "修改成功"
        print(message)
        purchaseRequisition = PurchaseRequisition.objects.filter(id=pk).values()
        reuqe = RequisitionItem.objects.filter(pr_id=pk).values("itemId", "estimatedPrice", "currency",
                                                                "deliveryDate", "quantity",
                                                                "meterial__id", "pr_id", "status",
                                                                "meterial__sloc", "meterial__material__mname"
                                                                , "meterial__stock__id")
        reuqe = list(reuqe)
        for i in reuqe:
            if i['status']=='0':
                i['status'] = "已创建采购申请"
            if i['status']=='1':
                i['status'] = "已创建采购订单"
        purchaseRequisition = list(purchaseRequisition)
        return render(
            request=request,
            template_name='../templates/purchaserequisition/pr-modify(1).html',
            context={'reuqe': reuqe, 'purchaseRequisition': purchaseRequisition}
        )









@csrf_exempt
def getmodifyinfo2(request):
    if request.method == "POST":
        print("111111111111")
        data = request.POST.get("rid")
        rid = eval(data)
        data1 = request.POST.get("itemId")
        itemId = eval(data1)
        data2 = request.POST.get("estimatedPrice")
        estimatedPrice = eval(data2)
        data3 = request.POST.get("currency")
        currency = eval(data3)
        data4 = request.POST.get("quantity")
        quantity = eval(data4)
        data5 = request.POST.get("deliveryDate")
        print(data5)
        deliveryDate = getDate2(data5)
        data6 = request.POST.get("meterial__id")
        meterial_id = eval(data6)
        print(rid)
        print(itemId)
        reque = RequisitionItem.objects.filter(pr_id=rid,itemId=itemId).update(
                                                      estimatedPrice=estimatedPrice,
                                                      quantity=quantity,
                                                      deliveryDate=deliveryDate,
                                                      currency=currency,
                                                      meterial_id=meterial_id
                                                      )
        print(rid)
        return HttpResponse(json.dumps(reque))




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







@csrf_exempt

def newrequeinsert(request):
    if request.method == "GET":
        return render(request, '../templates/purchaserequisition/create-new.html', locals())
    if request.method == "POST":
        print("11111")
        euser = request.user
        euserid = euser.pk
        mid = request.POST.get("mid")
        plant = request.POST.get("plant")
        itemId = request.POST.get("itemId")
        data = request.POST.get("json")
        text = request.POST.get("beizhu")
        print(text)
        print("type:",type(data))
        now_time = datetime.datetime.now()
        requision = PurchaseRequisition.objects.create(time=now_time, euser_id=euserid, text=text)
        prid= requision.id
        data1 = eval(data)
        for i in data1:
            print(i['deliveryDate'])
            str = getDate2(i['deliveryDate'])
            requisitionitem = RequisitionItem.objects.create(pr_id = prid,
                                                             meterial_id = i['material_id'] ,
                                                             estimatedPrice=i['estimatedPrice'],
                                                             currency=i['currency'],
                                                             quantity=i['quantity'],
                                                             status="0",
                                                             itemId=i['itemId'],
                                                             deliveryDate= str)

        content = 100000 + requision.id
        remessages = "创建成功"
        datalist = {
            "message":"创建成功",
            "content": content
        }
        return HttpResponse(json.dumps(datalist))




@csrf_exempt
def createsys(request: HttpRequest, pk):
    if request.method == "GET":
        pk = str(int(pk))
        print("pk:", pk)
        quotation = Quotation.objects.filter(id = pk).values()
        vendorid = quotation[0]['vendor_id']
        riid = quotation[0]['ri_id']
        price = quotation[0]['price']
        vendor = Vendor.objects.filter(vid = vendorid).values()
        requisitionItem = RequisitionItem.objects.filter(id = riid).values("currency","meterial__sloc",
                                                                           "id","itemId","meterial__material__mname","meterial__stock__id","meterial__id",
                                                                           "quantity","deliveryDate","meterial__stock__name"
                                                                           )
        collno = quotation[0]['collNo']
        zuoceinfo = Quotation.objects.filter(collNo = collno).values("id","rej")
        zuoceinfo = list(zuoceinfo)
        caigou = RequisitionItem.objects.filter(id = riid).values("meterial__stock__id","meterial__stock__pOrg",
                                                                  "meterial__stock__pGrp")


        vendor = list(vendor)
        caigou = list(caigou)
        for i in requisitionItem:
            i['price'] = price
            i['sum'] = i['quantity']*i['price']
        requisitionItem = list(requisitionItem)
        quotation = list(quotation)
        print(caigou)
        print(vendor)
        print(requisitionItem)
        print(zuoceinfo)
        return render(request, '../templates/purchaseorder/po-create_system.html',locals())
    if request.method == "POST":
        quotation = Quotation.objects.filter(id = pk).values()
        data = request.POST.get("json")
        euser_id = quotation[0]['euser_id']
        telephone = request.POST.get("telephone")
        shippingAddress = request.POST.get("shippingAddress")
        fax = request.POST.get("fax")
        now_time = datetime.datetime.now()
        vendor_id =  request.POST.get("vendor__id")
        data1 = eval(data)
        print(data1)
        pr =PurchaseOrder.objects.create(euser_id=euser_id, telephone=telephone,
                                                 shippingAddress=shippingAddress, fax=fax,
                                                 vendor_id=vendor_id, rfq_id=pk,time=now_time)
        if pr:
            print("创建成功")
        prid =pr.id
        for i in data1:
            print(i['deliveryDate'])
            str1 = getDate2(i['deliveryDate'])
            requisitionitem = OrderItem.objects.create(
                                                             meterialItem_id=i['meterial__id'],
                                                             price=i['price'],
                                                             currency=i['currency'],
                                                             quantity=i['quantity'],
                                                             status="0",
                                                             itemId=i['itemId'],
                                                             deliveryDate=str1,
                                                                po_id=prid)
        datalist = {
            "message": "创建成功",
            "content": prid
        }
        return HttpResponse(json.dumps(datalist))















@csrf_exempt
@login_required()
def createmanu(request):
    if request.method == "GET":
        return render(request, '../templates/purchaseorder/po-create_manual.html', locals())



@csrf_exempt
@login_required()
def creamanujiekou(request):
    if request.method == "POST":
        euser = request.user
        euserid = euser.pk
        data1= request.POST.get("json")
        data1 = eval(data1)
        telephone = request.POST.get("telephone")
        shippingAddress = request.POST.get("shippingAddress")
        fax = request.POST.get("fax")
        now_time = datetime.datetime.now()
        vendor_id =  request.POST.get("vid")
        print(data1)
        print(telephone)
        print(fax)
        print(vendor_id)
        print(shippingAddress)
        pr =PurchaseOrder.objects.create(euser_id=euserid, telephone=telephone,
                                                 shippingAddress=shippingAddress, fax=fax,
                                                 vendor_id=vendor_id,time=now_time)
        prid = pr.id
        for i in data1:
            print(i['deliveryDate'])
            str1 = getDate2(i['deliveryDate'])
            mete = MaterialItem.objects.filter(stock_id = i['plant'],material_id=i['material_id']).values()
            mateid = mete[0]['id']
            requisitionitem = OrderItem.objects.create(
                                                             meterialItem_id=mateid,
                                                             price=i['price'],
                                                             currency=i['currency'],
                                                             quantity=i['quantity'],
                                                             status="0",
                                                             itemId=i['itemId'],
                                                             deliveryDate=str1,
                                                                po_id=prid)
            print("chuangjiancg")
        datalist = {
            "message": "创建成功",
            "content": prid
        }
        return HttpResponse(json.dumps(datalist))


@csrf_exempt
def quomodify(request: HttpRequest, pk):
    if request.method == "GET":
        pk = str(int(pk))
        print("pk:", pk)
        quotation = Quotation.objects.filter(id = pk).values()
        vendorid = quotation[0]['vendor_id']
        riid = quotation[0]['ri_id']
        price = quotation[0]['price']
        vendor = Vendor.objects.filter(vid = vendorid).values()
        requisitionItem = RequisitionItem.objects.filter(id = riid).values("currency","meterial__sloc",
                                                                           "id","itemId","meterial__material__mname","meterial__stock__id","meterial__id",
                                                                           "quantity","deliveryDate","meterial__stock__name"
                                                                           )
        collno = quotation[0]['collNo']
        zuoceinfo = Quotation.objects.filter(collNo = collno).values("id","rej")
        zuoceinfo = list(zuoceinfo)
        caigou = RequisitionItem.objects.filter(id = riid).values("meterial__stock__id","meterial__stock__pOrg",
                                                                  "meterial__stock__pGrp","meterial__material__id",
                                                                  "meterial__stock__name","meterial__sloc")


        vendor = list(vendor)
        baojia  =Quotation.objects.filter(id = pk).values("price","validTime")
        baojia = list(baojia)
        caigou = list(caigou)
        quotation = list(quotation)
        for i in requisitionItem:
            if price==None:
                i['price']=0
            else:
                i['price'] = price
            if i['quantity']==None:
                i['quantity']=0
            i['sum'] = i['quantity']*i['price']
        requisitionItem = list(requisitionItem)
        quotation = list(quotation)
        print(caigou)
        print(vendor)
        print(requisitionItem)
        print(zuoceinfo)
        return render(request, '../templates/quotation/vq-modify.html', locals())
    if request.method == "POST":
        deadline = request.POST.get("deadline")
        deliverDate = request.POST.get("deliverDate")
        deliverDate = getDate2(deliverDate)
        deadline = getDate2(deadline)
        quantity = request.POST.get("quantity")
        collNo = request.POST.get("collNo")
        print(collNo)
        print("dead:",deadline)
        print("deliv:",deliverDate)
        quo = Quotation.objects.filter(id=pk).update(deadline = deadline,
                                                     quantity=quantity,collNo=collNo,deliveryDate=deliverDate)
        quoid= quo.id
        print(collNo)
        print(deadline)
        if quo:
            print("修改成功")
        datalist = {
            "message": "创建成功",
            "content": quoid
        }
        quotation = Quotation.objects.filter(id=pk).values()
        vendorid = quotation[0]['vendor_id']
        riid = quotation[0]['ri_id']
        price = quotation[0]['price']
        vendor = Vendor.objects.filter(vid=vendorid).values()
        requisitionItem = RequisitionItem.objects.filter(id=riid).values("currency", "meterial__sloc",
                                                                         "id", "itemId", "meterial__material__mname",
                                                                         "meterial__stock__id", "meterial__id",
                                                                         "quantity", "deliveryDate",
                                                                         "meterial__stock__name"
                                                                         )
        collno = quotation[0]['collNo']
        zuoceinfo = Quotation.objects.filter(collNo=collno).values("id", "rej")
        zuoceinfo = list(zuoceinfo)
        caigou = RequisitionItem.objects.filter(id=riid).values("meterial__stock__id", "meterial__stock__pOrg",
                                                                "meterial__stock__pGrp", "meterial__material__id",
                                                                "meterial__stock__name", "meterial__sloc")

        vendor = list(vendor)
        baojia = Quotation.objects.filter(id=pk).values("price", "validTime")
        baojia = list(baojia)
        caigou = list(caigou)
        quotation = list(quotation)
        for i in requisitionItem:
            i['price'] = price
            i['sum'] = i['quantity'] * i['price']
        requisitionItem = list(requisitionItem)
        quotation = list(quotation)
        print(caigou)
        print(vendor)
        print(requisitionItem)
        print(zuoceinfo)
        return render(request, '../templates/quotation/vq-modify.html', locals())






@csrf_exempt
def quomodifyjiekou(request):
    if request.method == "POST":
        pk = request.POST.get("id")
        deadline = request.POST.get("deadline")
        deliverDate = request.POST.get("deliveryDate")
        deliverDate = getDate2(deliverDate)
        deadline = getDate2(deadline)
        quantity = request.POST.get("quantity")
        collNo = request.POST.get("collNo")
        rej = request.POST.get("rej")
        print(deliverDate)
        print(deadline)
        print(quantity)
        print(rej)
        if rej=="true":
            rej =True
        if rej=="false":
            rej =False
        print(collNo)
        print(pk)
        print("dead:",deadline)
        print("deliv:",deliverDate)
        quo = Quotation.objects.filter(id=pk).update(deadline = deadline,
                                                     quantity=quantity,collNo=collNo,deliveryDate=deliverDate,
                                                     rej = rej)
        print(collNo)
        print(deadline)
        if quo:
            print("修改成功")
        datalist = {
            "message": "创建成功",
            "content": quo
        }
        return HttpResponse(json.dumps(datalist))








@csrf_exempt
def pomanage(request):
    return render(request, '../templates/purchaseorder/po_manage.html', locals())




@csrf_exempt
def poindex(request):
    return render(request, '../templates/purchaseorder/purchase_index.html', locals())



@csrf_exempt
def prmanage(request):
    return render(request, '../templates/purchaserequisition/pr_manage.html', locals())



@csrf_exempt
def quoma(request):
    return render(request, '../templates/quotation/quo_manage.html', locals())


