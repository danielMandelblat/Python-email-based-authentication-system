# Generated by Django 5.1 on 2024-08-28 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0005_authentication_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='code_timeout',
            field=models.PositiveIntegerField(default=30, help_text='minutes'),
        ),
    ]
