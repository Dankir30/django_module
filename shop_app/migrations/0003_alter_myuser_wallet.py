# Generated by Django 4.2.1 on 2023-05-08 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0002_alter_buyitemreturn_buy_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='wallet',
            field=models.DecimalField(decimal_places=2, default=10000, max_digits=15),
        ),
    ]
