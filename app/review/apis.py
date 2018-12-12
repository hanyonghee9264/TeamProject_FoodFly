from rest_framework.response import Response
from rest_framework.views import APIView

from review.models import Review
from review.serializers import ReviewSerializer


class ReviewList(APIView):
    def get(self, request):
        review = Review.objects.all()
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data)

