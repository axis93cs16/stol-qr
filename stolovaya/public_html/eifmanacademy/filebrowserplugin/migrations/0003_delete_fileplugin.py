# Generated by Django 3.2.16 on 2022-11-21 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('filebrowserplugin', '0002_fileplugin_showsize'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FilePlugin',
        ),
    ]
