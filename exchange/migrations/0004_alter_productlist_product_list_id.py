# Generated by Django 3.2.11 on 2022-02-12 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0003_alter_productlist_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productlist',
            name='product_list_id',
            field=models.AutoField(db_index=True, primary_key=True, serialize=False),
        ),
    ]