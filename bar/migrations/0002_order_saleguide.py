# Generated by Django 2.2.3 on 2021-11-06 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleGuide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('price', models.IntegerField()),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bar.Metric')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bar.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reference', models.CharField(max_length=128)),
                ('quantity', models.IntegerField()),
                ('product_name', models.CharField(max_length=128)),
                ('purchase_price', models.IntegerField()),
                ('purchase_metric', models.CharField(max_length=128)),
                ('sale_price', models.IntegerField()),
                ('sale_metric', models.CharField(max_length=128)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bar.Product')),
                ('sale_guide', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bar.SaleGuide')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
