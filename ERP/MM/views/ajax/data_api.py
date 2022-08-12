from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.forms.models import model_to_dict
import json
import pandas as pd

DATA_URL = './MM/data/'

@login_required
def load_country(request: HttpRequest):
    df = pd.read_csv(DATA_URL+'country.csv')
    df_dict = df.to_dict(orient='index')
    return HttpResponse(json.dumps(list(df_dict.values())))

@login_required
def load_company(request: HttpRequest):
    df = pd.read_csv(DATA_URL+'company.csv')
    df_dict = df.to_dict(orient='index')
    return HttpResponse(json.dumps(list(df_dict.values())))

@login_required
def load_currency(request: HttpRequest):
    df = pd.read_csv(DATA_URL+'currency.csv')
    df_dict = df.to_dict(orient='index')
    return HttpResponse(json.dumps(list(df_dict.values())))

@login_required
def load_language(request: HttpRequest):
    df = pd.read_csv(DATA_URL+'language.csv')
    df_dict = df.to_dict(orient='index')
    return HttpResponse(json.dumps(list(df_dict.values())))

@login_required
def load_meaunit(request: HttpRequest):
    df = pd.read_csv(DATA_URL+'meaunit.csv')
    df_dict = df.to_dict(orient='index')
    return HttpResponse(json.dumps(list(df_dict.values())))

@login_required
def load_pgrp(request: HttpRequest):
    df = pd.read_csv(DATA_URL+'pgrp.csv')
    df_dict = df.to_dict(orient='index')
    return HttpResponse(json.dumps(list(df_dict.values())))

@login_required
def load_plant(request: HttpRequest):
    df = pd.read_csv(DATA_URL+'plant.csv')
    df_dict = df.to_dict(orient='index')
    return HttpResponse(json.dumps(list(df_dict.values())))

@login_required
def load_porg(request: HttpRequest):
    df = pd.read_csv(DATA_URL+'porg.csv')
    df_dict = df.to_dict(orient='index')
    return HttpResponse(json.dumps(list(df_dict.values())))

@login_required
def load_sorg(request: HttpRequest):
    df = pd.read_csv(DATA_URL+'sorg.csv')
    df_dict = df.to_dict(orient='index')
    return HttpResponse(json.dumps(list(df_dict.values())))

@login_required
def load_tptype(request: HttpRequest):
    df = pd.read_csv(DATA_URL+'tptype.csv')
    df_dict = df.to_dict(orient='index')
    return HttpResponse(json.dumps(list(df_dict.values())))
