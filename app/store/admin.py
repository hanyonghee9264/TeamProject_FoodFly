from django.contrib import admin

# Register your models here.
from .models.food import Food
from .models.store import Store

admin.site.register(Store)
admin.site.register(Food)
