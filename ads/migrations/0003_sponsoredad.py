# Generated by Django 2.2.6 on 2020-11-13 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productreview'),
        ('ads', '0002_ad_fixed_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='SponsoredAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum_price', models.FloatField(blank=True, null=True)),
                ('maximum_price', models.FloatField(blank=True, null=True)),
                ('negotiable', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to='adverts')),
                ('image1', models.ImageField(upload_to='adverts')),
                ('image2', models.ImageField(upload_to='adverts')),
                ('image3', models.ImageField(upload_to='adverts')),
                ('image4', models.ImageField(upload_to='adverts')),
                ('image5', models.ImageField(upload_to='adverts')),
                ('image6', models.ImageField(upload_to='adverts')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('view', models.IntegerField(default=0)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sponsored_ad', to='products.Product')),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sponsored_ads', to='ads.Seller')),
            ],
        ),
    ]
