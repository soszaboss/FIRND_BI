# Generated by Django 5.1.1 on 2024-09-09 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_created_account_modified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='date_joined',
        ),
    ]
