# Generated by Django 2.2.3 on 2021-12-05 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar', '0021_auto_20211203_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='telephone',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
