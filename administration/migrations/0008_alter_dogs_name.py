# Generated by Django 3.2.9 on 2021-12-30 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0007_alter_dogs_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dogs',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
