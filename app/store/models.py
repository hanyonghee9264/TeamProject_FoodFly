from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Store(models.Model):
    STORE_CATEGORY = (
        ('0', '한식'),
        ('1', '일식'),
        ('2', '양식'),
        ('3', '중식'),
        ('4', '카페'),
    )
    store_category = models.CharField(
        verbose_name='상점분류',
        choices=STORE_CATEGORY,
        max_length=1,
    )
    name = models.CharField(verbose_name='상점이름', max_length=50)
    img_profile = models.ImageField(verbose_name='상점이미지', upload_to='store', blank=True)
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

    def __str__(self):
        return '{category}::{name}'.format(
            category=self.store_category,
            name=self.name,
        )

    class Meta:
        verbose_name = '상점'
        verbose_name_plural = f'{verbose_name} 목록'

#
# class Food(models.Model):
#     name = models.CharField(verbose_name='음식이름', max_length=50)
#     img_profile = models.ImageField(verbose_name='음식이미지', upload_to='food', blank=True)
#     price = models.PositiveIntegerField(verbose_name='가격', default=0)
#     stock = models.PositiveIntegerField(verbose_name='수량', default=0)
#     created_at = models.DateTimeField(verbose_name='등록일', auto_now_add=True)
#     store = models.ForeignKey(
#         Store,
#         verbose_name='음식점',
#         on_delete=models.CASCADE,
#     )
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = '음식'
#         verbose_name_plural = f'{verbose_name} 목록'
