# Generated by Django 3.2.16 on 2024-02-28 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stolovaya', '0044_auto_20240109_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stolovayacategory',
            name='category',
            field=models.CharField(choices=[('normal', 'Обычные'), ('lgota14', 'Льготники младшие'), ('lgota59', 'Льготники старшие'), ('internat14', 'Интернат младшие'), ('internat59', 'Интернат старшие'), ('dogovor1', 'Договор Тип1(нет супа)'), ('dogovor2', 'Договор Тип2(суп)'), ('dogovor3', 'Договор Тип3(суп)')], default='normal', max_length=255, verbose_name='typeofeda'),
        ),
        migrations.AlterField(
            model_name='stolovayaclasspit',
            name='obedkg3',
            field=models.TimeField(blank=True, null=True, verbose_name='Договор Тип3(суп)'),
        ),
        migrations.AlterField(
            model_name='stolovayapodacha',
            name='obedkg3',
            field=models.TimeField(blank=True, default='09:15:00', null=True, verbose_name='Договор Тип3(суп)'),
        ),
        migrations.AlterField(
            model_name='stolovayapriemipishi',
            name='obedkg3',
            field=models.TimeField(blank=True, default='09:30:00', null=True, verbose_name='Договор Тип3(суп)'),
        ),
        migrations.CreateModel(
            name='stolovayadietflag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime1', models.DateTimeField(verbose_name='DateTime_otmetka')),
                ('dateeda', models.DateField(verbose_name='Date_pitania')),
                ('dietflag', models.BooleanField(default=False, verbose_name='dieta')),
                ('uchid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stolovaya.stolovaya', verbose_name='id_uchenika')),
            ],
        ),
    ]
