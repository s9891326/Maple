# Generated by Django 3.2.11 on 2022-06-13 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='server_name',
            field=models.CharField(choices=[('傑尼斯', '傑尼斯'), ('斯卡尼亞', '斯卡尼亞'), ('露娜', '露娜'), ('溫迪亞', '溫迪亞'), ('凱伊尼', '凱伊尼')], max_length=8, verbose_name='伺服器'),
        ),
    ]
