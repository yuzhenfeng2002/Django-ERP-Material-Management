import json
from django.core import serializers
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.decorators import login_required
from django import forms
from django.views.decorators.csrf import csrf_exempt

from .auxiliary import getRegex


from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.decorators import login_required

from ..models import EUser, Material, MaterialItem, Stock
from .auxiliary import *


from ..models import EUser, Material, MaterialItem, Stock,PurchaseRequisition,RequisitionItem,Quotation,Vendor,PurchaseOrder,OrderItem



"""
创建时间+创建者编码+供应商编码+收货方电话+收货方传真+送货地址+参考供应商编码+参考请购单编码】
+1条/多条采购条目（每一条包括【条目编码+数量+单价+货币+数量+送货时间+工厂+物料编码】
"""



class PurchaseorderForm(forms.Form):
    euserid = forms.CharField(label="创建者ID", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telephone = forms.CharField(label="收货方电话", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    fax = forms.CharField(label="收货方传真", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    shippingAddress = forms.CharField(label="送货地址", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    vendor_id = forms.CharField(label="参考供应商编码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    rfq__id = forms.CharField(label="参考询价单编码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))



class OrderForem(forms.Form):
    pid = forms.CharField(label="采购订单编码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    itemId = forms.CharField(label="条目编码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.CharField(label="单价", max_length=256,widget=forms.TextInput(attrs={'class': 'form-control'}))
    currency = forms.CharField(label="货币", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    quantity = forms.CharField(label="数量", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    deliveryDate = forms.CharField(label="送货时间", max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    plant = forms.CharField(label="工厂", max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    material_id = forms.CharField(label="物料编码", max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))




"""
插入采购订单
"""
def insert(request):
    if request.method == "GET":
        Quotation_form = PurchaseorderForm()
        return render(request, '../templates/purchaseorder/insertpurchaseorder.html', locals())
    if request.method == "POST":
        euser_id = request.POST.get("euserid")
        telephone = request.POST.get("telephone")
        shippingAddress = request.POST.get("shippingAddress")
        fax = request.POST.get("fax")
        vendor_id = request.POST.get("vendor_id")
        rfq__id = request.POST.get("rfq__id")
        requision = PurchaseOrder.objects.create(euser_id=euser_id, telephone=telephone,
                                                 shippingAddress=shippingAddress, fax=fax,
                                                 vendor_id=vendor_id, rfq_id=rfq__id)
        id = requision.id
        message = "插入成功"
        return render(request, '../templates/purchaseorder/insertpurchaseorder.html', locals())
    else:
        message = "插入失败"
        return render(request, '../templates/purchaseorder/insertpurchaseorder.html', locals())




"""
插入采购条目
"""
def insertorderForem(request):
    if request.method == "GET":
        Quotation_form = PurchaseorderForm()
        return render(request, '../templates/purchaseorder/insertpurchaseorder.html', locals())
    if request.method == "POST":
        Quotation_form = PurchaseorderForm()
        pid = request.POST.get("pid")
        itemId = request.POST.get("itemId")
        price = request.POST.get("price")
        currency = request.POST.get("currency")
        quantity = request.POST.get("quantity")
        deliveryDate = request.POST.get("deliveryDate")
        plant = request.POST.get("plant")
        material_id = request.POST.get("material_id")
        materialitem = MaterialItem.objects.filter(material_id = material_id,stock_id = plant).values()
        mid = materialitem[0]['id']
        purchaseorder = OrderItem.objects.create(itemId = itemId,price =price,quantity =quantity,deliveryDate =deliveryDate,
                                                     meterial_id = mid,po_id =pid,
                                                 status=1 )
        requisitionItem = PurchaseOrder.objects.filter(id=pid).values()
        rfqid = requisitionItem[0]['rfq_id']
        RequisitionItem.objects.filter(id=rfqid).update(status = 1)
        if purchaseorder:
            pomessage = "插入成功"
            return render(request, '../templates/purchaseorder/insertpurchaseorder.html', locals())
        else:
            pomessage = "插入失败"
            return render(request, '../templates/purchaseorder/insertpurchaseorder.html', locals())



"""
筛选采购订单
"""
def shaixuan(request: HttpRequest):
    if request.method == "GET":
        Quotation_form = PurchaseorderForm()
        return render(request, '../templates/purchaseorder/shaixuan.html', locals())
    if request.method == "POST":
        euser_id = request.POST.get("euserid")
        telephone = request.POST.get("telephone")
        shippingAddress = request.POST.get("shippingAddress")
        fax = request.POST.get("fax")
        vendor_id = request.POST.get("vendor_id")
        rfq__id = request.POST.get("rfq__id")

        purchaseorder = PurchaseOrder.objects.filter(euser_id=euser_id, telephone=telephone,
                                                     shippingAddress=shippingAddress, fax=fax,
                                                     vendor_id=vendor_id, rfq_id=rfq__id).values()
    if len(purchaseorder) > 0:
        a = list(purchaseorder)
        print(purchaseorder)
        print(a)
        message = "查询成功"
        return render(request, '../templates/purchaseorder/shaixuan.html', locals())
    else:
        message = "查询失败"
        return render(request, '../templates/purchaseorder/shaixuan.html', locals())



"""
搜索采购订单
"""
def selectone(request: HttpRequest, pk):
    if request.method == "GET":
        pk = str(int(pk))
        print("pk:", pk)
        purchaseorder= PurchaseOrder.objects.filter(id = pk).values()
        vendor_id = purchaseorder[0]['vendor_id']
        vendor = Vendor.objects.filter(vid=vendor_id).values()
        vendor = list(vendor)
        purchaseorder = list(purchaseorder)
        return render(request, '../templates/purchaseorder/getpurchaseorderbyid.html', locals())



"""
修改信息
"""
def modifyone(request: HttpRequest, pk):
    if request.method == "GET":
        pk = str(int(pk))
        print("pk:", pk)
        quotation = PurchaseOrder.objects.filter(id=pk).values()
        quotation = list(quotation)
        return render(request, '../templates/purchaseorder/modify.html', locals())
    if request.method == "POST":
        euser_id = request.POST.get("euserid")
        telephone = request.POST.get("telephone")
        shippingAddress = request.POST.get("shippingAddress")
        fax = request.POST.get("fax")
        vendor_id = request.POST.get("vendor_id")
        rfq__id = request.POST.get("rfq__id")
        quotation1 = PurchaseOrder.objects.filter(id=pk).update(euser_id=euser_id, telephone=telephone,
                                                               shippingAddress=shippingAddress, fax=fax,
                                                               vendor_id=vendor_id, rfq_id=rfq__id)
        quotation = PurchaseOrder.objects.filter(id=pk).values()
        quotation = list(quotation)
        if quotation1:
            message = "修改成功"
            return render(request, '../templates/purchaseorder/modify.html', locals())
        else:
            message = "修改失败"
            return render(request, '../templates/purchaseorder/modify.html', locals())



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




"""
3.3.1  3. FUNCTION(查找询价单)
"""
def getquotebyid(request: HttpRequest, pk):
    if request.method == "GET":
        pk = str(int(pk))
        print("pk:", pk)
        quotation = Quotation.objects.filter(id = pk).values()
        vendorid = quotation[0]['vendor_id']
        riid = quotation[0]['ri_id']
        vendor = Vendor.objects.filter(vid = vendorid).values()
        requisitionItem = RequisitionItem.objects.filter(id = riid).values()
        miid = requisitionItem[0]['meterial_id']
        materialitem = MaterialItem.objects.filter(id = miid).values()
        material_id = materialitem[0]['material_id']
        material = Material.objects.filter(id = material_id).values()
        mname = material[0]['mname']
        stockid = materialitem[0]['stock_id']
        material_info  = {'mname':mname,'material_id':material_id}
        material_info = json.dumps(material_info)
        stock = Stock.objects.filter(id = stockid).values()
        stock = list(stock)
        vendor = list(vendor)
        quotation = list(quotation)
        print(quotation)
        sum = quotation[0]['quantity']*quotation[0]['price']
        quotation_info = {'quantity':quotation[0]['quantity'],
                          'price':quotation[0]['price'],
                          'sum':sum,
                          'deliveryDate':quotation[0]['deliveryDate']}
        quotation_info = json.dumps(quotation_info, cls=ComplexEncoder)
        return render(request, '../templates/quotation/getquotebyid.html',locals())




"""
3.3.2
2. FUNCTION(查找采购订单)
"""
def getquotebyid(request: HttpRequest, pk):
    if request.method == "GET":
        pk = str(int(pk))
        print("pk:", pk)
        quotation = Quotation.objects.filter(id = pk).values()








@csrf_exempt
def vqcreate(request: HttpRequest, pk):
    if request.method == "GET":
        pk = str(int(pk))
        print("pk:", pk)
        quotation = Quotation.objects.filter(id = pk).values()
        vendorid = quotation[0]['vendor_id']
        riid = quotation[0]['ri_id']
        vendor = Vendor.objects.filter(vid = vendorid).values()
        requisitionItem = RequisitionItem.objects.filter(id = riid).values()
        miid = requisitionItem[0]['meterial_id']
        mate = RequisitionItem.objects.filter(id = riid).values("meterial__id",  "meterial__stock__id",
                                                                                             "quantity","deliveryDate",
                                                                "meterial__stock__pOrg","meterial__stock__pGrp","meterial__sloc",
                                                                "meterial__stock__name")

        materialitem = list(mate)
        print(materialitem)
        vendor = list(vendor)
        quotation = list(quotation)
        print(quotation)
        print(materialitem)
        return render(request, '../templates/quotation/vq-create.html', locals())
    if request.method == "POST":
        pk = str(int(pk))
        print("pk:", pk)
        price = request.POST.get("price")
        currency = request.POST.get("currency")
        validTime = request.POST.get("validTime")
        validTime = getDate2(validTime)
        quotation1 = Quotation.objects.filter(id=pk).update(price=price,  validTime=validTime,currency=currency)
        quotation = Quotation.objects.filter(id=pk).values()
        vendorid = quotation[0]['vendor_id']
        riid = quotation[0]['ri_id']
        vendor = Vendor.objects.filter(vid=vendorid).values()
        requisitionItem = RequisitionItem.objects.filter(id=riid).values()
        miid = requisitionItem[0]['meterial_id']
        mate = RequisitionItem.objects.filter(id=riid).values("meterial__id", "meterial__stock__id",
                                                              "quantity",
                                                              "deliveryDate", "meterial__stock__pOrg",
                                                              "meterial__stock__pGrp",
                                                              "meterial__sloc", "meterial__stock__name")

        materialitem = list(mate)
        vendor = list(vendor)
        quotation = list(quotation)
        if quotation1:
            insertmessage = "修改成功"
            return render(request, '../templates/quotation/vq-create.html', locals())
        else:
            insertmessage = "修改失败"
            return render(request, '../templates/quotation/vq-create.html', locals())













@csrf_exempt
def vqcreatejiekou(request):
    if request.method == "POST":
        pk = request.POST.get("quoid")
        print("id:",pk)
        price = request.POST.get("price")
        currency = request.POST.get("currency")
        validTime = request.POST.get("validTime")
        validTime = getDate2(validTime)
        quotation1 = Quotation.objects.filter(id=pk).update(price=price, validTime=validTime, currency=currency)
        if quotation1:
            print("修改成功")
        return HttpResponse(json.dumps(pk))










@csrf_exempt
def poinfo(request: HttpRequest, pk):
    if request.method == "GET":
        pk = str(int(pk))
        print("pk:", pk)
        caigou = PurchaseOrder.objects.filter(id = pk).values("telephone","fax","shippingAddress")
        vendorid =  PurchaseOrder.objects.filter(id = pk).values("vendor_id")
        vendorid = vendorid[0]['vendor_id']
        vendor = Vendor.objects.filter(vid = vendorid).values("vid","vname","city","address")
        vendor = list(vendor)
        orderitems  = OrderItem.objects.filter(po_id= pk).values("itemId","meterialItem__id","meterialItem__material__mname",
                                                                 "quantity","price","meterialItem__stock__id","meterialItem__sloc",
                                                                 "deliveryDate","po__rfq__rej","currency","status")
        orderitems = list(orderitems)
        caigou= list(caigou)
        print(orderitems)
        for i in orderitems:
            if i['status']=='0':
                i['status']="货物未发出"
            if i['status']=='1':
                i['status']="货物已送达"
            if i['status']=='2':
                i['status']="已收到发票"
            if i['status']=='3':
                i['status']="已完成支付"

        xiangqing = PurchaseOrder.objects.filter(id = pk).values("id","euser_id","time","orderitem__currency")
        xiangqing = list(xiangqing)
        print(xiangqing)
        sum = 0
        sumquantity =0
        for i in orderitems:
            print(i['quantity'])
            print(i['price'])
            i['sum'] = i['quantity']*i['price']
            sum+=i['sum']
            sumquantity+=i['quantity']
        xiangqing[0]['sum'] = sum
        xiangqing[0]['sumquantity'] = sumquantity
        print(len(xiangqing))
        while len(xiangqing)!=1:
            xiangqing.pop()
        print(orderitems)
        print(xiangqing)
        print(orderitems)
        return render(request, '../templates/purchaseorder/po-info.html', locals())



@csrf_exempt
def pomodifyinfo(request: HttpRequest, pk):
    if request.method == "GET":
        pk = str(int(pk))
        print("pk:", pk)
        caigou = PurchaseOrder.objects.filter(id = pk).values("telephone","fax","shippingAddress")
        vendorid =  PurchaseOrder.objects.filter(id = pk).values("vendor_id")
        vendorid = vendorid[0]['vendor_id']
        vendor = Vendor.objects.filter(vid = vendorid).values("vid","vname","city","address")
        vendor = list(vendor)
        orderitems  = OrderItem.objects.filter(po_id= pk).values("itemId","meterialItem__id","meterialItem__material__mname",
                                                                 "quantity","price","meterialItem__stock__id","meterialItem__sloc",
                                                                 "deliveryDate","status","currency")
        orderitems = list(orderitems)


        for i in orderitems:
            if i['status']=='0':
                i['status']="货物未发出"
            if i['status']=='1':
                i['status']="货物已送达"
            if i['status']=='2':
                i['status']="已收到发票"
            if i['status']=='3':
                i['status']="已完成支付"



        caigou= list(caigou)


        xiangqing = PurchaseOrder.objects.filter(id = pk).values("id","euser_id","time","orderitem__currency")
        xiangqing = list(xiangqing)
        print(xiangqing)
        sum = 0
        sumquantity =0
        for i in orderitems:
            print(i['quantity'])
            print(i['price'])
            i['sum'] = i['quantity']*i['price']
            sum+=i['sum']
            sumquantity+=i['quantity']
        xiangqing[0]['sum'] = sum
        xiangqing[0]['sumquantity'] = sumquantity
        while len(xiangqing)!=1:
            xiangqing.pop()
        print(orderitems)
        print(xiangqing)
        return render(request, '../templates/purchaseorder/po-modify.html', locals())
    if request.method == "POST":
        pk = str(int(pk))
        print("pk:", pk)
        caigou = PurchaseOrder.objects.filter(id = pk).values("telephone","fax","shippingAddress")
        vendorid =  PurchaseOrder.objects.filter(id = pk).values("vendor_id")
        vendorid = vendorid[0]['vendor_id']
        vendor = Vendor.objects.filter(vid = vendorid).values("vid","vname","city","address")
        vendor = list(vendor)
        orderitems  = OrderItem.objects.filter(po_id= pk).values("itemId","meterialItem__id","meterialItem__material__mname",
                                                                 "quantity","price","meterialItem__stock__id","meterialItem__sloc",
                                                                 "deliveryDate","status","currency")
        orderitems = list(orderitems)

        for i in orderitems:
            if i['status']=='0':
                i['status']="货物未发出"
            if i['status']=='1':
                i['status']="货物已送达"
            if i['status']=='2':
                i['status']="已收到发票"
            if i['status']=='3':
                i['status']="已完成支付"



        caigou= list(caigou)



        xiangqing = PurchaseOrder.objects.filter(id = pk).values("id","euser_id","time","orderitem__currency")
        xiangqing = list(xiangqing)
        print(xiangqing)
        sum = 0
        sumquantity =0
        for i in orderitems:
            print(i['quantity'])
            print(i['price'])
            i['sum'] = i['quantity']*i['price']
            sum+=i['sum']
            sumquantity+=i['quantity']
        xiangqing[0]['sum'] = sum
        xiangqing[0]['sumquantity'] = sumquantity
        while len(xiangqing) != 1:
            xiangqing.pop()
        print(orderitems)
        print(xiangqing)
        telephone = request.POST.get("telephone")
        shippingAddress = request.POST.get("shippingAddress")
        fax = request.POST.get("fax")
        quotation1 = PurchaseOrder.objects.filter(id=pk).update( telephone=telephone,
                                                               shippingAddress=shippingAddress, fax=fax,
                                                                )
        if quotation1:
            message = "修改成功"
            return render(request, '../templates/purchaseorder/po-modify.html', locals())
        else:
            message = "修改失败"
            return render(request, '../templates/purchaseorder/po-modify.html', locals())




@csrf_exempt
def pomodifyinfo2(request):
    if request.method == "POST":
        data = request.POST.get("json")
        data = eval(data)
        id = data[0]['id']
        itemId = data[0]['itemId']
        quantity = data[0]['quantity']
        currency = data[0]['currency']
        deliveryDate = getDate2(data[0]['deliveryDate'])
        orderitem = OrderItem.objects.filter(id=id).update(itemId = itemId,
                                                           quantity=quantity,
                                                           currency = currency,
                                                           deliveryDate =deliveryDate)
        if orderitem:
            print("xiugai")
            print(data)
            datalist = {
                "message": "创建成功",
                "content": orderitem
            }
            return HttpResponse(json.dumps(datalist))



@csrf_exempt
def pomodifyinfo3(request):
    if request.method == "POST":
        data = request.POST.get("json")
        data = eval(data)
        print(data)
        id = data[0]['id']
        itemId = data[0]['itemId']
        quantity = data[0]['quantity']
        currency = data[0]['currency']
        deliveryDate = getDate2(data[0]['deliveryDate'])
        orderitem = OrderItem.objects.filter(itemId=itemId).update(quantity=quantity,
                                                           currency = currency,
                                                           deliveryDate =deliveryDate)
        if orderitem:
            print("xiugai")
            print(data)
            datalist = {
                "message": "创建成功",
                "content": orderitem
            }
            return HttpResponse(json.dumps(datalist))















@csrf_exempt
def vreview(request: HttpRequest):
    if request.method == "GET":
        quotation= Quotation.objects.all().values("id","vendor_id","collNo","ri__meterial__material_id",
                                                  "ri__quantity","vendor__vname","price","euser__material__mname")
        quotation = list(quotation)
        for i in quotation:
            vendorid = i['vendor_id']
            orderitem = OrderItem.objects.filter(po__vendor=vendorid).values()
            orderitem = list(orderitem)
            print(orderitem)
            sum = 0
            ontimeScore = 0
            quantityScore =0
            serviceScore =0
            qualityScore =0
            for j in orderitem:
                sum+=j['price']*j['quantity']
            for p in orderitem:
                print(p['ontimeScore'])
                if p['ontimeScore']==None:
                    p['ontimeScore'] =0
                if p['quantityScore']==None:
                    p['quantityScore'] =0
                if p['serviceScore']==None:
                    p['serviceScore'] =0
                if p['qualityScore']==None:
                    p['qualityScore'] =0
                quanzhong = p['price']*p['quantity']/sum
                ontimeScore+=p['ontimeScore']*quanzhong
                quantityScore+=p['quantityScore']*quanzhong
                serviceScore+=p['serviceScore']*quanzhong
                qualityScore+=p['qualityScore']*quanzhong
            i['qualityScore'] = round(qualityScore, 1)
            i['serviceScore'] = round(serviceScore, 1)
            i['quantityScore'] = round(quantityScore, 1)
            i['ontimeScore'] = round(ontimeScore, 1)
            i['sum'] = sum
            i['avgscore'] = round((quantityScore + serviceScore + quantityScore + ontimeScore) / 4, 1)
        quotation.sort(key=lambda x: x["avgscore"], reverse=True)
        for i in range(len(quotation)):
            quotation[i]['paiming'] = i+1
        print(quotation)
        return render(request, '../templates/quotation/vq-value.html',locals())
    if request.method == "POST":
        a = request.POST.get("indus")
        b = request.POST.get("collNo")
        print(a)
        print(b)
        quotation = Quotation.objects.filter(ri__meterial__sOrg=a,collNo=b).values("id", "vendor_id", "collNo", "ri__meterial__material_id",
                                                   "ri__quantity", "vendor__vname", "price","euser__material__mname")
        quotation = list(quotation)
        for i in quotation:
            vendorid = i['vendor_id']
            orderitem = OrderItem.objects.filter(po__vendor=vendorid).values()
            orderitem = list(orderitem)
            print(orderitem)
            sum = 0
            ontimeScore = 0
            quantityScore = 0
            serviceScore = 0
            qualityScore = 0
            for j in orderitem:
                sum += j['price'] * j['quantity']
            for p in orderitem:
                print(p['ontimeScore'])
                if p['ontimeScore'] == None:
                    p['ontimeScore'] = 0
                if p['quantityScore'] == None:
                    p['quantityScore'] = 0
                if p['serviceScore'] == None:
                    p['serviceScore'] = 0
                if p['qualityScore'] == None:
                    p['qualityScore'] = 0
                quanzhong = p['price'] * p['quantity'] / sum
                ontimeScore += p['ontimeScore'] * quanzhong
                quantityScore += p['quantityScore'] * quanzhong
                serviceScore += p['serviceScore'] * quanzhong
                qualityScore += p['qualityScore'] * quanzhong
            i['qualityScore'] = round(qualityScore,1)
            i['serviceScore'] = round(serviceScore,1)
            i['quantityScore'] = round(quantityScore,1)
            i['ontimeScore'] = round(ontimeScore,1)
            i['sum'] = sum
            i['avgscore'] = round((quantityScore + serviceScore + quantityScore + ontimeScore) / 4,1)
        quotation.sort(key=lambda x: x["avgscore"], reverse=True)
        for i in range(len(quotation)):
            quotation[i]['paiming'] = i+1
        return render(request, '../templates/quotation/vq-value.html', locals())






@csrf_exempt
def searchpo(request):
    if request.method == "GET":
        vendorid =  PurchaseOrder.objects.all().values('rfq__quantity','rfq__price','id','rfq__ri__meterial_id',
                                                       'euser_id','time','rfq__rej','vendor_id','rfq__collNo','rfq__ri__itemId',
                                                       'rfq__ri__currency','rfq__ri__status')
        for i in vendorid:
            i['sum'] = i['rfq__quantity']*i['rfq__price']
        for i in vendorid:
            if i['rfq__ri__status']=='0':
                i['rfq__ri__status'] = "已创建采购申请"
            if i['rfq__ri__status']=='1':
                i['rfq__ri__status'] = "已创建采购订单"
        vendorid = list(vendorid)
        print(vendorid)
        return render(request, '../templates/purchaseorder/purchase_order.html', locals())
    if request.method == "POST":
        id = request.POST.get("id")
        ven = request.POST.get("ven")
        mate = request.POST.get("mate")
        eu = request.POST.get("euser")
        vendorid = PurchaseOrder.objects.filter(id=id,vendor_id=ven,
                                                rfq__ri__meterial=mate,
                                                euser_id=eu,
                                                ).values('rfq__quantity', 'rfq__price', 'id', 'rfq__ri__meterial_id',
                                                      'euser_id', 'time', 'rfq__rej', 'vendor_id', 'rfq__collNo','rfq__ri__itemId',
                                                         'rfq__ri__currency','rfq__ri__status')
        print(vendorid)
        for i in vendorid:
            i['sum'] = i['rfq__quantity']*i['rfq__price']
        for i in vendorid:
            if i['rfq__ri__status']=='0':
                i['rfq__ri__status'] = "已创建采购申请"
            if i['rfq__ri__status']=='1':
                i['rfq__ri__status'] = "已创建采购订单"
        vendorid = list(vendorid)
        return render(request, '../templates/purchaseorder/purchase_order.html', locals())



@csrf_exempt
def searchqo(request):
    if request.method == "GET":
        vendorid =  Quotation.objects.all().values("id","euser_id","ri__meterial__material_id","vendor_id","time")
        vendorid = list(vendorid)
        return render(request, '../templates/quotation/vendor_quotation.html', locals())
    if request.method == "POST":
        id = request.POST.get("id")
        print(id)
        ven = request.POST.get("ven")
        print(ven)
        mate = request.POST.get("mate")
        print(mate)
        eu = request.POST.get("euser")
        print(eu)
        collNo = request.POST.get("collNo")
        print(collNo)
        vendorid = Quotation.objects.filter(id=id,vendor_id=ven,
                                                euser_id=eu,collNo=collNo
                                                ).values("id","euser_id","ri__meterial__material_id","vendor_id","time")
        print(vendorid)
        vendorid = list(vendorid)
        return render(request, '../templates/quotation/vendor_quotation.html', locals())




@csrf_exempt
def searchpo(request):
    if request.method == "GET":
        vendorid =  PurchaseOrder.objects.all().values('rfq__quantity','rfq__price','id','rfq__ri__meterial_id',
                                                       'euser_id','time','rfq__rej','vendor_id','rfq__collNo','rfq__ri__itemId',
                                                       'rfq__ri__currency','rfq__ri__status')
        for i in vendorid:
            if i['rfq__quantity']==None:
                i['rfq__quantity']=0
            if i['rfq__price']==None:
                i['rfq__price'] =0
            i['sum'] = i['rfq__quantity']*i['rfq__price']
        for i in vendorid:
            if i['rfq__ri__status']=='0':
                i['rfq__ri__status'] = "已创建采购申请"
            if i['rfq__ri__status']=='1':
                i['rfq__ri__status'] = "已创建采购订单"
        vendorid = list(vendorid)
        print(vendorid)
        return render(request, '../templates/purchaseorder/purchase_order.html', locals())
    if request.method == "POST":
        id = request.POST.get("id")
        ven = request.POST.get("ven")
        mate = request.POST.get("mate")
        eu = request.POST.get("euser")
        vendorid = PurchaseOrder.objects.filter(id=id,vendor_id=ven,
                                                rfq__ri__meterial=mate,
                                                euser_id=eu,
                                                ).values('rfq__quantity', 'rfq__price', 'id', 'rfq__ri__meterial_id',
                                                      'euser_id', 'time', 'rfq__rej', 'vendor_id', 'rfq__collNo','rfq__ri__itemId',
                                                         'rfq__ri__currency','rfq__ri__status')
        print(vendorid)
        for i in vendorid:
            i['sum'] = i['rfq__quantity']*i['rfq__price']
        for i in vendorid:
            if i['rfq__ri__status']=='0':
                i['rfq__ri__status'] = "已创建采购申请"
            if i['rfq__ri__status']=='1':
                i['rfq__ri__status'] = "已创建采购订单"
        vendorid = list(vendorid)
        return render(request, '../templates/purchaseorder/purchase_order.html', locals())







@csrf_exempt
def searchpo2(request):
    if request.method == "GET":
        vendorid =  PurchaseOrder.objects.all().values('rfq__quantity','rfq__price','id','rfq__ri__meterial_id',
                                                       'euser_id','time','rfq__rej','vendor_id','rfq__collNo','rfq__ri__itemId',
                                                       'rfq__ri__currency','rfq__ri__status')
        for i in vendorid:
            i['sum'] = i['rfq__quantity']*i['rfq__price']
        for i in vendorid:
            if i['rfq__ri__status']=='0':
                i['rfq__ri__status'] = "已创建采购申请"
            if i['rfq__ri__status']=='1':
                i['rfq__ri__status'] = "已创建采购订单"
        vendorid = list(vendorid)
        print(vendorid)
        return render(request, '../templates/receipt/purchase_order.html', locals())
    if request.method == "POST":
        id = request.POST.get("id")
        ven = request.POST.get("ven")
        mate = request.POST.get("mate")
        eu = request.POST.get("euser")
        vendorid = PurchaseOrder.objects.filter(id=id,vendor_id=ven,
                                                rfq__ri__meterial=mate,
                                                euser_id=eu,
                                                ).values('rfq__quantity', 'rfq__price', 'id', 'rfq__ri__meterial_id',
                                                      'euser_id', 'time', 'rfq__rej', 'vendor_id', 'rfq__collNo','rfq__ri__itemId',
                                                         'rfq__ri__currency','rfq__ri__status')
        print(vendorid)
        for i in vendorid:
            i['sum'] = i['rfq__quantity']*i['rfq__price']
        for i in vendorid:
            if i['rfq__ri__status']=='0':
                i['rfq__ri__status'] = "已创建采购申请"
            if i['rfq__ri__status']=='1':
                i['rfq__ri__status'] = "已创建采购订单"
        vendorid = list(vendorid)
        return render(request, '../templates/receipt/purchase_order.html', locals())







@csrf_exempt
def searchpo3(request):
    if request.method == "GET":
        vendorid =  PurchaseOrder.objects.all().values('rfq__quantity','rfq__price','id','rfq__ri__meterial_id',
                                                       'euser_id','time','rfq__rej','vendor_id','rfq__collNo','rfq__ri__itemId',
                                                       'rfq__ri__currency','rfq__ri__status')
        for i in vendorid:
            i['sum'] = i['rfq__quantity']*i['rfq__price']
        for i in vendorid:
            if i['rfq__ri__status']=='0':
                i['rfq__ri__status'] = "已创建采购申请"
            if i['rfq__ri__status']=='1':
                i['rfq__ri__status'] = "已创建采购订单"
        vendorid = list(vendorid)
        print(vendorid)
        return render(request, '../templates/invoice/purchase_order.html', locals())
    if request.method == "POST":
        id = request.POST.get("id")
        ven = request.POST.get("ven")
        mate = request.POST.get("mate")
        eu = request.POST.get("euser")
        vendorid = PurchaseOrder.objects.filter(id=id,vendor_id=ven,
                                                rfq__ri__meterial=mate,
                                                euser_id=eu,
                                                ).values('rfq__quantity', 'rfq__price', 'id', 'rfq__ri__meterial_id',
                                                      'euser_id', 'time', 'rfq__rej', 'vendor_id', 'rfq__collNo','rfq__ri__itemId',
                                                         'rfq__ri__currency','rfq__ri__status')
        print(vendorid)
        for i in vendorid:
            i['sum'] = i['rfq__quantity']*i['rfq__price']
        for i in vendorid:
            if i['rfq__ri__status']=='0':
                i['rfq__ri__status'] = "已创建采购申请"
            if i['rfq__ri__status']=='1':
                i['rfq__ri__status'] = "已创建采购订单"
        vendorid = list(vendorid)
        return render(request, '../templates/invoice/purchase_order.html', locals())






@csrf_exempt
def searchjiekou(request):
    if request.method == "POST":
        print("111")
        cname = request.POST.get("cname")
        ctime = request.POST.get("ctime")
        gcode = request.POST.get("gcode")
        reque = RequisitionItem.objects.filter(deliveryDate=ctime,pr__euser_id=cname,
                                               meterial_id=gcode).values("pr_id","pr__euser_id","deliveryDate",
                                                                         "meterial__id","itemId")
        reque = list(reque)
        return HttpResponse(reque)



@csrf_exempt
def searchjiekouzhuanhua(request):
    if request.method == "POST":
        print("111")
        cname = request.POST.get("cname")
        ctime = request.POST.get("ctime")
        ctime = getDate2(ctime)
        gcode = request.POST.get("gcode")
        reque = RequisitionItem.objects.filter(deliveryDate=ctime,pr__euser_id=cname,
                                               meterial_id=gcode).values("pr_id","pr__euser_id","deliveryDate",
                                                                         "meterial__id","itemId")
        reque = list(reque)
        return HttpResponse(reque)






@csrf_exempt
def choose(request):
    if request.method == "GET":

        return render(request, '../templates/purchaseorder/po-create_choose.html', locals())