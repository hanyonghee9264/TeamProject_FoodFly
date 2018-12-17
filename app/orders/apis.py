from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status, generics

from store.models.food import Food, SideDishes
from .models.order import Order

from .models.cart import Cart, CartItem
from .serializers import CartItemSerializer, OrderSerializer, CartSerializer

User = get_user_model()


class CartItemList(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        cart = Cart.objects.get_or_create(user=request.user)[0]
        food = Food.objects.get(pk=request.data.pop('food_pk'))

        # 음식에 추가(사이드)메뉴가 존재하는 경우
        if food.has_side_dishes:
            side_index_list = request.data.pop('side_dishes_pk')
            side_dishes = []
            for index in side_index_list:
                side_dishes.append(SideDishes.objects.get(pk=index))

            serializer = CartItemSerializer(
                data={
                    **request.data,
                    'cart': cart,
                },
                context={
                    'food': food,
                    'side_dishes': side_dishes,
                },
            )
        # 추가 메뉴가 없는 경우
        else:
            serializer = CartItemSerializer(
                data={
                    **request.data,
                    'cart': cart,
                },
                context={
                    'food': food,
                }
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        cart = Cart.objects.get(user=request.user)
        food = Food.objects.get(pk=request.data.get('food_pk'))
        item = CartItem.objects.get(
            cart=cart,
            food=food,
        )

        serializer = CartItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        food = get_object_or_404(Food, pk=request.data.get('food_pk'))
        cart.item.filter(food=food).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = Order.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(qs)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = OrderSerializer
