# Generated by Django 5.0 on 2024-04-04 09:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safglobalcrm', '0002_alter_hubadditionalofficeaddress_hub_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hubadditionalofficeaddress',
            name='hub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additionalAddresses', to='safglobalcrm.hubs'),
        ),
    ]
