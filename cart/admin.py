from django.contrib import admin

# Register your models here.
from .models import Order, Item, Cart, CartItem

admin.site.register(Order)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(CartItem)
