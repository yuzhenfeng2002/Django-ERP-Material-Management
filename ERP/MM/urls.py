from django.urls import path

from .views import user, test, vendor, material
from .views.ajax import material_api

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
    path('material/create/', material.create_material, name='create_material'),
    path('material/display/<int:pk>/', material.display_material, name='display_material'),
    path('material/update/', material.update_material, name='update_material'),
    path('material/search/', material.search_material, name='search_material'),
    path('material/item/create/', material.create_item, name='create_item'),
    path('material/item/display/<int:pk>/', material.display_item, name='display_item'),
    path('material/item/update/', material.update_item, name='update_item'),
    path('api/material/search/', material_api.search_material, name='ajax_search_material'),
    path('api/material/stock/search/', material_api.search_stock, name='ajax_search_stock')
]