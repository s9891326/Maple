# Generated by Django 3.2.11 on 2022-02-06 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0004_alter_equiplibrary_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equip',
            name='stage_level',
            field=models.CharField(blank=True, choices=[('普通', '普通'), ('稀有', '稀有'), ('史詩', '史詩'), ('罕見', '罕見'), ('傳說', '傳說'), ('神話', '神話'), ('古代', '古代'), ('死靈', '死靈')], default='普通', max_length=16, verbose_name='階段等級'),
        ),
        migrations.AlterField(
            model_name='equiplibrary',
            name='category',
            field=models.CharField(choices=[('武器', '武器'), ('防具', '防具'), ('造型', '造型'), ('消耗品', '消耗品'), ('合作', '合作')], default='武器', max_length=16, verbose_name='類別'),
        ),
    ]