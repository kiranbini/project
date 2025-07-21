from django.contrib import admin
from . models import Cart, CartItem, Orders, ProductOrders, Payment

# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'payment_type', 'payment_status', 'delivery_status']
    list_editable = ['delivery_status',]
admin.site.register(Orders, OrderAdmin)



admin.site.register(ProductOrders)
admin.site.register(Payment)
