from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.decorators import login_required

from ..models import EUser, Vendor
from .auxiliary import *

@login_required
def create(request: HttpRequest):
    user = request.user
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/vendor/create.html',
        )
    else:
        return HttpResponse(status=405)

@login_required
def search(request: HttpRequest):
    user = request.user
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/vendor/search.html'
        )
    else:
        return HttpResponse(status=405)

@login_required
def history(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/vendor/history.html'
        )
    else:
        return HttpResponse(status=405)