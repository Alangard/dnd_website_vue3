# Generated by Django 4.1.7 on 2023-10-25 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("journal_api", "0003_alter_account_is_active_alter_account_is_staff_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="subscription",
            old_name="date_created",
            new_name="subscribtion_datetime",
        ),
    ]
