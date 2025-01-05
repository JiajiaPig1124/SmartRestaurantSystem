# Generated by Django 3.2.8 on 2025-01-05 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='菜系名称')),
                ('description', models.TextField(blank=True, verbose_name='描述')),
            ],
            options={
                'verbose_name': '菜系',
                'verbose_name_plural': '菜系',
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='菜品名称')),
                ('description', models.TextField(blank=True, verbose_name='描述')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价格')),
                ('image', models.ImageField(blank=True, upload_to='dishes/', verbose_name='图片')),
                ('is_available', models.BooleanField(default=True, verbose_name='是否可用')),
                ('stock', models.IntegerField(default=0, verbose_name='库存')),
                ('sales_count', models.IntegerField(default=0, verbose_name='销量')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('cuisine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='menu.cuisine', verbose_name='菜系')),
            ],
            options={
                'verbose_name': '菜品',
                'verbose_name_plural': '菜品',
                'ordering': ['-sales_count'],
            },
        ),
    ]
