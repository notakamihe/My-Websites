# Generated by Django 3.1.4 on 2020-12-28 04:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_auto_20201228_0431'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=2000, validators=[django.core.validators.MinLengthValidator(10)])),
                ('replier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.profile')),
                ('to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.forumpost')),
            ],
        ),
    ]
