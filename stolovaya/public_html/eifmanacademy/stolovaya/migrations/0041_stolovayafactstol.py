# Generated by Django 3.2.16 on 2023-01-31 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stolovaya', '0040_auto_20230127_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='stolovayafactstol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(verbose_name='DateTime_otmetka')),
                ('dateeda', models.DateField(verbose_name='Date_pitania')),
                ('typeofedapit', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='type_of_eda_pit')),
                ('uchid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stolovaya.stolovaya', verbose_name='id_uchenika')),
            ],
        ),
    ]
