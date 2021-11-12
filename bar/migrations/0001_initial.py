# Generated by Django 2.2.3 on 2021-11-06 02:00

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
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('unit', models.CharField(max_length=128)),
                ('symbol', models.CharField(max_length=64)),
                ('multiplier', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MetricSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('is_standard', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('brand', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=2048)),
                ('barcode', models.CharField(max_length=128)),
                ('quantity', models.FloatField()),
                ('purchase_price', models.IntegerField()),
                ('metric_system', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bar.MetricSystem')),
                ('purchase_metric', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bar.Metric')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bar.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=254)),
                ('telephone', models.CharField(max_length=16)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCatgories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bar.Category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bar.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='metric',
            name='metric_system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bar.MetricSystem'),
        ),
        migrations.AddField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(through='bar.ProductCatgories', to='bar.Product'),
        ),
    ]
