# Generated by Django 3.1.7 on 2021-04-10 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iMarket', '0003_auto_20210410_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
