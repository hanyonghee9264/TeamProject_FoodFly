from django.contrib import admin

# Register your models here.
from .models.food import Food, FoodCategory, FoodImage
from .models.store import Store, StoreCategory, StoreImage

admin.site.register(Store)
admin.site.register(StoreCategory)
admin.site.register(StoreImage)
admin.site.register(Food)
admin.site.register(FoodCategory)
admin.site.register(FoodImage)
