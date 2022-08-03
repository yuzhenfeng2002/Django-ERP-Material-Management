from unicodedata import name
from django.urls import path

from .views import user, test, vendor

app_name = 'MM'
urlpatterns = [
    path('', test.test, name='test'),
    path('login/', user.login, name='login'),
    path('register/', user.register, name='register'),
    path('home/', user.home, name='home'),
    path('logout/', user.logout, name='logout'),
    path('vendor/create/', vendor.create, name='create_vendor'),
    path('vendor/display/<int:pk>/', vendor.display, name='display_vendor'),
    path('vendor/update/', vendor.update, name='update_vendor'),
    path('vendor/search/', vendor.search, name='search_vendor'),
]