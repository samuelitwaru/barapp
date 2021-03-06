# Generated by Django 2.2.3 on 2021-11-06 05:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bar', '0004_auto_20211106_0509'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cashier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cashier', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='waiter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='waiter', to=settings.AUTH_USER_MODEL),
        ),
    ]
