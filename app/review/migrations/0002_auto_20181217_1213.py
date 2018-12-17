# Generated by Django 2.1.4 on 2018-12-17 03:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5)], verbose_name='별점'),
        ),
    ]