# Generated by Django 5.0 on 2024-06-21 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safglobalcrm', '0013_alter_customers_responsible_office'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='all_account_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_account_manager', to='safglobalcrm.officeusers'),
        ),
        migrations.AlterField(
            model_name='customers',
            name='main_account_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_account_manager', to='safglobalcrm.officeusers'),
        ),
        migrations.AlterField(
            model_name='customers',
            name='responsible_office',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='safglobalcrm.offices'),
        ),
    ]
