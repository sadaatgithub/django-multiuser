# Generated by Django 4.2.3 on 2023-07-09 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoMultiuserApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccount',
            old_name='type',
            new_name='role',
        ),
    ]
