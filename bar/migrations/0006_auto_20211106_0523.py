# Generated by Django 2.2.3 on 2021-11-06 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0005_auto_20211106_0517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_served',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'PENDING'), (1, 'READY'), (2, 'PAID')], default=0),
        ),
    ]
