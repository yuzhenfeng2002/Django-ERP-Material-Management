from django.urls import path

from .views import user, test, vendor, material, receipt, invoice
from .views.ajax import material_api, data_api, stock_api, vendor_api, user_api, receipt_api, invoice_api

app_name = 'MM'
urlpatterns = [
    path('', test.test, name='test'),
    path('login/', user.login, name='login'),
    path('register/', user.register, name='register'),
    path('home/', user.home, name='home'),
    path('logout/', user.logout, name='logout'),

    path('vendor/create/', vendor.create, name='create_vendor'),
    path('vendor/search/', vendor.search, name='search_vendor'),

    path('material/search/', material.search_material, name='search_material'),
    path('material/item/create/', material.create_item, name='create_item'),
    path('material/item/stock/', material.search_item_stock, name='search_item_stock'),

    path('receipt/create/', receipt.create_receipt, name='create_receipt'),
    path('receipt/display/', receipt.display_receipt, name='display_receipt'),
    path('receipt/search/', receipt.search_receipt, name='search_receipt'),
    path('receipt/create2/', receipt.load_order_item, name='load_order_item_receipt'),

    path('invoice/create/', invoice.create_invoice, name='create_invoice'),
    path('invoice/create2/', invoice.load_order_item, name='load_order_item_invoice'),
    path('invoice/search/', invoice.search_invoice, name='search_invoice'),
    path('invoice/display/', invoice.display_invoice, name='display_invoice'),

    # ajax
    ## user
    path('api/user/loadAll/', user_api.load_user, name='ajax_load_user'),
    ## vendor
    path('api/vendor/update/', vendor_api.update_vendor, name='ajax_update_vendor'),
    path('api/vendor/search/', vendor_api.search_vendor, name='ajax_search_vendor'),
    path('api/vendor/create/', vendor_api.create_vendor, name='ajax_create_vendor'),
    path('api/vendor/score/', vendor_api.search_vendor_history, name='ajax_search_vendor_history'),
    ## material
    path('api/material/item/search/', material_api.search_item, name='ajax_search_item'),
    path('api/material/item/update/', material_api.update_item, name='ajax_update_item'),
    path('api/material/item/create/', material_api.create_item, name='ajax_create_item'),
    path('api/material/item/stockHistory/', material_api.update_item, name='ajax_update_item'),
    path('api/material/stock/search/', material_api.search_stock_history, name='ajax_search_stock_history'),
    path('api/material/stock/getByName/', stock_api.getByName, name='ajax_getStockByName'),

    path('api/receipt/create/', receipt_api.create_receipt, name='ajax_create_receipt'),
    path('api/receipt/search/', receipt_api.search_receipt, name='ajax_search_receipt'),
    path('api/invoice/search/', invoice_api.search_invoice, name='ajax_search_invoice'),


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