# Generated by Django 3.1.4 on 2020-12-26 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20201226_0121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forumuser',
            old_name='last_name',
            new_name='surname',
        ),
    ]
