# Generated by Django 3.2.16 on 2023-01-11 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stolovaya', '0036_auto_20230106_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='stolovayaclasspit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classname', models.CharField(max_length=255, verbose_name='Группа')),
                ('zavtrak', models.TimeField(verbose_name='Завтрак')),
                ('obed', models.TimeField(verbose_name='Обед')),
                ('poldnik', models.TimeField(verbose_name='Полдник')),
                ('ujin1', models.TimeField(verbose_name='Ужин 1')),
                ('ujin2', models.TimeField(verbose_name='Ужин 2')),
                ('obedk', models.TimeField(blank=True, null=True, verbose_name='Комплексный Обед')),
                ('obedkg1', models.TimeField(blank=True, null=True, verbose_name='Договор Тип1(нет супа)')),
                ('obedkg2', models.TimeField(blank=True, null=True, verbose_name='Договор Тип2(суп)')),
            ],
        ),
        migrations.AlterField(
            model_name='stolovayacategory',
            name='category',
            field=models.CharField(choices=[('normal', 'Обычные'), ('lgota14', 'Льготники младшие'), ('lgota59', 'Льготники старшие'), ('internat14', 'Интернат младшие'), ('internat59', 'Интернат старшие'), ('dogovor1', 'Договор Тип1(нет супа)'), ('dogovor2', 'Договор Тип2(суп)')], default='normal', max_length=255, verbose_name='typeofeda'),
        ),
        migrations.AlterField(
            model_name='stolovayapodacha',
            name='obedkg1',
            field=models.TimeField(blank=True, null=True, verbose_name='Договор Тип1(нет супа)'),
        ),
        migrations.AlterField(
            model_name='stolovayapodacha',
            name='obedkg2',
            field=models.TimeField(blank=True, null=True, verbose_name='Договор Тип2(суп)'),
        ),
        migrations.AlterField(
            model_name='stolovayapriemipishi',
            name='obedkg1',
            field=models.TimeField(blank=True, null=True, verbose_name='Договор Тип1(нет супа)'),
        ),
        migrations.AlterField(
            model_name='stolovayapriemipishi',
            name='obedkg2',
            field=models.TimeField(blank=True, null=True, verbose_name='Договор Тип2(суп)'),
        ),
    ]
