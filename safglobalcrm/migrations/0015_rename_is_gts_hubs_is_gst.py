# Generated by Django 5.0 on 2024-06-26 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('safglobalcrm', '0014_alter_customers_all_account_manager_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hubs',
            old_name='is_gts',
            new_name='is_gst',
        ),
    ]
