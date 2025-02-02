# Generated by Django 3.2.16 on 2023-12-19 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stolovaya', '0042_stolovayacategory_xvarx'),
    ]

    operations = [
        migrations.CreateModel(
            name='stolovayablkdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime1', models.DateTimeField(verbose_name='DateTime_otmetka')),
                ('dateeda', models.DateField(verbose_name='Date_pitania')),
                ('blockflag', models.BooleanField(default=False, verbose_name='blocked')),
                ('uchid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stolovaya.stolovaya', verbose_name='id_uchenika')),
            ],
        ),
    ]
