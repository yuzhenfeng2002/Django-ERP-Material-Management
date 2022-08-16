from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.decorators import login_required

from ..models import EUser, Material, MaterialItem, Stock
from .auxiliary import *

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = (
            'mname', 'mType', 'mGroup', 'meaunit',
            'netWeight', 'weightUnit', 'transGrp',
            'loadingGrp', 'industrySector'
        )

@login_required
def create_material(request: HttpRequest):
    user = request.user
    if request.method == 'GET':
        form = MaterialForm()
        return render(
            request=request,
            template_name='../templates/material/material/create.html',
            context={'form': form}
        )
    elif request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material: Material = form.instance
            material.save()
            messages.success(request=request, message="Successfully created!")
            return HttpResponseRedirect(reverse('MM:display_material', args=(material.pk,)))
        else:
            return render(
                request=request,
                template_name='../templates/material/material/create.html',
                context={'form': form}
            )

@login_required
def search_material(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/material/search.html'
        )
    else:
        return HttpResponse(status=405)

@login_required
def search_item_stock(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/material/stock.html'
        )
    else:
        return HttpResponse(status=405)

@login_required
def create_item(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/material/create.html'
        )
    else:
        return HttpResponse(status=405)