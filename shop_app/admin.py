from django.contrib import admin
from .models import Product, BuyItem, BuyItemReturn, MyUser

admin.site.register(Product)
admin.site.register(BuyItem)
admin.site.register(BuyItemReturn)
admin.site.register(MyUser)
# Register your models here.
