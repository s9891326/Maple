# Generated by Django 3.2.11 on 2022-02-07 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0007_auto_20220207_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equip',
            name='profession',
        ),
        migrations.AddField(
            model_name='equiplibrary',
            name='profession',
            field=models.CharField(default='共用', max_length=64, verbose_name='裝備職業'),
        ),
    ]
