from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class StoreCategory(models.Model):
    name = models.CharField(verbose_name='카테고리', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = f'{verbose_name} 목록'


class Store(models.Model):
    category = models.ForeignKey(
        StoreCategory,
        on_delete=models.SET_NULL,
        verbose_name='카테고리',
        null=True
    )
    name = models.CharField(verbose_name='상점이름', max_length=50)
    store_info = models.TextField(verbose_name='상점소개', blank=True)
    origin_info = models.TextField(verbose_name='원산지 정보', blank=True)
    created_at = models.DateTimeField(verbose_name='등록일', auto_now_add=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='상점주',
    )
    least_cost = models.PositiveIntegerField(verbose_name='최소주문금액', default=0)
    takeout = models.BooleanField(verbose_name='테이크아웃', default=False)
    fee = models.PositiveIntegerField(verbose_name='배달팁', default=0)
    rating_average = models.DecimalField(verbose_name='별점평균', blank=True, null=True, max_digits=5, decimal_places=1)

    def __str__(self):
        return '{category}::{name}'.format(
            category=self.category,
            name=self.name,
        )

    class Meta:
        verbose_name = '상점'
        verbose_name_plural = f'{verbose_name} 목록'


class StoreImage(models.Model):
    location = models.ImageField(verbose_name='상점사진', upload_to='store', blank=True)
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        verbose_name='상점',
    )
    created_at = models.DateTimeField(verbose_name='등록일', auto_now_add=True)

    class Meta:
        verbose_name = '상점이미지'
        verbose_name_plural = f'{verbose_name} 목록'
