from django.contrib import admin

# Register your models here.
from .models.order import Order
from .models.cart import Cart, CartItem

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
