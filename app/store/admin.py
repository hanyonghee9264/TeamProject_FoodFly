from django.contrib import admin

# Register your models here.
from .models import Store, Food

admin.site.register(Store)
admin.site.register(Food)
