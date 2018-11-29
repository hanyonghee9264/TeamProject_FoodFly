from rest_framework import serializers

from .models import Store


class StoreSerializer(serializers.ModelSerializer):
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
        )
