# Generated by Django 4.2.3 on 2023-07-29 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_rename_customer_id_order_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(max_length=10),
        ),
    ]
