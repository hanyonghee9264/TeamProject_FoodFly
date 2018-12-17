from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Avg

from members.models import User
from store.models.store import Store


class Review(models.Model):
    content = models.TextField(verbose_name='리뷰내용', blank=True)
    rating = models.PositiveIntegerField(
        verbose_name='별점',
        default=0,
        validators=[MaxValueValidator(5)]
    )
    user = models.ForeignKey(
        User,
        verbose_name='사용자',
        on_delete=models.CASCADE,
    )
    store = models.ForeignKey(
        Store,
        verbose_name='상점',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(verbose_name='등록일', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='수정일', auto_now=True)

    class Meta:
        verbose_name = '리뷰'
        verbose_name_plural = f'{verbose_name} 목록'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        star_rating = Review.objects.filter(store_id=self.store.pk).aggregate(Avg('rating'))
        store_average = Store.objects.get(pk=self.store.pk)
        store_average.rating_average = star_rating['rating__avg']
        store_average.save()


class ReviewImage(models.Model):
    location = models.ImageField(verbose_name='리뷰사진', upload_to='review', blank=True, null=True)
    review = models.ForeignKey(
        Review,
        verbose_name='리뷰',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(verbose_name='등록일', auto_now_add=True)

    class Meta:
        verbose_name = '리뷰이미지'
        verbose_name_plural = f'{verbose_name} 목록'


class Comment(models.Model):
    content = models.TextField(verbose_name='사장님댓글', blank=True)
    user = models.ForeignKey(
        User,
        verbose_name='사장님',
        on_delete=models.CASCADE,
    )
    review = models.ForeignKey(
        Review,
        verbose_name='리뷰',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(verbose_name='등록일', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='수정일', auto_now=True)

    class Meta:
        verbose_name = '사장님댓글'
        verbose_name_plural = f'{verbose_name} 목록'
