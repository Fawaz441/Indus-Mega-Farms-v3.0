# Generated by Django 2.2.6 on 2021-04-03 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0007_auto_20210403_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='exhausted',
            field=models.BooleanField(default=False),
        ),
    ]