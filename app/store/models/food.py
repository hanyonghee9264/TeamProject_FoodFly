from django.db import models
from .store import Store


class FoodCategory(models.Model):
    name = models.CharField(verbose_name='음식분류', max_length=50)
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        verbose_name='상점',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '메뉴'
        verbose_name_plural = f'{verbose_name} 목록'


class Food(models.Model):
    category = models.ForeignKey(
        FoodCategory,
        on_delete=models.CASCADE,
        verbose_name='메뉴'
    )
    name = models.CharField(verbose_name='음식이름', max_length=50)
    price = models.PositiveIntegerField(verbose_name='가격', default=0)
    stock = models.PositiveIntegerField(verbose_name='수량', default=0)
    created_at = models.DateTimeField(verbose_name='등록일', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='수정일', auto_now=True)
    has_side_dishes = models.BooleanField(verbose_name='사이드메뉴', default=False)
    food_info = models.TextField(verbose_name='음식정보', blank=True)

    def __str__(self):
        return '{name}::{price}원'.format(
            name=self.name,
            price=self.price,
        )

    class Meta:
        verbose_name = '음식'
        verbose_name_plural = f'{verbose_name} 목록'


class FoodImage(models.Model):
    location = models.ImageField(verbose_name='음식사진', upload_to='food', blank=True)
    food = models.ForeignKey(
        Food,
        verbose_name='음식',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(verbose_name='등록일', auto_now_add=True)

    class Meta:
        verbose_name = '음식사진'
        verbose_name_plural = f'{verbose_name} 목록'


class SideDishes(models.Model):
    name = models.CharField(verbose_name='사이드메뉴이름', max_length=50)
    price = models.PositiveIntegerField(verbose_name='가격', default=0)
    is_required = models.BooleanField(verbose_name='필수선택', default=False)
    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        verbose_name='음식'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '사이드메뉴'
        verbose_name_plural = f'{verbose_name} 목록'
