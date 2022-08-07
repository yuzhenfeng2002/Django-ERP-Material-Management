from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.core import serializers

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