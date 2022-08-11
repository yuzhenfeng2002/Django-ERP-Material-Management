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
def display_material(request: HttpRequest, pk):
    pk = str(int(pk)) # turn '002' into '2'
    material = get_object_or_404(Material, pk=pk)
    form = MaterialForm(instance=material)
    return render(
        request=request,
        template_name='../templates/material/material/display.html',
        context={'form': form, 'pk': material.pk}
    )

@login_required
def update_material(request: HttpRequest):
    pk = request.POST.get('pk')
    pk = str(int(pk)) # turn '002' into '2'
    material: Material = get_object_or_404(Material, pk=pk)
    form = MaterialForm(request.POST, instance=material)
    error_message = None

    if error_message is None:
        if form.is_valid():
            material.save()
            messages.success(request=request, message="Successfully updated!")
            return HttpResponseRedirect(reverse('MM:display_material', args=(material.pk,)))
        else:
            return render(
                request=request,
                template_name='../templates/material/material/display.html',
                context={'form': form, 'pk': int(pk)}
            )
    else:
        messages.error(request=request, message=error_message)
        return HttpResponseRedirect(reverse('MM:display_material', args=(material.pk,)))

@login_required
def search_material(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/material/material/search.html'
        )
    elif request.method == 'POST':
        post = request.POST
        pk = getPk(post.get('pk'))
        mname = getRegex(post.get('mname'))
        mType = getRegex(post.get('mType'))
        industrySector = getRegex(post.get('industrySector'))
        materials = Material.objects.filter(
            pk__regex=pk, mname__regex=mname, mType__regex=mType, industrySector__regex=industrySector
        )
        
        if len(materials) > 0:
            messages.success(request=request, message="Succeed to get {:} results.".format(len(materials)))
            return render(
                request=request,
                template_name='../templates/material/material/search.html',
                context={'materials':materials}
            )
        else:
            messages.success(request=request, message="There is no matched result.")
            return render(
                request=request,
                template_name='../templates/material/material/search.html',
            )

class ItemForm(forms.ModelForm):
    material_id = forms.CharField()
    stock_id = forms.CharField()
    class Meta:
        model = MaterialItem
        fields = (
            'sloc', 'sOrg', 'distrChannel', 'unrestrictUse',
            'blocked', 'qltyInspection', 'transit'
        )

@login_required
def create_item(request: HttpRequest):
    user = request.user
    if request.method == 'GET':
        form = ItemForm()
        return render(
            request=request,
            template_name='../templates/material/item/create.html',
            context={'form': form}
        )
    elif request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item: MaterialItem = form.instance
            material_id = int(request.POST.get('material_id'))
            stock_id = int(request.POST.get('stock_id'))
            material = Material.objects.get(pk=material_id)
            stock = Stock.objects.get(pk=stock_id)
            item.material = material
            item.stock = stock
            item.save()
            messages.success(request=request, message="Successfully created!")
            return HttpResponseRedirect(reverse('MM:display_item', args=(item.pk,)))
        else:
            return render(
                request=request,
                template_name='../templates/material/item/create.html',
                context={'form': form}
            )

@login_required
def display_item(request: HttpRequest, pk):
    pk = str(int(pk)) # turn '002' into '2'
    item: MaterialItem = get_object_or_404(MaterialItem, pk=pk)
    form = ItemForm(instance=item)
    form.fields['material_id'].initial = item.material.id
    form.fields['stock_id'].initial = item.stock.id
    return render(
        request=request,
        template_name='../templates/material/item/display.html',
        context={'form': form, 'pk': item.pk}
    )

@login_required
def update_item(request: HttpRequest):
    pk = request.POST.get('pk')
    pk = str(int(pk)) # turn '002' into '2'
    material: Material = get_object_or_404(Material, pk=pk)
    form = MaterialForm(request.POST, instance=material)
    error_message = None

    if error_message is None:
        if form.is_valid():
            material.save()
            messages.success(request=request, message="Successfully updated!")
            return HttpResponseRedirect(reverse('MM:display_material', args=(material.pk,)))
        else:
            return render(
                request=request,
                template_name='../templates/material/material.html',
                context={'form': form, 'pk': int(pk)}
            )
    else:
        messages.error(request=request, message=error_message)
        return HttpResponseRedirect(reverse('MM:display_material', args=(material.pk,)))

@login_required
def search_item(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/material/item/search.html'
        )
    elif request.method == 'POST':
        post = request.POST
        pk = getPk(post.get('pk'))
        mname = getRegex(post.get('mname'))
        mType = getRegex(post.get('mType'))
        industrySector = getRegex(post.get('industrySector'))
        materials = Material.objects.filter(
            pk__regex=pk, mname__regex=mname, mType__regex=mType, industrySector__regex=industrySector
        )
        
        if len(materials) > 0:
            messages.success(request=request, message="Succeed to get {:} results.".format(len(materials)))
            return render(
                request=request,
                template_name='../templates/material/search_material.html',
                context={'materials':materials}
            )
        else:
            messages.success(request=request, message="There is no matched result.")
            return render(
                request=request,
                template_name='../templates/material/search_material.html',
            )