from rest_framework import permissions, status, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from review.models import Review
from review.serializers import ReviewSerializer, ReviewCreateSerializer, ReviewImageSerializer, \
    ReviewImageCreateSerializer
from store.models.store import Store
from store.serializers import StoreImageSerializer


class ReviewList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request):
        review = Review.objects.all()
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # store = Store.objects.get(pk=request.data.pop('store'))
        store = Store.objects.get(pk=request.data['store'])
        serializer = ReviewSerializer(
            data=request.data,
            context={
                'request': request,
                'store': store,
            }
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, partial=True):
        review_pk = request.data.get('pk')

        if not review_pk:
            raise serializers.ValidationError({'detail': 'pk값이 주어지지 않았습니다.'})
        review = Review.objects.get(pk=review_pk)
        if review.user != request.user:
            raise serializers.ValidationError({'detail': '해당 유저가 아닙니다.'})

        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        review = get_object_or_404(Review, user=request.user, pk=request.data.get('review_pk'))

        if review.user != request.user:
            raise serializers.ValidationError({'detail': '해당 유저가 아닙니다.'})

        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewImageCreate(APIView):
    def post(self, request, format=None):
        serializer = ReviewImageCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
