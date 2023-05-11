# Generated by Django 4.1.7 on 2023-04-17 14:21

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal_api", "0004_alter_post_publish_datetime"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="publish_datetime",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2023, 4, 17, 17, 21, 6, 848152),
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(
                        datetime.datetime(2023, 4, 17, 17, 26, 6, 848152)
                    )
                ],
            ),
        ),
    ]