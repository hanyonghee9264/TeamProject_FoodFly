from django.urls import path

from members.apis import AuthToken, UserRegister, Profile

urlpatterns = [
    path('login/', AuthToken.as_view()),
    path('register/', UserRegister().as_view()),
    path('profile/', Profile.as_view()),
]
