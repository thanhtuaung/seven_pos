# Generated by Django 4.2.3 on 2023-07-29 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='customer_id',
            new_name='customer',
        ),
    ]
