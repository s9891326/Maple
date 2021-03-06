# Generated by Django 3.2.11 on 2022-06-26 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0002_auto_20220622_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='server_name',
            field=models.CharField(choices=[('jenes', '傑尼斯'), ('scania', '斯卡尼亞'), ('luna', '露娜'), ('vindia', '溫迪亞'), ('kainey', '凱伊尼')], max_length=8, verbose_name='伺服器'),
        ),
        migrations.AlterField(
            model_name='coin',
            name='total',
            field=models.IntegerField(verbose_name='總額(x億楓幣)'),
        ),
    ]
