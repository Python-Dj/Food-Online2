# Generated by Django 5.1.2 on 2024-11-15 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0003_tax'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tax',
            options={'verbose_name_plural': 'Taxes'},
        ),
    ]
