# Generated by Django 3.1.4 on 2020-12-26 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20201226_0229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forumuser',
            name='username',
        ),
    ]
