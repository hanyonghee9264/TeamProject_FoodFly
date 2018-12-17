from django.urls import path

from ..apis import OrderList, OrderDetail

urlpatterns = [
    path('', OrderList.as_view()),
    path('<int:pk>/', OrderDetail.as_view()),
]
