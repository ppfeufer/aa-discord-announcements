"""
Test models
"""

# Django
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.test import TestCase, modify_settings

# AA Discord Announcements
from aa_discord_announcements.models import PingTarget, Webhook


class TestModels(TestCase):
    """
    Test our models
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up groups and users
        """

        super().setUpClass()

        cls.group = Group.objects.create(name="Superhero")

    def test_discord_webhook_valid_webhook_url(self):
        """
        Test if we DO NOT get a ValidationError for a Discord webhook
        :return:
        """

        # given
        webhook = Webhook(
            url=(
                "https://discord.com/api/webhooks/873266850833505395/"
                "3pZfW9m66VO-LVomItmu2hEWFJnQkbj1aHOsPw2D6Zz-C2poLto1BArweS2pxTE7rrnI"
            ),
        )

        # when (should not fail and raise an exception)
        webhook.clean()

    def test_discord_webhook_invalid_webhook_url_should_throw_exception(self):
        """
        Test if we get a ValidationError for a Discord webhook
        :return:
        """

        # given
        webhook = Webhook(
            url=(
                "https://discord.com/api/webhooks/754119343402302920F/x-BfFCdEG"
                "-qGg_39_mFUqRSLoz2dm6Oa8vxNdaAxZdgKOAyesVpy-Bzf8wDU_vHdFpm-"
            ),
        )

        # when
        with self.assertRaises(ValidationError):
            webhook.clean()

        with self.assertRaisesMessage(
            ValidationError,
            expected_message=(
                "Invalid webhook URL. The webhook URL you entered does not match any "
                "known format for a Discord webhook. Please check the "
                "webhook URL."
            ),
        ):
            webhook.clean()

    @modify_settings(INSTALLED_APPS={"remove": "allianceauth.services.modules.discord"})
    def test_should_raise_validation_error_for_not_activated_discord_service(self):
        """
        Test should raise a validation error when Discord service is not active
        :return:
        """

        # given
        ping_target = PingTarget(name=self.group, discord_id=123456789)

        # when
        with self.assertRaises(ValidationError):
            ping_target.clean()

        with self.assertRaisesMessage(
            ValidationError,
            expected_message=(
                "You might want to install the Discord service first ..."
            ),
        ):
            ping_target.clean()
