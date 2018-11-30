from rest_framework import serializers

from .models import Store, Food


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = (
            'pk',
            'name',
            'img_profile',
            'price',
            'stock',
            'store',
            'set_menu',
            'food_info',
        )


class StoreSerializer(serializers.ModelSerializer):
    food_set = FoodSerializer(many=True)

    class Meta:
        model = Store
        fields = (
            'pk',
            'store_category',
            'name',
            'img_profile',
            'store_info',
            'origin_info',
            'created_at',
            'owner',
            'least_cost',
            'takeout',
            'fee',
            'food_set',
        )
