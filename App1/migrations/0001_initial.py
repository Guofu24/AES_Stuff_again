# Generated by Django 5.0.5 on 2024-06-24 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stuff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Firstname', models.CharField(max_length=255)),
                ('Lastname', models.CharField(max_length=255)),
                ('Position', models.CharField(max_length=255)),
                ('Year', models.CharField(max_length=4)),
                ('Phone', models.CharField(max_length=10)),
                ('Address', models.CharField(max_length=255)),
            ],
        ),
    ]
