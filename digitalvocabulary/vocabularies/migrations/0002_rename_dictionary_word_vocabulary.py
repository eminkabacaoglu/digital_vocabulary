# Generated by Django 5.1.2 on 2024-10-14 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vocabularies', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='word',
            old_name='dictionary',
            new_name='vocabulary',
        ),
    ]