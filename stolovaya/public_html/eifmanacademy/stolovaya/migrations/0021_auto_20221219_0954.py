# Generated by Django 3.2.16 on 2022-12-19 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stolovaya', '0020_stolovayacategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stolovayacategory',
            name='dateeda',
            field=models.DateField(verbose_name='Date_pitania'),
        ),
        migrations.AlterField(
            model_name='stolovayatalon',
            name='dateeda',
            field=models.DateField(verbose_name='Date_pitania'),
        ),
    ]
