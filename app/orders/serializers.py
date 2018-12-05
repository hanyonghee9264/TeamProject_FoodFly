from rest_framework import serializers

from members.serializers import UserSerializer
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
        # food = Food.objects.get(pk=self.context['food_pk'])
        cart = validate_data['cart']
        food = self.context['food']
        if CartItem.objects.filter(cart=cart, food=food).exists():
            raise serializers.ValidationError('이미 존재하는 아이템입니다.')
        item = CartItem.objects.create(
            cart=cart,
            food=food,
            quantity=validate_data['quantity'],
        )
        return item


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            'pk',
            'user',
            'shipping',
            'created_at',
            'payment_status',
            'cartitem_set',
        )
        read_only_fields = ('cartitem_set',)

    def create(self, validate_data):
        user = self.context['request'].user
        shipping = validate_data['shipping']
        order = Order.objects.create(
            user=user,
            shipping=shipping,
        )
        cart = Cart.objects.get(user=user)
        for item in cart.item.filter(is_ordered=False):
            item.order = order
        return order
