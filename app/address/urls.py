from django.urls import path

from .apis import UserAddressAPIView

urlpatterns = [
    path('', UserAddressAPIView.as_view()),
]
