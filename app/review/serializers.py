from rest_framework import serializers

from members.serializers import UserSerializer
from review.models import Review, ReviewImage, Comment


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Review
        fields = (
            'pk',
            'content',
            'rating',
            'user',
            'store',
        )


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = (
            'location',
            'created_at',
        )


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = (
            'pk',
            'content',
            'user',
            'review',
        )
