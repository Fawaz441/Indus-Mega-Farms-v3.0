# Generated by Django 2.2.6 on 2020-11-13 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0003_sponsoredad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsoredad',
            name='image1',
        ),
        migrations.AddField(
            model_name='sponsoredad',
            name='category',
            field=models.CharField(blank=True, choices=[('PROCESSED_FOOD', 'PROCESSED_FOOD'), ('CROPS', 'CROPS'), ('FRUITS', 'FRUITS'), ('LIVESTOCK', 'LIVESTOCK'), ('STUDENT_ITEMS', 'STUDENT_ITEMS'), ('FARM_TOOLS', 'FARM_TOOLS'), ('FARM_MACHINERY', 'FARM_MACHINERY'), ('FARM_SERVICES', 'FARM_SERVICES'), ('FOOD_STUFF', 'FOOD_STUFF'), ('LAND', 'LAND'), ('OTHER', 'OTHER')], max_length=100, null=True),
        ),
    ]
