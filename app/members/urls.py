from django.urls import path

from members.apis import AuthToken, UserRegister

urlpatterns = [
    path('auth/', AuthToken.as_view()),
    path('register/', UserRegister().as_view()),
]
