from django.urls import path

from review.apis import ReviewList

urlpatterns = [
    path('list/', ReviewList.as_view()),
]
