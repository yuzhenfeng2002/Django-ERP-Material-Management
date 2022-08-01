from django.urls import path

from .views import user, test

app_name = 'MM'
urlpatterns = [
    path('', test.test, name='test'),
    path('login/', user.login, name='login'),
]