# Generated by Django 3.2.16 on 2022-12-29 13:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stolovaya', '0031_auto_20221228_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stolovaya',
            name='pitendateen',
            field=models.DateField(default=datetime.datetime(2030, 1, 1, 1, 1, 1, 1), verbose_name='Pitanie_po_menu_s'),
        ),
    ]
