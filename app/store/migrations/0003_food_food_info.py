# Generated by Django 2.1.3 on 2018-11-30 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_food'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='food_info',
            field=models.TextField(blank=True, verbose_name='음식정보'),
        ),
    ]
