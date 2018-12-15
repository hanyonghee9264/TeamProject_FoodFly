from rest_framework import serializers
from rest_framework.compat import MaxValueValidator
from rest_framework.generics import get_object_or_404

from review.models import Review, ReviewImage, Comment
from store.models.store import Store

class ReviewImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = (
            'review',
            'location',
        )


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = (
            'location',
        )


class ReviewSerializer(serializers.ModelSerializer):
    store = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )
    reviewimage_set = ReviewImageSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = (
            'pk',
            'content',
            'rating',
            'user',
            'store',
            'reviewimage_set',
        )
        read_only_fields = (
            'user',
        )

    def create(self, validate_data):
        user = self.context['request'].user
        store = self.context['store']
        review = Review.objects.create(
            **validate_data,
            user=user,
            store=store,
        )
        return review


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            'pk',
            'content',
            'user',
            'review',
        )


class ReviewCreateSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=100)
    rating = serializers.IntegerField(default=0, validators=[MaxValueValidator(5)])
    store = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.review = None

    def create(self, validate_data):
        store = Store.objects.get(pk=validate_data['store'])
        review = Review.objects.create(
            content=validate_data['content'],
            rating=validate_data['rating'],
            store=store,
            user=self.context['request'].user
        )
        self.review = review
        return review

    def to_representation(self, instance):
        return ReviewSerializer(self.review).data
