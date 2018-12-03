from django.urls import path

from .apis import CartItemList

urlpatterns = [
    path('items/', CartItemList.as_view()),
]
