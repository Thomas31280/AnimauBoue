# Generated by Django 3.2.9 on 2021-12-11 00:04

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('email', models.EmailField(blank=True, max_length=65, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.clients')),
            ],
        ),
        migrations.CreateModel(
            name='Parks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2)),
                ('availability', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.SmallIntegerField()),
                ('dog_1_arrival', models.DateTimeField()),
                ('dog_1_departure', models.DateTimeField()),
                ('dog_2_arrival', models.DateTimeField(blank=True)),
                ('dog_2_departure', models.DateTimeField(blank=True)),
                ('dog_3_arrival', models.DateTimeField(blank=True)),
                ('dog_3_departure', models.DateTimeField(blank=True)),
                ('dog_4_arrival', models.DateTimeField(blank=True)),
                ('dog_4_departure', models.DateTimeField(blank=True)),
                ('dog_5_arrival', models.DateTimeField(blank=True)),
                ('dog_5_departure', models.DateTimeField(blank=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.clients')),
                ('dog_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dog_1_relation', to='administration.dogs')),
                ('dog_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dog_2_relation', to='administration.dogs')),
                ('dog_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dog_3_relation', to='administration.dogs')),
                ('dog_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dog_4_relation', to='administration.dogs')),
                ('dog_5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dog_5_relation', to='administration.dogs')),
                ('park', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.parks')),
            ],
        ),
        migrations.AddIndex(
            model_name='clients',
            index=models.Index(fields=['first_name', 'name'], name='administrat_first_n_51b5a7_idx'),
        ),
    ]