from django.contrib import admin
from .models import Contact

admin.site.register(Contact)
from .models import Product

admin.site.register(Product)


from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'qty', 'price', 'order')