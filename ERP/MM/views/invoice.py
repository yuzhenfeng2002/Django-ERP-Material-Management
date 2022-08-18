from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.decorators import login_required

from ..models import EUser, Material, MaterialItem, Stock
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