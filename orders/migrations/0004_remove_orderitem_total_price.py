# Generated by Django 5.0.7 on 2024-08-06 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='total_price',
        ),
    ]
