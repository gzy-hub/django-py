# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-01-27 03:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('mall', '0002_delete_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='商品名称')),
                ('img', models.ImageField(upload_to='', verbose_name='商品的主图')),
                ('price', models.IntegerField(verbose_name='兑换价格')),
                ('origin_price', models.FloatField(verbose_name='原价')),
                ('count', models.PositiveIntegerField(verbose_name='购买数量')),
                ('amount', models.FloatField(verbose_name='总额')),
                ('status', models.SmallIntegerField(choices=[(10, '购物车'), (11, '已提交'), (12, '已支付'), (13, '已发货'), (14, '已完成'), (15, '已删除')], default=10, verbose_name='状态')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'db_table': 'mine_cart',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=256, verbose_name='评价内容')),
                ('reorder', models.SmallIntegerField(default=0, verbose_name='排序')),
                ('is_anonymous', models.BooleanField(default=True, verbose_name='是否匿名')),
                ('score', models.FloatField(default=10.0, verbose_name='商品评分')),
                ('score_deliver', models.FloatField(default=10.0, verbose_name='配送服务分')),
                ('score_package', models.FloatField(default=10.0, verbose_name='快递包装分')),
                ('score_speed', models.FloatField(default=10.0, verbose_name='送货速度分')),
                ('is_valid', models.BooleanField(default=True, verbose_name='是否有效')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
            ],
            options={
                'db_table': 'mine_product_comments',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=32, verbose_name='订单编码')),
                ('buy_count', models.IntegerField(default=1, verbose_name='购买数量')),
                ('buy_amount', models.FloatField(verbose_name='总价')),
                ('to_user', models.CharField(max_length=32, verbose_name='收货人')),
                ('to_area', models.CharField(max_length=32, verbose_name='省市区')),
                ('to_address', models.CharField(max_length=256, verbose_name='详细地址')),
                ('to_phone', models.CharField(max_length=32, verbose_name='手机号码')),
                ('remark', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
                ('express_type', models.CharField(blank=True, max_length=32, null=True, verbose_name='快递')),
                ('express_no', models.CharField(blank=True, max_length=32, null=True, verbose_name='单号')),
                ('status', models.SmallIntegerField(choices=[(10, '购物车'), (11, '已提交'), (12, '已支付'), (13, '已发货'), (14, '已完成'), (15, '已删除')], default=11, verbose_name='订单状态')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='accounts.User')),
            ],
            options={
                'db_table': 'mine_order',
            },
        ),
        migrations.AddField(
            model_name='comments',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='mine.Order', verbose_name='订单'),
        ),
        migrations.AddField(
            model_name='comments',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='mall.Product', verbose_name='商品'),
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='accounts.User', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='cart',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mine.Order', verbose_name='订单'),
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mall.Product'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='accounts.User'),
        ),
    ]
