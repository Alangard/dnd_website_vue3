from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal_api", "0042_rename_subscriber_subscription_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="subscribed_to",
            field=models.ManyToManyField(
                blank=True, related_name="subscribers", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]