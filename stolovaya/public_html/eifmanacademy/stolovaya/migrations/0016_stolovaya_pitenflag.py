# Generated by Django 3.2.16 on 2022-12-15 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stolovaya', '0015_auto_20221215_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='stolovaya',
            name='pitenflag',
            field=models.BooleanField(default=True, verbose_name='Pitanie_po_menu'),
        ),
    ]
