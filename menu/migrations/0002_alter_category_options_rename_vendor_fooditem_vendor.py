# Generated by Django 5.1.2 on 2024-10-23 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.RenameField(
            model_name='fooditem',
            old_name='Vendor',
            new_name='vendor',
        ),
    ]
