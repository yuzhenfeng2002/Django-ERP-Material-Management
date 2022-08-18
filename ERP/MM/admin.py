from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(EUser)
admin.site.register(Vendor)
admin.site.register(Stock)
admin.site.register(Material)
admin.site.register(MaterialItem)
admin.site.register(StockHistory)
admin.site.register(GoodReceipt)