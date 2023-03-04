# Generated by Django 4.1.7 on 2023-03-03 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipclub', '0006_equipclub_rent_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userrent',
            old_name='hour_rent',
            new_name='last_hour_rent',
        ),
        migrations.AddField(
            model_name='equipclub',
            name='hour_rent',
            field=models.IntegerField(default=0),
        ),
    ]
