# Generated by Django 2.1.4 on 2018-12-20 08:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, verbose_name='사장님댓글')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='등록일')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
            ],
            options={
                'verbose_name': '사장님댓글',
                'verbose_name_plural': '사장님댓글 목록',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, verbose_name='리뷰내용')),
                ('rating', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5)], verbose_name='별점')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='등록일')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Store', verbose_name='상점')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'verbose_name': '리뷰',
                'verbose_name_plural': '리뷰 목록',
            },
        ),
        migrations.CreateModel(
            name='ReviewImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.ImageField(blank=True, null=True, upload_to='review', verbose_name='리뷰사진')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='등록일')),
                ('review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='review.Review', verbose_name='리뷰')),
            ],
            options={
                'verbose_name': '리뷰이미지',
                'verbose_name_plural': '리뷰이미지 목록',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='review.Review', verbose_name='리뷰'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사장님'),
        ),
    ]
