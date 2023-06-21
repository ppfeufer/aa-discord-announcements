# Generated by Django 4.0.10 on 2023-06-19 10:01

# Django
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("aa_discord_announcements", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pingtarget",
            name="discord_id",
            field=models.CharField(
                blank=True,
                help_text="ID of the Discord role to ping",
                max_length=255,
                unique=True,
                verbose_name="Discord ID",
            ),
        ),
        migrations.AlterField(
            model_name="pingtarget",
            name="is_enabled",
            field=models.BooleanField(
                db_index=True,
                default=True,
                help_text="Whether this ping target is enabled or not",
                verbose_name="Is enabled",
            ),
        ),
        migrations.AlterField(
            model_name="pingtarget",
            name="name",
            field=models.OneToOneField(
                help_text="Name of the Discord role to ping. (Note: This must be an Auth group that is synced to Discord.)",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="discord_announcement_pingtarget",
                to="auth.group",
                verbose_name="Group name",
            ),
        ),
        migrations.AlterField(
            model_name="pingtarget",
            name="notes",
            field=models.TextField(
                blank=True,
                default="",
                help_text="You can add notes about this configuration here if you want",
                verbose_name="Notes",
            ),
        ),
        migrations.AlterField(
            model_name="pingtarget",
            name="restricted_to_group",
            field=models.ManyToManyField(
                blank=True,
                help_text="Restrict ping rights to the following group(s) …",
                related_name="discord_announcement_pingtarget_required_groups",
                to="auth.group",
                verbose_name="Group restrictions",
            ),
        ),
        migrations.AlterField(
            model_name="webhook",
            name="is_enabled",
            field=models.BooleanField(
                db_index=True,
                default=True,
                help_text="Whether this webhook is active or not",
                verbose_name="Is enabled",
            ),
        ),
        migrations.AlterField(
            model_name="webhook",
            name="name",
            field=models.CharField(
                help_text="Name of the channel this webhook posts to",
                max_length=255,
                unique=True,
                verbose_name="Discord channel",
            ),
        ),
        migrations.AlterField(
            model_name="webhook",
            name="notes",
            field=models.TextField(
                blank=True,
                default="",
                help_text="You can add notes about this webhook here if you want",
                verbose_name="Notes",
            ),
        ),
        migrations.AlterField(
            model_name="webhook",
            name="restricted_to_group",
            field=models.ManyToManyField(
                blank=True,
                help_text="Restrict ping rights to the following group(s) …",
                related_name="discord_announcement_webhook_required_groups",
                to="auth.group",
                verbose_name="Group restrictions",
            ),
        ),
        migrations.AlterField(
            model_name="webhook",
            name="url",
            field=models.CharField(
                help_text="URL of this webhook, e.g. https://discord.com/api/webhooks/123456/abcdef",
                max_length=255,
                unique=True,
                verbose_name="Webhook URL",
            ),
        ),
    ]