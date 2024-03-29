# Generated by Django 3.2.11 on 2022-10-07 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0009_auto_20220921_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='level',
            field=models.IntegerField(default=0, verbose_name='裝備等級'),
        ),
        migrations.AlterField(
            model_name='product',
            name='maple_capability',
            field=models.CharField(choices=[('null', '無'), ('cruel', '殘忍的紋章'), ('conquer', '征服紋章'), ('clever', '機靈紋章'), ('strong', '強力紋章'), ('sacred', '神聖紋章'), ('sharp', '銳利紋章'), ('experience', '經驗紋章'), ('adjudgement', '審判紋章'), ('defense', '忍耐紋章'), ('physical', '毀滅紋章')], default='null', max_length=16, verbose_name='楓底能力'),
        ),
        migrations.AlterField(
            model_name='product',
            name='total_level',
            field=models.IntegerField(default=0, verbose_name='裝備總等級'),
        ),
    ]
