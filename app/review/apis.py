from rest_framework import permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from review.models import Review
from review.serializers import ReviewSerializer, ReviewCreateSerializer
from store.models.store import Store


class ReviewList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request):
        review = Review.objects.all()
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data)

    def post(self, request):
        store = Store.objects.get(pk=request.data.pop('store'))
        serializer = ReviewSerializer(
            data=request.data,
            context={
                'request': request,
                'store': store,
            }
        )
        # serializer = ReviewCreateSerializer(
        #     data=request.data,
        #     context={
        #         'request': request,
        #     }
        # )
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
        review_pk = request.data.get('pk')

        if not review_pk:
            raise serializers.ValidationError({'detail': 'pk값이 주어지지 않았습니다.'})
        review = Review.objects.get(pk=review_pk)

        if review.user != request.user:
            raise serializers.ValidationError({'detail': '해당 유저가 아닙니다.'})

        review_pk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)