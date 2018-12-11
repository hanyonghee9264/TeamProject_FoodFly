from rest_framework import serializers

from address.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
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
