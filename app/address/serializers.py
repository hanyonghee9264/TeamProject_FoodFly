from rest_framework import serializers

from address.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'pk',
            'old_address',
            'address',
            'detail_address',
            'lat',
            'lng',
            'user',
            'store',
            'created_at',
        )
        read_only_fields = ('user', 'store')

    def create(self, validate_data):
        address = Address.objects.create(
            **validate_data,
            user=self.context['request'].user,
        )
        return address


class AddressInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'pk',
            'old_address',
            'address',
            'detail_address',
            'lat',
            'lng'
        )
