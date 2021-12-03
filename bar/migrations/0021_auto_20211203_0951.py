# Generated by Django 2.2.3 on 2021-12-03 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0020_ordergroup_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AlterField(
            model_name='ordergroup',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'PENDING'), (1, 'READY'), (2, 'PAID')], default=0),
        ),
    ]
