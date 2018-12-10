from django.contrib.auth import get_user_model
from django.db import models
from store.models.food import Food, SideDishes
from .order import Order

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user.username}::cart'

    @property
    def payment(self):
        payment = 0
        for item in self.item.all():
            if not item.is_ordered:
                payment += item.total_price
        return payment


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        verbose_name='장바구니',
        on_delete=models.CASCADE,
        related_name='item',
        related_query_name='items',
    )
    food = models.ForeignKey(
        Food,
        verbose_name='음식',
        on_delete=models.CASCADE,
        related_name='in_cart',
        related_query_name='in_carts',
    )
    quantity = models.PositiveIntegerField(verbose_name='수량', default=0)
    is_ordered = models.BooleanField(
        verbose_name='주문상태',
        default=False
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='주문번호',
        blank=True,
        null=True,
    )
    options = models.ManyToManyField(
        SideDishes,
        related_name='option',
        related_query_name='options',
    )

    @property
    def total_price(self):
        price = self.food.price
        for item in self.options.all():
            price += item.price
        return self.quantity * price

    class Meta:
        verbose_name = '아이템'
        verbose_name_plural = f'{verbose_name} 목록'

