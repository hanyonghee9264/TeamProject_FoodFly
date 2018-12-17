from django.db import transaction
from rest_framework import serializers

from members.serializers import UserSerializer
from store.serializers import FoodSerializer, SideDishSerializer
from .models.cart import Cart, CartItem
from .models.order import Order


class CartItemSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = (
            'cart',
            'food',
            'quantity',
            'is_ordered',
            'options',
            'total_price',
        )
        read_only_fields = ('options',)

    @transaction.atomic
    def create(self, validate_data):
        cart = validate_data['cart']
        food = self.context['food']

        if CartItem.objects.filter(cart=cart, food=food, is_ordered=False).exists():
            raise serializers.ValidationError('이미 존재하는 아이템입니다.')

        item = CartItem.objects.create(
            cart=cart,
            food=food,
            quantity=validate_data['quantity'],
        )
        if food.has_side_dishes:
            side_dishes = self.context['side_dishes']
            for side_dish in side_dishes:
                item.options.add(side_dish)
                item.save()
        return item

    def get_total_price(self, obj):
        return obj.total_price


class OrderSerializer(serializers.ModelSerializer):
    cartitem_set = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'pk',
            'user',
            'shipping',
            'created_at',
            'payment_status',
            'cartitem_set',
            'payment',
        )
        read_only_fields = ('user',)

    @classmethod
    def setup_eager_loading(cls, qs):
        queryset = qs.select_related('user').prefetch_related('cartitem_set')
        return queryset

    @transaction.atomic
    def create(self, validate_data):

        user = self.context['request'].user
        shipping = validate_data['shipping']
        order = Order.objects.create(
            user=user,
            shipping=shipping,
        )
        cart = Cart.objects.get(user=user)
        for item in cart.item.filter(is_ordered=False).select_related('cart', 'food', 'order').prefetch_related('options'):
            item.order = order
            item.is_ordered = True
            item.save()

        return order


class CartSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            'user',
            'item',
            'payment',
        )

    def get_item(self, obj):
        item = obj.item.filter(is_ordered=False)
        return CartItemSerializer(item, many=True).data
