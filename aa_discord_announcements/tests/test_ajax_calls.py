"""
Test ajax calls
"""

# Standard Library
from http import HTTPStatus

# Django
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

# AA Discord Announcements
from aa_discord_announcements.tests.utils import create_fake_user


class TestAccess(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up groups and users
        """

        super().setUpClass()

        cls.group = Group.objects.create(name="Superhero")

        # User cannot access fleetpings
        cls.user_1001 = create_fake_user(1001, "Peter Parker")

        # User can access fleetpings
        cls.user_1002 = create_fake_user(
            1002, "Bruce Wayne", permissions=["aa_discord_announcements.basic_access"]
        )

    def test_ajax_get_ping_targets_no_access(self):
        """
        Test ajax call to get ping targets available for
        the current user without access to it
        :return:
        """

        # given
        self.client.force_login(self.user_1001)

        # when
        res = self.client.get(
            reverse("aa_discord_announcements:ajax_get_announcement_targets")
        )

        # then
        self.assertEqual(res.status_code, HTTPStatus.FOUND)

    def test_ajax_get_ping_targets_general(self):
        """
        Test ajax call to get ping targets available for the current user
        :return:
        """

        # given
        self.client.force_login(self.user_1002)

        # when
        res = self.client.get(
            reverse("aa_discord_announcements:ajax_get_announcement_targets")
        )

        # then
        self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_ajax_get_webhooks_no_access(self):
        """
        Test ajax call to get webhooks available for
        the current user without access to it
        :return:
        """

        # given
        self.client.force_login(self.user_1001)

        # when
        res = self.client.get(reverse("aa_discord_announcements:ajax_get_webhooks"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.FOUND)

    def test_ajax_get_webhooks_general(self):
        """
        Test ajax call to get webhooks available for the current user
        :return:
        """

        # given
        self.client.force_login(self.user_1002)

        # when
        res = self.client.get(reverse("aa_discord_announcements:ajax_get_webhooks"))

        # then
        self.assertEqual(res.status_code, HTTPStatus.OK)
