# Generated by Django 3.2.16 on 2023-01-27 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stolovaya', '0039_auto_20230123_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='stolovaya',
            name='qrcode',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='QR_Code'),
        ),
        migrations.AlterField(
            model_name='stolovayapodacha',
            name='zavtrakg',
            field=models.TimeField(blank=True, null=True, verbose_name='Завтрак(Льгот)'),
        ),
        migrations.AlterField(
            model_name='stolovayapriemipishi',
            name='zavtrakg',
            field=models.TimeField(blank=True, null=True, verbose_name='Завтрак(Льгот)'),
        ),
    ]
