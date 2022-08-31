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
import json
import datetime

from ...models import *
from ..auxiliary import *

@login_required
def create_vendor(request: HttpRequest):
    post = request.POST
    vname = post.get('vname')
    city = post.get('city')
    address = post.get('address')
    postcode = post.get('postcode')
    country = post.get('country')
    language = post.get('language')
    glAcount = post.get('glAcount')
    phone = post.get('phone')
    fax = post.get('fax')
    tpType = post.get('tpType')
    companyCode = post.get('companyCode')
    pOrg = post.get('pOrg')
    currency = post.get('currency')
    new_vendor = Vendor(
        vname=vname, city=city, address=address, country=country,
        postcode=postcode, language=language, glAcount=glAcount,
        phone=phone, fax=fax, tpType=tpType, companyCode=companyCode, 
        pOrg=pOrg, currency=currency, 
    )
    user = request.user
    euser = EUser.objects.get(pk=user.pk)
    new_vendor.euser = euser
    try:
        new_vendor.full_clean()
    except ValidationError as e:
        error_fields = list(e.error_dict.keys())
        return HttpResponse(json.dumps({'status':0, 'message':"表单填写错误！", 'fields':error_fields}))
    new_vendor.save()
    return HttpResponse(json.dumps({'status':1, 'message':"供应商创建成功！供应商编号为"+str(new_vendor.vid)+"。", 'vendor':model_to_dict(new_vendor)}))

@login_required
def search_vendor_history(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponse(status=405)
    post = request.POST # test
    range = int(post.get('range'))
    mid = getPkExact(post.get('mid'), 'V')
    w1 = float(post.get('w1'))/100; w2 = float(post.get('w2'))/100; w3 = float(post.get('w3'))/100; w4 = float(post.get('w4'))/100
    range_list = [12, 6, 3]
    now = timezone.now()
    start = now + datetime.timedelta(days=-30 * range_list[range])
    history = OrderItem.objects.filter(
        meterialItem__material__id=mid, po__time__range=[start, now]
    )
    history_not_null = history.exclude(qualityScore__isnull=True
    ).exclude(serviceScore__isnull=True).exclude(quantityScore__isnull=True
    ).exclude(ontimeScore__isnull=True)
    response: QuerySet = history_not_null.values_list('po__vendor').annotate(
        quan=Sum(F('price') * F('quantity')), num=Count('id'), score=Sum(
            (F('quantityScore')*w1+F('qualityScore')*w2+F('serviceScore')*w3+F('ontimeScore')*w4) * (F('price') * F('quantity'))
        ) / Sum(F('price') * F('quantity'))
    )
    response = response.order_by('-score')
    vendor_list = list(response)
    for i,x in enumerate(response):
        vendor: Vendor = Vendor.objects.get(pk__exact=x[0])
        vendor_list[i] = {
            'vendor':model_to_dict(vendor), 'quan':vendor_list[i][1],
            'num':vendor_list[i][2], 'score':vendor_list[i][3],
        }
    return HttpResponse(json.dumps(vendor_list, default=str))

@login_required
def search_vendor(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponse(status=405)
    post = request.POST
    pk = post.get('pk')
    if pk == '' or pk is None:
        vname = getRegex(post.get('vname'))
        uid = getPk(post.get('uid'), 'U')
        city = getRegex(post.get('city'))
        country = getRegex(post.get('country'))
        companyCode = getRegex(post.get('company'))
        vendors = Vendor.objects.filter(
            vname__regex=vname, euser__uid__regex=uid, city__regex=city,
            country__regex=country, companyCode__regex=companyCode
        )
        vendor_list = json.loads(serializers.serialize('json', list(vendors)))
        for i, vendor in enumerate(vendors):
            user: EUser = EUser.objects.get(pk__exact=vendor.euser.pk)
            vendor_list[i]['user'] = model_to_dict(user)
        return HttpResponse(json.dumps(vendor_list, default=str))
    else:
        pk = getPkExact(pk, 'V')
        vendors: QuerySet = Vendor.objects.filter(pk__exact=pk)
        if len(vendors) != 1:
            return HttpResponse(json.dumps({'status':0, 'message':"物料相关信息错误！"}))
        else:
            return HttpResponse(json.dumps({'status':1, 'message':"查找成功！", 'vendor':model_to_dict(vendors.first())}))

@login_required
def update_vendor(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponse(status=405)
    post = request.POST
    vid = post.get('vid')
    uid = post.get('uid')
    vendors = Vendor.objects.filter(vid__exact=vid)
    if len(vendors) != 1:
        return HttpResponse(json.dumps({'status':0, 'message':"物料相关信息错误！"}))
    vendor: Vendor = vendors.first()
    vname = post.get('vname')
    city = post.get('city')
    address = post.get('address')
    postcode = post.get('postcode')
    country = post.get('country')
    language = post.get('language')
    glAcount = post.get('glAcount')
    phone = post.get('phone')
    fax = post.get('fax')
    tpType = post.get('tpType')
    companyCode = post.get('companyCode')
    pOrg = post.get('pOrg')
    currency = post.get('currency')
    vendor.vname=vname; vendor.city=city; vendor.address=address; vendor.country=country
    vendor.postcode=postcode; vendor.language=language; vendor.glAcount=glAcount
    vendor.phone=phone; vendor.fax=fax; vendor.tpType=tpType; vendor.companyCode=companyCode
    vendor.pOrg=pOrg; vendor.currency=currency
    try:
        vendor.full_clean()
    except ValidationError as e:
        error_fields = list(e.error_dict.keys())
        return HttpResponse(json.dumps({'status':0, 'message':"表单填写错误！", 'fields':error_fields}))
    vendor.save()
    return HttpResponse(json.dumps({'status':1, 'message':"供应商信息已更新！"}))