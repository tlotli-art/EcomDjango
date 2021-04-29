# Generated by Django 3.1.7 on 2021-04-10 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iMarket', '0002_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='digital',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='complete',
            field=models.BooleanField(default=False, null=True),
        ),
    ]