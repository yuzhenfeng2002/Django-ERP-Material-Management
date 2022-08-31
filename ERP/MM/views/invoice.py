import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.db.models import QuerySet, Sum, F
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.utils import timezone

from ..models import *
from .auxiliary import *

@login_required
def create_invoice(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/invoice/create.html'
        )
    else:
        return HttpResponse(status=405)

@login_required
def search_invoice(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/invoice/search.html'
        )
    else:
        return HttpResponse(status=405)

@login_required
def payment(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/invoice/pay.html'
        )
    else:
        return HttpResponse(status=405)

@login_required
def display_invoice(request: HttpRequest):
    get = request.GET
    pk = getPkExact(get.get('pk'))
    invoice: Invoice = Invoice.objects.get(pk__exact=pk)
    item: OrderItem = get_object_or_404(OrderItem, pk=invoice.pk)
    item_dict = model_to_dict(item)
    materialItem: MaterialItem = get_object_or_404(MaterialItem, id__exact=item.meterialItem.id)
    material: Material = get_object_or_404(Material, id__exact=materialItem.material.id)
    stock: Stock = get_object_or_404(Stock, id__exact=materialItem.stock.id)
    po: PurchaseOrder = get_object_or_404(PurchaseOrder, id__exact=item.po.id)
    vendor: Vendor = get_object_or_404(Vendor, vid__exact=po.vendor.vid)
    gr: GoodReceipt = get_object_or_404(GoodReceipt, orderItem__id__exact=item.id)
    item_dict['po'] = model_to_dict(po)
    item_dict['materialItem'] = model_to_dict(materialItem)
    item_dict['material'] = model_to_dict(material)
    item_dict['stock'] = model_to_dict(stock)
    item_dict['invoice'] = model_to_dict(invoice)
    item_dict['vendor'] = model_to_dict(vendor)
    item_dict['gr'] = model_to_dict(gr)
    return render(
        request=request,
        template_name='../templates/invoice/display.html',
        context={'context': item_dict}
    )

@login_required
def load_order_item(request: HttpRequest):
    get = request.GET
    orderID = get.get('orderID')
    itemID = get.get('itemID')
    item: OrderItem = get_object_or_404(OrderItem, po__id__exact=orderID, itemId__exact=itemID)
    item_dict = model_to_dict(item)
    materialItem: MaterialItem = get_object_or_404(MaterialItem, id__exact=item.meterialItem.id)
    material: Material = get_object_or_404(Material, id__exact=materialItem.material.id)
    stock: Stock = get_object_or_404(Stock, id__exact=materialItem.stock.id)
    po: PurchaseOrder = get_object_or_404(PurchaseOrder, id__exact=item.po.id)
    item_dict['po_'] = model_to_dict(po)
    item_dict['materialItem_'] = model_to_dict(materialItem)
    item_dict['material_'] = model_to_dict(material)
    item_dict['stock_'] = model_to_dict(stock)
    return render(
        request=request,
        template_name='../templates/invoice/create2.html',
        context={'context': item_dict}
    )

@login_required
def display_purchase_order(request: HttpRequest, pk):
    if request.method == "GET":
        pk = getPkExact(pk, "O")
        purchaseOrder: PurchaseOrder = PurchaseOrder.objects.get(id=pk)
        vendor: Vendor =  Vendor.objects.get(vid=purchaseOrder.vendor.vid)
        orderItems  = OrderItem.objects.filter(po_id=pk).values(
            "itemId","meterialItem__id","meterialItem__material__mname",
            "quantity","price","meterialItem__stock__id", "meterialItem__stock__name",
            "meterialItem__sloc","deliveryDate","po__rfq__rej","currency","status"
        )
        orderItems = list(orderItems)
        for i in orderItems:
            if i['status']=='0':
                i['status']="货物未发出"
            if i['status']=='1':
                i['status']="货物已送达"
            if i['status']=='2':
                i['status']="已收到发票"
            if i['status']=='3':
                i['status']="已完成支付"
        sum = 0
        for i in orderItems:
            i['sum'] = i['quantity'] * i['price']
            sum += i['sum']
        return render(
            request, '../templates/invoice/order.html',
            context={
                "purchaseOrder": purchaseOrder, "vendor": vendor, "orderItems": orderItems,
                "sum": sum, "itemNum": len(orderItems), "currency": orderItems[0]['currency'],
                "user_id": purchaseOrder.euser.uid
            }    
        )

@login_required
def search_orders(request):
    if request.method == "GET":
        purchaseOrders = []
        return render(request, '../templates/receipt/orders.html', context={"purchaseOrders":purchaseOrders})
    if request.method == "POST":
        id = request.POST.get("id"); id = getPk(id)
        ven = request.POST.get("ven"); ven = getPk(ven)
        mate = request.POST.get("mate"); mate = getPk(mate)
        eu = request.POST.get("euser"); eu = getPk(eu)
        range = int(request.POST.get("range"))
        range_list = [12, 6, 3]
        now = timezone.now()
        start = now + datetime.timedelta(days=-30 * range_list[range])
        orderItems: QuerySet = OrderItem.objects.filter(
            po__id__regex=id, po__vendor__vid__regex=ven, meterialItem__material__id__regex=mate,
            po__euser__uid__regex=eu, po__time__range=[start, now]
        )
        orderItems: QuerySet = orderItems.values(
            "po__id", "itemId", "meterialItem__material__mname", "quantity", "price", "currency",
            "po__euser__uid", "po__vendor__vid", "po__time", "status", sum=F("quantity")*F("price")
        ).order_by("po__id")
        orderItems = list(orderItems)
        for i in orderItems:
            if i['status']=='0':
                i['status']="货物未发出"
            if i['status']=='1':
                i['status']="货物已送达"
            if i['status']=='2':
                i['status']="已收到发票"
            if i['status']=='3':
                i['status']="已完成支付"
                i['rfq__ri__status'] = "已创建采购订单"
        return render(request, '../templates/invoice/orders.html', {"orderItems":orderItems})