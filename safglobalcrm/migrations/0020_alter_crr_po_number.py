# Generated by Django 5.0.6 on 2024-07-24 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safglobalcrm', '0019_alter_cities_slug_alter_states_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crr',
            name='po_number',
            field=models.TextField(),
        ),
    ]