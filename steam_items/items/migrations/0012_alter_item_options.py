# Generated by Django 4.2.8 on 2023-12-21 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0011_alter_itemaddition_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['name']},
        ),
    ]
