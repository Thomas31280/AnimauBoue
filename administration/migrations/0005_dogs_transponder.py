# Generated by Django 3.2.9 on 2021-12-21 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0004_auto_20211215_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='dogs',
            name='transponder',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
