# Generated by Django 2.2.6 on 2020-11-20 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20201114_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderedproduct',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='in_cart', to='products.Product'),
        ),
    ]
