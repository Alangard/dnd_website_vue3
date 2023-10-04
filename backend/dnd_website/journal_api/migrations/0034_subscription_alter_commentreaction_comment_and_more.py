# Generated by Django 4.1.7 on 2023-10-03 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("journal_api", "0033_post_allow_comments"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subscribed_to",
                    models.ManyToManyField(
                        related_name="subscribers", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "subscriber",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subscriptions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Subscription",
                "verbose_name_plural": "Subscription",
                "db_table": "Subscription",
            },
        ),
        migrations.AlterField(
            model_name="commentreaction",
            name="comment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comment_reactions",
                to="journal_api.comment",
            ),
        ),
        migrations.AlterField(
            model_name="commentreaction",
            name="reaction_type",
            field=models.CharField(
                blank=True,
                choices=[("like", "Like"), ("dislike", "Dislike")],
                max_length=10,
                null=True,
            ),
        ),
        migrations.DeleteModel(
            name="PostBodyImage",
        ),
    ]