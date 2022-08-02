from unicodedata import name
from django.urls import path

from .views import user, test

app_name = 'MM'
urlpatterns = [
    path('', test.test, name='test'),
    path('login/', user.login, name='login'),
    path('register/', user.register, name='register'),
    path('home/', user.home, name='home'),
    path('logout/', user.logout, name='logout')
]