from django.urls import path

from ..apis import CartItemList, CartItemDetail

urlpatterns = [
    path('items/', CartItemList.as_view()),
    path('items/<int:pk>/', CartItemDetail.as_view()),
]
