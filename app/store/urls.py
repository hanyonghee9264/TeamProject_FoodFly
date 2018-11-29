from django.urls import path

from .apis import StoreList, StoreDetail

urlpatterns = [
    path('list/', StoreList.as_view(),),
    path('<int:pk>/', StoreDetail.as_view(),),
]
