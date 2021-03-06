# Generated by Django 3.2.11 on 2022-06-04 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import exchange.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('star', models.IntegerField(verbose_name='星力')),
                ('level', models.IntegerField(verbose_name='裝備等級')),
                ('total_level', models.IntegerField(verbose_name='裝備總等級')),
                ('cut_num', models.IntegerField(blank=True, default=0, verbose_name='剩餘剪刀數')),
                ('attack', models.IntegerField(blank=True, default=0, verbose_name='攻擊力')),
                ('main_attribute', models.CharField(blank=True, max_length=16, null=True, verbose_name='主屬性')),
                ('potential_level', models.CharField(choices=[('無', '無'), ('稀有', '稀有'), ('史詩', '史詩'), ('罕見', '罕見'), ('傳說', '傳說')], default='無', max_length=8, verbose_name='淺力等級')),
                ('potential_capability', models.CharField(default='', max_length=64, verbose_name='淺力能力')),
                ('spark_level', models.CharField(choices=[('無', '無'), ('罕見', '罕見'), ('傳說', '傳說'), ('神話', '神話')], default='無', max_length=8, verbose_name='星火等級')),
                ('spark_capability', models.CharField(default='', max_length=64, verbose_name='星火能力')),
                ('is_equippable_soul', models.BooleanField(default=False, verbose_name='可裝備靈魂')),
                ('soul_capability', models.CharField(blank=True, max_length=64, null=True, verbose_name='靈魂能力')),
                ('is_maple', models.BooleanField(verbose_name='是否楓葉底')),
                ('maple_capability', models.CharField(choices=[('無', '無'), ('殘忍的紋章', '殘忍的紋章'), ('征服紋章', '征服紋章'), ('機靈紋章', '機靈紋章'), ('強力紋章', '強力紋章'), ('神聖紋章', '神聖紋章')], default='無', max_length=16, verbose_name='楓底能力')),
                ('maple_level', models.IntegerField(default=0, verbose_name='楓底等級')),
                ('price', models.BigIntegerField(db_index=True, verbose_name='價錢')),
                ('explanation', models.TextField(blank=True, default='', verbose_name='說明')),
                ('label_level', models.IntegerField(choices=[(0, '無'), (1, '特殊'), (2, '紅色'), (3, '黑色'), (4, '大師')], default=0, verbose_name='標籤等級')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='上架日期')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('title', models.CharField(blank=True, max_length=32, null=True, verbose_name='商品標題')),
                ('server_name', models.CharField(choices=[('無', '無'), ('傑尼斯', '傑尼斯'), ('斯卡尼亞', '斯卡尼亞'), ('露娜', '露娜'), ('溫迪亞', '溫迪亞'), ('凱伊尼', '凱伊尼')], max_length=8, verbose_name='伺服器')),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='創建者')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
            },
        ),
        migrations.CreateModel(
            name='ProductList',
            fields=[
                ('product_list_id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('武器', '武器'), ('防具', '防具'), ('造型', '造型'), ('消耗品', '消耗品')], default='武器', max_length=16, verbose_name='類別')),
                ('type', models.CharField(max_length=16, verbose_name='種類')),
                ('name', models.CharField(db_index=True, max_length=16, verbose_name='裝備名稱')),
                ('stage_level', models.IntegerField(choices=[(0, '共用'), (1, '普通'), (2, '稀有'), (3, '史詩'), (4, '罕見'), (5, '傳說'), (6, '神話'), (7, '古代'), (8, '死靈')], default=0, verbose_name='階段等級')),
                ('image', models.ImageField(blank=True, upload_to=exchange.models.PathAndRename('product_list_image'), verbose_name='商品列圖片')),
            ],
            options={
                'verbose_name': '商品列',
                'verbose_name_plural': '商品列',
                'unique_together': {('category', 'type', 'stage_level', 'name')},
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('product_image_id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=exchange.models.PathAndRename('product_image'), verbose_name='商品圖片')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='exchange.product', verbose_name='商品')),
            ],
            options={
                'verbose_name': '裝備圖庫',
                'verbose_name_plural': '裝備圖庫',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='exchange.productlist', verbose_name='商品列'),
        ),
    ]
