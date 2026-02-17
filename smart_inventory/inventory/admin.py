from django.contrib import admin
from .models import Supplier, Product, StockTransaction


admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(StockTransaction)
