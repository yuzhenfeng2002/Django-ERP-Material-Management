from aem import Query
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from psutil import users
from ..models import EUser

def login(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/user/login.html',
        )
    if request.method == 'POST':
        email = request.POST.get('email')
        user = EUser.objects.filter(email__exact=email).get()
