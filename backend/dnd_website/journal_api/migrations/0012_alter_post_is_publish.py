# Generated by Django 4.1.7 on 2023-04-17 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal_api", "0011_alter_post_publish_datetime"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="is_publish",
            field=models.BooleanField(default=False),
        ),
    ]
