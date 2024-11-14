# Generated by Django 5.1.2 on 2024-11-13 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0007_rename_to_closed_openinghour_is_closed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openinghour',
            options={'ordering': ('day', '-from_hour')},
        ),
        migrations.AlterUniqueTogether(
            name='openinghour',
            unique_together={('vendor', 'day', 'from_hour', 'to_hour')},
        ),
    ]