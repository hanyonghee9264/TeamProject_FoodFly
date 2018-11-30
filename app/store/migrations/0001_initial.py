# Generated by Django 2.1.3 on 2018-11-29 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_category', models.CharField(choices=[('0', '한식'), ('1', '일식'), ('2', '양식'), ('3', '중식'), ('4', '카페')], max_length=1, verbose_name='상점분류')),
                ('name', models.CharField(max_length=50, verbose_name='상점이름')),
                ('img_profile', models.ImageField(blank=True, upload_to='store', verbose_name='상점이미지')),
                ('store_info', models.TextField(blank=True, verbose_name='상점소개')),
                ('origin_info', models.TextField(blank=True, verbose_name='원산지 정보')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='등록일')),
                ('least_cost', models.PositiveIntegerField(default=0, verbose_name='최소주문금액')),
                ('takeout', models.BooleanField(default=False, verbose_name='테이크아웃')),
                ('fee', models.PositiveIntegerField(default=0, verbose_name='배달팁')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='상점주')),
            ],
            options={
                'verbose_name': '상점',
                'verbose_name_plural': '상점 목록',
            },
        ),
    ]
