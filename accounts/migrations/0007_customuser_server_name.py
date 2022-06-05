# Generated by Django 3.2.11 on 2022-06-04 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customuser_line_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='server_name',
            field=models.CharField(choices=[('無', '無'), ('傑尼斯', '傑尼斯'), ('斯卡尼亞', '斯卡尼亞'), ('露娜', '露娜'), ('溫迪亞', '溫迪亞'), ('凱伊尼', '凱伊尼')], default='無', max_length=8, verbose_name='伺服器'),
        ),
    ]
