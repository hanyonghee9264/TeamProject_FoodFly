from django.db import transaction
from rest_framework import serializers

from members.serializers import UserSerializer
from store.models.food import Food, SideDishes
from store.models.store import Store
from store.serializers import FoodSerializer, SideDishSerializer
from .models.cart import Cart, CartItem
from .models.order import Order


class CartItemSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = (
            'pk',
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
    store = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'pk',
            'user',
            'phone',
            'shipping',
            'comment',
            'payment_option',
            'payment_status',
            'store',
            'payment',
            'created_at',
        )
        read_only_fields = ('user',)

    @classmethod
    def setup_eager_loading(cls, qs):
        queryset = qs.select_related('user').prefetch_related('cartitem_set')
        return queryset

    def get_store(self, obj):
        data =[]
        for i in obj.cartitem_set.select_related('cart', 'food', 'order').prefetch_related('options'):
            store = Store.objects.get(foodcategory__food__pk=i.food.pk)
            total_price = i.total_price
            info = {'store': store.name, 'total_price': total_price}
            data.append(info)
        return data

    @transaction.atomic
    def create(self, validate_data):
        user = self.context['request'].user
        order = Order.objects.create(
            **validate_data,
            user=user,
        )
        cart = Cart.objects.get(user=user)
        for item in cart.item.filter(is_ordered=False).select_related('cart', 'food', 'order').prefetch_related('options'):
            item.order = order
            item.is_ordered = True
            item.save()

        return order


class OptionSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.name


class CartItemInfoSerializer(serializers.ModelSerializer):
    store = serializers.SerializerMethodField()
    food = serializers.SerializerMethodField()
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = CartItem
        fields = (
            'pk',
            'store',
            'food',
            'is_ordered',
            'options',
            'quantity',
            'total_price',
        )

    def get_store(self, obj):
        return Store.objects.get(foodcategory__food__pk=obj.food.pk).name

    def get_food(self, obj):
        return Food.objects.get(pk=obj.food.pk).name

    def to_representation(self, instance):
        if not instance.is_ordered:
            return super().to_representation(instance)


class CartSerializer(serializers.ModelSerializer):
    item = CartItemInfoSerializer(many=True, read_only=True)
    # item = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            'user',
            'item',
            'payment',
        )

    # def get_item(self, obj):
    #     data = []
    #     for i in obj.item.filter(is_ordered=False):
    #         store = Store.objects.get(foodcategory__food__pk=i.food.pk)
    #         food = Food.objects.get(pk=i.food.pk)
    #         quantity = i.quantity
    #         total_price = i.total_price
    #         info = {
    #             'pk': i.pk,
    #             'store': store.name,
    #             'food': food.name,
    #             'quantity': quantity,
    #             'total_price': total_price
    #         }
    #         data.append(info)
    #     return data
