# Generated by Django 5.1.2 on 2025-01-11 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0007_cartitem_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='color',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='size',
        ),
    ]
