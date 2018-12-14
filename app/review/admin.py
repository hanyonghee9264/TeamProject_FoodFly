from django.contrib import admin

from .models import Review, ReviewImage, Comment

admin.site.register(Review)
admin.site.register(ReviewImage)
admin.site.register(Comment)
