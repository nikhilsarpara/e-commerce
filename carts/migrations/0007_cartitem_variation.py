# Generated by Django 5.1.2 on 2025-01-10 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0006_cartitem_color_cartitem_size'),
        ('store', '0003_veriation'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variation',
            field=models.ManyToManyField(blank=True, to='store.veriation'),
        ),
    ]
