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
def search_vendor_history(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponse(status=405)
    post = request.POST # test
    range = int(post.get('range'))
    mid = getPkExact(post.get('mid'), 'V')
    w1 = int(post.get('w1')); w2 = int(post.get('w2')); w3 = int(post.get('w3')); w4 = int(post.get('w4'))
    range_list = [12, 6, 3]
    now = timezone.now()
    start = now + datetime.timedelta(days=-30 * range_list[range])
    history = OrderItem.objects.filter(
        meterial__id=mid, po__time__range=[start, now]
    )
    history_not_null = history.exclude(qualityScore__isnull=True
    ).exclude(serviceScore__isnull=True).exclude(quantityScore__isnull=True
    ).exclude(ontimeScore__isnull=True)
    response = history_not_null.values_list('po__vendor').annotate(
        quan=Sum(F('price') * F('quantity')), num=Count('id'), score=Sum(
            (F('quantityScore')*w1+F('qualityScore')*w2+F('serviceScore')*w3+F('ontimeScore')*w4) * (F('price') * F('quantity'))
        ) / Sum(F('price') * F('quantity'))
    )
    vendor_list = list(response)
    for i,x in enumerate(response):
        vendor: Vendor = Vendor.objects.get(pk__exact=x[0])
        vendor_list[i] = {
            'vendor':model_to_dict(vendor), 'quan':vendor_list[i][1],
            'num':vendor_list[i][2], 'score':vendor_list[i][3],
        }
    return HttpResponse(json.dumps(vendor_list, default=str))
