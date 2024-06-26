# Generated by Django 5.0 on 2024-04-11 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safglobalcrm', '0008_alter_shipmentservicedetails_air_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='crrdocuments',
            name='crr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='safglobalcrm.crr'),
        ),
        migrations.AddField(
            model_name='crrstockitem',
            name='crr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='safglobalcrm.crr'),
        ),
        migrations.AlterField(
            model_name='crr',
            name='agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='safglobalcrm.agents'),
        ),
        migrations.AlterField(
            model_name='crr',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('D', 'Delivered'), ('O', 'On Call')], default='P', max_length=1),
        ),
    ]
