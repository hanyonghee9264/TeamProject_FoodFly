from django.urls import path, include

from .apis import StoreList, StoreDetail

urlpatterns = [
    path('', StoreList.as_view(),),
    path('<int:category_pk>/', StoreList.as_view(),),
    path('<int:category_pk>/store/<int:store_pk>/', StoreDetail.as_view(),),
]
