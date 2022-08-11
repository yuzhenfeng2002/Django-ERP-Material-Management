from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.forms.models import model_to_dict
import json

from ...models import EUser, Material, MaterialItem, Stock
from ..auxiliary import *

@login_required
def search_material(request: HttpRequest):
    post = request.POST
    mname = getRegex(post.get('mname'))
    mType = getRegex(post.get('mType'))
    industrySector = getRegex(post.get('industrySector'))
    materials = Material.objects.filter(
        mname__regex=mname, mType__regex=mType, industrySector__regex=industrySector
    )
    return HttpResponse(serializers.serialize('json', list(materials)))

@login_required
def search_item(request: HttpRequest):
    post = request.POST
    mname = getRegex(post.get('mname'))
    mType = getRegex(post.get('mType'))
    industrySector = getRegex(post.get('industrySector'))
    stock_id = getRegex(post.get('stock'))
    sloc = getRegex(post.get('sloc'))
    items = MaterialItem.objects.filter(
        material__mname__regex=mname, material__mType__regex=mType, 
        material__industrySector__regex=industrySector, stock__id__regex=stock_id,
        sloc__regex=sloc
    )
    items_list = json.loads(serializers.serialize('json', list(items)))
    for i, item in enumerate(items):
        material: Material = Material.objects.get(pk__exact=item.material.pk)
        stock: Stock = Stock.objects.get(pk__exact=item.stock.pk)
        items_list[i]['material'] = model_to_dict(material)
        items_list[i]['stock'] = model_to_dict(stock)
    return HttpResponse(json.dumps(items_list))

@login_required
def search_stock(request: HttpRequest):
    post = request.POST
    client = getRegex(post.get('client'))
    companyCode = getRegex(post.get('companyCode'))
    pOrg = getRegex(post.get('pOrg'))
    pGrp = getRegex(post.get('pGrp'))
    stocks = Stock.objects.filter(
        client__regex=client, companyCode__regex=companyCode, pOrg__regex=pOrg, pGrp__regex=pGrp
    )
    return HttpResponse(serializers.serialize('json', list(stocks)))