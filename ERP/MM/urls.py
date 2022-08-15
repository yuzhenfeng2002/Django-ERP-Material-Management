from django.urls import path

from .views import user, test, vendor, material
from .views.ajax import material_api, data_api, stock_api

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
    path('material/item/search/', material.search_item, name='search_item'),
    path('material/item/stock/', material.search_item_stock, name='search_item_stock'),
    path('api/material/search/', material_api.search_material, name='ajax_search_material'),
    path('api/material/item/search/', material_api.search_item, name='ajax_search_item'),
    path('api/material/item/update/', material_api.update_item, name='ajax_update_item'),
    path('api/material/item/stockHistory/', material_api.update_item, name='ajax_update_item'),
    path('api/material/stock/search/', material_api.search_stock_history, name='ajax_search_stock_history'),
    path('api/material/stock/getByName/', stock_api.getByName, name='ajax_getStockByName'),
    # pre-determined data
    path('api/data/country/', data_api.load_country, name='ajax_load_country'),
    path('api/data/company/', data_api.load_company, name='ajax_load_company'),
    path('api/data/currency/', data_api.load_currency, name='ajax_load_currency'),
    path('api/data/language/', data_api.load_language, name='ajax_load_language'),
    path('api/data/meaunit/', data_api.load_meaunit, name='ajax_load_meaunit'),
    path('api/data/pgrp/', data_api.load_pgrp, name='ajax_load_pgrp'),
    path('api/data/plant/', data_api.load_plant, name='ajax_load_plant'),
    path('api/data/porg/', data_api.load_porg, name='ajax_load_porg'),
    path('api/data/sorg/', data_api.load_sorg, name='ajax_load_sorg'),
    path('api/data/tptype/', data_api.load_tptype, name='ajax_load_tptype'),
]