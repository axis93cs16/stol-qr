# Generated by Django 3.2.16 on 2022-12-05 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stolovaya', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stolovayainfodata',
            name='uchid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stolovaya.stolovaya', verbose_name='id_uchenika'),
        ),
    ]
