# Generated by Django 3.2.16 on 2022-12-06 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stolovaya', '0003_stolovayainfopit'),
    ]

    operations = [
        migrations.AddField(
            model_name='stolovaya',
            name='medflag',
            field=models.BooleanField(default=False, verbose_name='checked'),
        ),
        migrations.AlterField(
            model_name='stolovaya',
            name='internat',
            field=models.CharField(choices=[('normal', 'normal'), ('2-level', '2-level'), ('3-level', '3-level'), ('4-level', '3-level')], default='normal', max_length=255, verbose_name='internat'),
        ),
    ]
