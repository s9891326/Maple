# Generated by Django 3.2.11 on 2022-06-13 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='標題')),
                ('value', models.IntegerField(verbose_name='幣值')),
                ('total', models.IntegerField(verbose_name='總額')),
                ('pay_method', models.CharField(max_length=16, verbose_name='支付方式')),
                ('contact_method', models.CharField(choices=[('Email', 'Email'), ('Line', 'Line'), ('其他', '其他')], max_length=8, verbose_name='聯絡方式')),
                ('contact_explanation', models.CharField(blank=True, max_length=32, null=True, verbose_name='其他方式的敘述')),
                ('server_name', models.CharField(choices=[('傑尼斯', '傑尼斯'), ('斯卡尼亞', '斯卡尼亞'), ('露娜', '露娜'), ('溫迪亞', '溫迪亞'), ('凱伊尼', '凱伊尼')], max_length=8, verbose_name='伺服器')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='上架日期')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='創建者')),
            ],
            options={
                'verbose_name': '楓幣',
                'verbose_name_plural': '楓幣',
            },
        ),
    ]