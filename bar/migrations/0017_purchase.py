# Generated by Django 2.2.3 on 2021-11-28 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0016_auto_20211119_0736'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField()),
                ('product_name', models.CharField(max_length=128)),
                ('purchase_price', models.IntegerField()),
                ('purchase_metric', models.CharField(max_length=128)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bar.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
