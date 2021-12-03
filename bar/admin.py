from django.contrib import admin

# Register your models here.
from . import models


admin.site.register(models.Profile)
admin.site.register(models.MetricSystem)
admin.site.register(models.Metric)
admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.ProductCategories)
admin.site.register(models.Stock)
admin.site.register(models.SaleGuide)
admin.site.register(models.Order)
admin.site.register(models.OrderGroup)