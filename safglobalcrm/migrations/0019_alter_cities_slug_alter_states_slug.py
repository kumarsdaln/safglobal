# Generated by Django 5.0.6 on 2024-07-12 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safglobalcrm', '0018_alter_countries_phonecode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cities',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AlterField(
            model_name='states',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
