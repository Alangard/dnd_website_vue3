# Generated by Django 4.1.7 on 2023-04-15 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal_api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="publish_datetime",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
