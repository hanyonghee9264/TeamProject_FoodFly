from django.urls import path

from review.apis import ReviewList, ReviewImageCreate

urlpatterns = [
    path('', ReviewList.as_view()),
    path('image/', ReviewImageCreate.as_view())
]
