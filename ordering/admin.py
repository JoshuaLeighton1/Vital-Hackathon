from django.contrib import admin
from .models import Product, EmployeeProfile, Order

admin.site.register(Product)
admin.site.register(EmployeeProfile)
admin.site.register(Order)
