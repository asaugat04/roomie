# Generated by Django 5.0.6 on 2024-05-11 21:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_profile_lives_in_alter_room_listed_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='lives_in',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.room'),
        ),
    ]
