# Generated by Django 4.1.7 on 2023-03-01 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipclub', '0004_equipclub_rent_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipclub',
            name='rent_price',
        ),
    ]
