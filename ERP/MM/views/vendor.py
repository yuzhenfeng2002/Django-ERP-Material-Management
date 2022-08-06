from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.decorators import login_required

from ..models import EUser, Vendor

def getRegex(string):
    if string == '':
        return r'.*'
    else:
        return string

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = (
            'vname', 'city', 'country', 'address', 'postcode', 'language',
            'phone', 'fax', 'companyCode', 'pOrg',
            'glAcount', 'tpType', 'currency'
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
            vendor.save()
            messages.success(request=request, message="Successfully created!")
            return HttpResponseRedirect(reverse('MM:display_vendor', args=(vendor.pk,)))
        else:
            return render(
                request=request,
                template_name='../templates/vendor/vendor.html',
                context={'form': form}
            )

@login_required
def display(request: HttpRequest, pk):
    pk = str(int(pk)) # turn '002' into '2'
    vendor = get_object_or_404(Vendor, pk=pk)
    form = VendorForm(instance=vendor)
    return render(
        request=request,
        template_name='../templates/vendor/vendor.html',
        context={'form': form, 'pk': vendor.pk}
    )

@login_required
def update(request: HttpRequest):
    pk = request.POST.get('pk')
    pk = str(int(pk)) # turn '002' into '2'
    user = request.user
    vendor: Vendor = get_object_or_404(Vendor, pk=pk)
    form = VendorForm(request.POST, instance=vendor)
    error_message = None

    if vendor.euser.pk != user.pk:
        error_message = "You do not have access to the vendor."
    
    if error_message is None:
        if form.is_valid():
            vendor.save()
            messages.success(request=request, message="Successfully updated!")
            return HttpResponseRedirect(reverse('MM:display_vendor', args=(vendor.pk,)))
        else:
            return render(
                request=request,
                template_name='../templates/vendor/vendor.html',
                context={'form': form, 'pk': pk}
            )
    else:
        messages.error(request=request, message=error_message)
        return HttpResponseRedirect(reverse('MM:display_vendor', args=(vendor.pk,)))

@login_required
def search(request: HttpRequest):
    user = request.user
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/vendor/search.html'
        )
    elif request.method == 'POST':
        post = request.POST
        pk = getRegex(str(int(post.get('pk'))))
        vname = getRegex(post.get('vname'))
        uid = getRegex(post.get('uid'))
        city = getRegex(post.get('city'))
        country = getRegex(post.get('country'))
        companyCode = getRegex(post.get('companyCode'))
        vendors = Vendor.objects.filter(
            pk__regex=pk, vname__regex=vname, euser__uid__regex=uid, city__regex=city,
            country__regex=country, companyCode__regex=companyCode
        )
        
        if len(vendors) > 0:
            messages.success(request=request, message="Succeed to get {:} results.".format(len(vendors)))
            return render(
                request=request,
                template_name='../templates/vendor/search.html',
                context={'vendors':vendors}
            )
        else:
            messages.success(request=request, message="There is no matched result.")
            return render(
                request=request,
                template_name='../templates/vendor/search.html',
            )