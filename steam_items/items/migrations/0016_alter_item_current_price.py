# Generated by Django 4.2.8 on 2023-12-22 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0015_alter_item_current_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='current_price',
            field=models.FloatField(default=0.0),
        ),
    ]