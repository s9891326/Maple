# Generated by Django 3.2.11 on 2022-02-05 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0002_alter_equip_equip_library'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equip',
            name='equip_library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exchange.equiplibrary', verbose_name='裝備庫'),
        ),
    ]
