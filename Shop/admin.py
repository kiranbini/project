from django.contrib import admin
from . models import *
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    search_fields = ['product', 'description', 'category__category']
    list_display = ['product', 'category', 'stock', 'price']
    list_editable = ['stock', 'price']
admin.site.register(GreeneryProducts, ItemAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"link":['category',]}
admin.site.register(Categories, CategoryAdmin)



admin.site.register(Feedback)