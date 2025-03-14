# Standard Library
from unittest.mock import patch

# Django
from django.contrib.auth.models import Group
from django.test import TestCase

# AA Discord Announcements
from aa_discord_announcements.helper.announcement_context import (
    get_announcement_context_from_form_data,
    get_webhook_announcement_context,
)
from aa_discord_announcements.models import PingTarget, Webhook


class TestAnnouncementContextTests(TestCase):
    """
    Test the get_announcement_context_from_form_data function
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up groups and users
        """

        super().setUpClass()

        cls.group = Group.objects.create(name="Superhero")

    @patch("aa_discord_announcements.models.PingTarget.objects.get")
    @patch("aa_discord_announcements.models.Webhook.objects.get")
    def test_gets_announcement_context_with_here_mention(
        self, mock_get_webhook, mock_get_ping_target
    ):
        """
        Test the get_announcement_context_from_form_data function with @here mention

        :param mock_get_webhook:
        :type mock_get_webhook:
        :param mock_get_ping_target:
        :type mock_get_ping_target:
        :return:
        :rtype:
        """

        form_data = {
            "announcement_target": "@here",
            "announcement_channel": 1,
            "announcement_text": "Test announcement",
        }

        mock_get_webhook.return_value.url = "http://example.com/webhook"
        context = get_announcement_context_from_form_data(form_data)

        self.assertEqual(context["announcement_target"]["at_mention"], "@here")
        self.assertEqual(
            context["announcement_channel"]["webhook"], "http://example.com/webhook"
        )
        self.assertEqual(context["announcement_text"], "Test announcement")

    @patch("aa_discord_announcements.models.PingTarget.objects.get")
    @patch("aa_discord_announcements.models.Webhook.objects.get")
    def test_gets_announcement_context_with_custom_target(
        self, mock_get_webhook, mock_get_ping_target
    ):
        """
        Test the get_announcement_context_from_form_data function with a custom ping target

        :param mock_get_webhook:
        :type mock_get_webhook:
        :param mock_get_ping_target:
        :type mock_get_ping_target:
        :return:
        :rtype:
        """

        form_data = {
            "announcement_target": self.group,
            "announcement_channel": 1,
            "announcement_text": "Test announcement",
        }

        mock_get_ping_target.return_value = PingTarget(
            discord_id="123456789", name=self.group
        )
        mock_get_webhook.return_value.url = "http://example.com/webhook"

        context = get_announcement_context_from_form_data(form_data)

        self.assertEqual(context["announcement_target"]["group_id"], 123456789)
        self.assertEqual(context["announcement_target"]["group_name"], self.group.name)
        self.assertEqual(
            context["announcement_target"]["at_mention"], f"@{self.group.name}"
        )
        self.assertEqual(
            context["announcement_channel"]["webhook"], "http://example.com/webhook"
        )
        self.assertEqual(context["announcement_text"], "Test announcement")

    @patch("aa_discord_announcements.models.PingTarget.objects.get")
    @patch("aa_discord_announcements.models.Webhook.objects.get")
    def test_handles_nonexistent_custom_target(
        self, mock_get_webhook, mock_get_ping_target
    ):
        """
        Test the get_announcement_context_from_form_data function with a nonexistent custom target

        :param mock_get_webhook:
        :type mock_get_webhook:
        :param mock_get_ping_target:
        :type mock_get_ping_target:
        :return:
        :rtype:
        """

        form_data = {
            "announcement_target": "nonexistent",
            "announcement_channel": 1,
            "announcement_text": "Test announcement",
        }

        mock_get_ping_target.side_effect = PingTarget.DoesNotExist
        mock_get_webhook.return_value.url = "http://example.com/webhook"

        context = get_announcement_context_from_form_data(form_data)

        self.assertIsNone(context["announcement_target"]["group_id"])
        self.assertIsNone(context["announcement_target"]["group_name"])
        self.assertEqual(context["announcement_target"]["at_mention"], "")
        self.assertEqual(
            context["announcement_channel"]["webhook"], "http://example.com/webhook"
        )
        self.assertEqual(context["announcement_text"], "Test announcement")

    @patch("aa_discord_announcements.models.PingTarget.objects.get")
    @patch("aa_discord_announcements.models.Webhook.objects.get")
    def test_handles_nonexistent_webhook(self, mock_get_webhook, mock_get_ping_target):
        """
        Test the get_announcement_context_from_form_data function with a nonexistent webhook

        :param mock_get_webhook:
        :type mock_get_webhook:
        :param mock_get_ping_target:
        :type mock_get_ping_target:
        :return:
        :rtype:
        """

        form_data = {
            "announcement_target": "@here",
            "announcement_channel": "nonexistent",
            "announcement_text": "Test announcement",
        }

        mock_get_webhook.side_effect = Webhook.DoesNotExist

        context = get_announcement_context_from_form_data(form_data)

        self.assertEqual(context["announcement_target"]["at_mention"], "@here")
        self.assertIsNone(context["announcement_channel"]["webhook"])
        self.assertEqual(context["announcement_text"], "Test announcement")


class TestWebhookAnnouncementContextTests(TestCase):
    """
    Test the get_webhook_announcement_context function
    """

    def test_returns_correct_context_with_group_id(self):
        """
        Test the get_webhook_announcement_context function with a group ID

        :return:
        :rtype:
        """

        announcement_context = {
            "announcement_target": {"group_id": 123456789},
            "announcement_text": "Test announcement",
        }

        result = get_webhook_announcement_context(announcement_context)

        self.assertEqual(result["content"], "<@&123456789>\n\nTest announcement")

    def test_returns_correct_context_with_at_here(self):
        """
        Test the get_webhook_announcement_context function with an @here mention

        :return:
        :rtype:
        """

        announcement_context = {
            "announcement_target": {"group_id": None, "at_mention": "@here"},
            "announcement_text": "Test announcement",
        }

        result = get_webhook_announcement_context(announcement_context)

        self.assertEqual(result["content"], "@here\n\nTest announcement")

    def test_handles_empty_announcement_text(self):
        """
        Test the get_webhook_announcement_context function with an empty announcement text

        :return:
        :rtype:
        """

        announcement_context = {
            "announcement_target": {"group_id": 123456789, "at_mention": ""},
            "announcement_text": "",
        }

        result = get_webhook_announcement_context(announcement_context)

        self.assertEqual(result["content"], "<@&123456789>")

    def test_handles_empty_announcement_target(self):
        """
        Test the get_webhook_announcement_context function with an empty announcement target

        :return:
        :rtype:
        """

        announcement_context = {
            "announcement_target": {"group_id": None, "at_mention": ""},
            "announcement_text": "Test announcement",
        }

        result = get_webhook_announcement_context(announcement_context)

        self.assertEqual(result["content"], "\n\nTest announcement")

    def test_handles_empty_context(self):
        """
        Test the get_webhook_announcement_context function with an empty context

        :return:
        :rtype:
        """

        announcement_context = {
            "announcement_target": {"group_id": None, "at_mention": ""},
            "announcement_text": "",
        }

        result = get_webhook_announcement_context(announcement_context)

        self.assertEqual(result["content"], "")
