# Generated by Django 4.1.1 on 2022-10-31 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_checkoutaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default=0, upload_to='images'),
        ),
    ]
