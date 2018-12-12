from rest_framework import serializers

from address.models import Address
from address.serializers import AddressInfoSerializer
from members.serializers import UserSerializer
from .models.food import Food, FoodCategory, FoodImage, SideDishes
from .models.store import Store, StoreCategory, StoreImage


class SideDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = SideDishes
        fields = (
            'pk',
            'name',
            'price',
            'is_required',
        )


class FoodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodImage
        fields = (
            'location',
            'created_at',
        )


# 음식 데이터를 위한 Serializer
class FoodSerializer(serializers.ModelSerializer):
    foodimage_set = FoodImageSerializer(many=True)
    sidedishes_set = SideDishSerializer(many=True)

    def get_foodimage_set(self, obj):
        images = FoodImage.objects.select_related('food').filter(food=obj)
        return FoodImageSerializer(images, many=True)

    class Meta:
        model = Food
        fields = (
            'pk',
            'name',
            'price',
            'stock',
            'has_side_dishes',
            'food_info',
            'foodimage_set',
            'sidedishes_set',
        )


# 식당에 있는 메뉴 Serializer
class FoodCategorySerializer(serializers.ModelSerializer):
    food_set = FoodSerializer(many=True)

    class Meta:
        model = FoodCategory
        fields = (
            'name',
            'store',
            'food_set',
        )


# 식당의 범주 Serializer
class StoreCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreCategory
        fields = (
            'name',
        )


class StoreImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreImage
        fields = (
            'location',
            'created_at',
        )


# 식당 데이터를 위한 Serializer
class StoreSerializer(serializers.ModelSerializer):
    # owner = UserSerializer()
    category = StoreCategorySerializer()
    storeimage_set = StoreImageSerializer(many=True)
    address = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = (
            'pk',
            'name',
            'store_info',
            'origin_info',
            'owner',
            'least_cost',
            'takeout',
            'fee',
            'storeimage_set',
            'category',
            'address',
        )
        read_only_fields = ('owner', 'category',)

    def get_address(self, obj):
        if not Address.objects.filter(store=obj).exists():
            return
        else:
            return AddressInfoSerializer(Address.objects.get(store=obj)).data


# 식당에 있는 음식과 음식 메뉴를 위한 Serializer
class StoreDetailSerializer(StoreSerializer):
    menu = serializers.SerializerMethodField(read_only=True)

    # 식당에 있는 메뉴의 음식들을 꺼내오기 위한 함수
    def get_menu(self, obj):
        category = FoodCategory.objects.filter(store=obj).prefetch_related('food_set')
        return FoodCategorySerializer(category, many=True).data

    class Meta(StoreSerializer.Meta):
        fields = StoreSerializer.Meta.fields + (
            'menu',
        )
