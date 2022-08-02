from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django import forms
from django.contrib.auth.decorators import login_required

from ..models import EUser, Vendor

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = (
            'vname', 'city', 'country', 'address', 'postcode', 'language',
            'glAcount', 'tpType', 'complanyCode', 'currency'
        )

@login_required
def create(request: HttpRequest):
    user = request.user
    if request.method == 'GET':
        form = VendorForm()
        return render(
            request=request,
            template_name='../templates/vendor/vendor.html',
            context={'form': form}
        )
    elif request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor: Vendor = form.instance
            euser = EUser.objects.get(pk=user.pk)
            vendor.euser = euser
            vendor.score = 100
            # vendor.save()
            # return HttpResponseRedirect(reverse('MM:display_vendor', args=(vendor.pk,)))
            return HttpResponse("Succeed!")

@login_required
def display(request: HttpRequest, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    form = VendorForm(instance=vendor)
    return render(
        request=request,
        template_name='../templates/vendor/vendor.html',
        context={'form': form, 'pk': vendor.pk}
    )

