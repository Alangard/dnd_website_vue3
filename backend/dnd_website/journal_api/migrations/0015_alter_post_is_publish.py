# Generated by Django 4.1.7 on 2023-04-17 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal_api", "0014_alter_post_is_publish"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="is_publish",
            field=models.BooleanField(default=True),
        ),
    ]