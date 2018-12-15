from django.contrib.auth import get_user_model
from django.db import models

from store.models.store import Store

User = get_user_model()


class Address(models.Model):
    old_address = models.CharField(verbose_name='지번주소', max_length=100)
    address = models.CharField(verbose_name='도로명 주소', max_length=100)
    detail_address = models.CharField(verbose_name='상세주소', max_length=100, blank=True)
    # 위도, 경도 (정수 부분 4자리, 소수점 이하 자리수 6자리)
    # lat(latitude): 위도 lng(longitude): 경도
    lat = models.DecimalField(verbose_name='위도', max_digits=12, decimal_places=9)
    lng = models.DecimalField(verbose_name='경도', max_digits=12, decimal_places=9)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='사용자',
        related_name='is_host_address_set',
        related_query_name='is_host_address',
        blank=True,
        null=True,
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.SET_NULL,
        verbose_name='상점',
        related_name='is_store_address_set',
        related_query_name='is_store_address',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(verbose_name='등록일', auto_now=True)

    class Meta:
        verbose_name = '주소'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return '{present} {detail}'.format(
            present=self.address,
            detail=self.detail_address,
        )
