# Generated by Django 3.2.16 on 2024-09-10 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stolovaya', '0045_auto_20240228_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='stolovayainfopit',
            name='forceflagip',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='force_checked_ip'),
        ),
        migrations.AddField(
            model_name='stolovayainfopit',
            name='internatp',
            field=models.BooleanField(blank=True, null=True, verbose_name='internatp'),
        ),
        migrations.AddField(
            model_name='stolovayainfopitafter',
            name='internatp',
            field=models.BooleanField(blank=True, null=True, verbose_name='internatp_checked'),
        ),
        migrations.AlterField(
            model_name='stolovayacategory',
            name='category',
            field=models.CharField(choices=[('normal', 'Обычные'), ('lgota14', 'Льготники младшие'), ('lgota59', 'Льготники старшие'), ('internat14', 'Интернат младшие'), ('internat59', 'Интернат старшие'), ('dogovor1', 'Договор Тип1(нет супа)'), ('dogovor2', 'Договор Тип2(суп)'), ('dogovor3', 'Договор Тип3(суп)'), ('internatp', 'internatp')], default='normal', max_length=255, verbose_name='typeofeda'),
        ),
        migrations.AlterField(
            model_name='stolovayatalon',
            name='catoftalon',
            field=models.CharField(choices=[('obed1', 'obed2'), ('obed2', 'obed2'), ('obed3', 'obed3'), ('internatp', 'internatp')], default='obed1', max_length=255, verbose_name='catoftalon'),
        ),
    ]
