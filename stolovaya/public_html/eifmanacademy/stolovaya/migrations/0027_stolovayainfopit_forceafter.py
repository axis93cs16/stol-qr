# Generated by Django 3.2.16 on 2022-12-21 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stolovaya', '0026_auto_20221221_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='stolovayainfopit',
            name='forceafter',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='force_checked_after'),
        ),
    ]
