from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models import QuerySet, Sum
import json
import pandas as pd
from ...models import EUser

DATA_URL = './MM/data/'

@login_required
def load_user(request: HttpRequest):
    user: QuerySet = EUser.objects.all()
    return HttpResponse(json.dumps(list(user), default=str))
