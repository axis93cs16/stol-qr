# Generated by Django 3.2.16 on 2022-12-13 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stolovaya', '0008_auto_20221213_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='stolovayainfopit',
            name='forceflag',
            field=models.BooleanField(default=False, verbose_name='force_checked'),
        ),
    ]