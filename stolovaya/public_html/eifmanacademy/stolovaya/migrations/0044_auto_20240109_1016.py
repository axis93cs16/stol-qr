# Generated by Django 3.2.16 on 2024-01-09 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stolovaya', '0043_stolovayablkdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='stolovayaclasspit',
            name='obedkg3',
            field=models.TimeField(blank=True, null=True, verbose_name='obedkg3'),
        ),
        migrations.AddField(
            model_name='stolovayainfopit',
            name='forceflagokg3',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='force_checked_okg3'),
        ),
        migrations.AddField(
            model_name='stolovayainfopit',
            name='obedkg3',
            field=models.BooleanField(blank=True, null=True, verbose_name='dogovor_3_checked'),
        ),
        migrations.AddField(
            model_name='stolovayainfopitafter',
            name='obedkg3',
            field=models.BooleanField(blank=True, null=True, verbose_name='obedkg3_checked'),
        ),
        migrations.AddField(
            model_name='stolovayapodacha',
            name='obedkg3',
            field=models.TimeField(blank=True, default='09:15:00', null=True, verbose_name='obedkg3'),
        ),
        migrations.AddField(
            model_name='stolovayapriemipishi',
            name='obedkg3',
            field=models.TimeField(blank=True, default='09:30:00', null=True, verbose_name='Договор Тип2(суп)'),
        ),
        migrations.AlterField(
            model_name='stolovayacategory',
            name='category',
            field=models.CharField(choices=[('normal', 'Обычные'), ('lgota14', 'Льготники младшие'), ('lgota59', 'Льготники старшие'), ('internat14', 'Интернат младшие'), ('internat59', 'Интернат старшие'), ('dogovor1', 'Договор Тип1(нет супа)'), ('dogovor2', 'Договор Тип2(суп)'), ('dogovor3', 'dogovor3')], default='normal', max_length=255, verbose_name='typeofeda'),
        ),
        migrations.AlterField(
            model_name='stolovayapodacha',
            name='obed',
            field=models.TimeField(default='09:15:00', verbose_name='Обед'),
        ),
        migrations.AlterField(
            model_name='stolovayapodacha',
            name='obedk',
            field=models.TimeField(blank=True, default='09:15:00', null=True, verbose_name='Комплексный Обед'),
        ),
        migrations.AlterField(
            model_name='stolovayapodacha',
            name='obedkg1',
            field=models.TimeField(blank=True, default='09:15:00', null=True, verbose_name='Договор Тип1(нет супа)'),
        ),
        migrations.AlterField(
            model_name='stolovayapodacha',
            name='obedkg2',
            field=models.TimeField(blank=True, default='09:15:00', null=True, verbose_name='Договор Тип2(суп)'),
        ),
        migrations.AlterField(
            model_name='stolovayapodacha',
            name='poldnik',
            field=models.TimeField(default='09:15:00', verbose_name='Полдник'),
        ),
        migrations.AlterField(
            model_name='stolovayapodacha',
            name='ujin1',
            field=models.TimeField(default='09:15:00', verbose_name='Ужин 1'),
        ),
        migrations.AlterField(
            model_name='stolovayapodacha',
            name='ujin2',
            field=models.TimeField(default='09:15:00', verbose_name='Ужин 2'),
        ),
        migrations.AlterField(
            model_name='stolovayapodacha',
            name='zavtrak',
            field=models.TimeField(default='07:30:00', verbose_name='Завтрак'),
        ),
        migrations.AlterField(
            model_name='stolovayapodacha',
            name='zavtrakg',
            field=models.TimeField(blank=True, default='07:30:00', null=True, verbose_name='Завтрак(Льгот)'),
        ),
        migrations.AlterField(
            model_name='stolovayapriemipishi',
            name='obed',
            field=models.TimeField(default='09:30:00', verbose_name='Обед'),
        ),
        migrations.AlterField(
            model_name='stolovayapriemipishi',
            name='obedkg1',
            field=models.TimeField(blank=True, default='09:30:00', null=True, verbose_name='Договор Тип1(нет супа)'),
        ),
        migrations.AlterField(
            model_name='stolovayapriemipishi',
            name='obedkg2',
            field=models.TimeField(blank=True, default='09:30:00', null=True, verbose_name='Договор Тип2(суп)'),
        ),
        migrations.AlterField(
            model_name='stolovayapriemipishi',
            name='poldnik',
            field=models.TimeField(default='09:30:00', verbose_name='Полдник'),
        ),
        migrations.AlterField(
            model_name='stolovayapriemipishi',
            name='ujin1',
            field=models.TimeField(default='09:30:00', verbose_name='Ужин 1'),
        ),
        migrations.AlterField(
            model_name='stolovayapriemipishi',
            name='ujin2',
            field=models.TimeField(default='09:30:00', verbose_name='Ужин 2'),
        ),
        migrations.AlterField(
            model_name='stolovayapriemipishi',
            name='zavtrak',
            field=models.TimeField(default='07:31:00', verbose_name='Завтрак'),
        ),
        migrations.AlterField(
            model_name='stolovayapriemipishi',
            name='zavtrakg',
            field=models.TimeField(blank=True, default='09:30:00', null=True, verbose_name='Завтрак(Льгот)'),
        ),
        migrations.AlterField(
            model_name='stolovayatalon',
            name='catoftalon',
            field=models.CharField(choices=[('obed1', 'obed2'), ('obed2', 'obed2'), ('obed3', 'obed3')], default='obed1', max_length=255, verbose_name='catoftalon'),
        ),
    ]