from rest_framework import serializers

from members.serializers import UserSerializer
from review.models import Review, ReviewImage, Comment
from store.serializers import StoreSerializer


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = (
            'location',
            'created_at',
        )


class ReviewSerializer(serializers.ModelSerializer):
    reviewimage_set = ReviewImageSerializer(many=True, required=False)
    store_set = StoreSerializer(required=False)

    class Meta:
        model = Review
        fields = (
            'pk',
            'content',
            'rating',
            'store_set',
            'reviewimage_set',
        )
        read_only_fields = (
            'store',
            'reviewimage_set',
        )


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            'pk',
            'content',
            'user',
            'review',
        )
