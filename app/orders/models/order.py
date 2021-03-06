from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    shipping = models.CharField(verbose_name='배송지', max_length=50)
    created_at = models.DateTimeField(verbose_name='주문일자', auto_now=True)
    payment_status = models.BooleanField(verbose_name='결제상태', default=False)
    payment_option = models.CharField(verbose_name='결제수단', max_length=50, blank=True)
    comment = models.TextField(verbose_name='요청사항', blank=True)
    phone = models.CharField(verbose_name='전화번호', max_length=13, blank=True)

    class Meta:
        verbose_name = '주문'
        verbose_name_plural = f'{verbose_name} 목록'

    @property
    def payment(self):
        payment = 0
        for item in self.cartitem_set.all():
            if item.is_ordered:
                payment += item.total_price
        return payment
