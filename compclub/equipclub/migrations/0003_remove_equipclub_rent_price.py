# Generated by Django 4.1.7 on 2023-03-01 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipclub', '0002_equipclub_userrent_delete_equipment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipclub',
            name='rent_price',
        ),
    ]
