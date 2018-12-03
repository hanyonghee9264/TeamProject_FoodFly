from rest_framework import serializers

from store.models import Food
from store.serializers import FoodSerializer
from .models.cart import Cart, CartItem
from .models.order import Order


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = (
            'user',
        )


class CartItemSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = (
            'cart',
            'food',
            'quantity',
            'is_ordered',
        )

    def create(self, validate_data):
        food = Food.objects.get(pk=self.context['food_pk'])
        c = CartItem.objects.create(
            cart=validate_data['cart'],
            food=food,
            quantity=validate_data['quantity'],
        )
        return c


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'pk'
            'user',
            'shipping',
            'created_at',
            'payment_status',
            'cartitem_set',
        )
