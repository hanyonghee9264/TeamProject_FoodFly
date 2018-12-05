from django.urls import path

from ..apis import OrderList

urlpatterns = [
    path('', OrderList.as_view()),
]
