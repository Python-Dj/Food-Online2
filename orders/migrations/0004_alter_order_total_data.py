# Generated by Django 5.1.2 on 2024-11-21 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_total_data_order_vendors_alter_order_tax_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]