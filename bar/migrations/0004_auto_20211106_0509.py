# Generated by Django 2.2.3 on 2021-11-06 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0003_order_is_standard'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='is_standard',
            new_name='is_served',
        ),
    ]
