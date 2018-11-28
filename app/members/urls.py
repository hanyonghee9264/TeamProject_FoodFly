from django.urls import path

from members.apis import AuthToken

urlpatterns = [
    path('auth/', AuthToken.as_view()),
]
