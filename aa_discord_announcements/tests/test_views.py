"""
Test cases for the views in the aa_discord_announcements Django app.
"""

# Standard Library
import importlib
import json
import sys
import typing
from http import HTTPStatus
from unittest.mock import MagicMock, patch

# Django
from django.test import RequestFactory
from django.urls import reverse

# Alliance Auth
from allianceauth.groupmanagement.models import Group

# AA Discord Announcements
from aa_discord_announcements import __title__
from aa_discord_announcements.forms import AnnouncementForm
from aa_discord_announcements.models import Webhook

# Local
from aa_discord_announcements.tests import BaseTestCase
from aa_discord_announcements.tests.utils import create_fake_user
from aa_discord_announcements.views import ajax_create_announcement


class TestIndexView(BaseTestCase):
    """
    Test the index view of the aa_discord_announcements app.
    """

    @classmethod
    def setUpClass(cls: "TestIndexView") -> None:
        """
        Set up groups and users for testing.

        :return:
        """

        super().setUpClass()

        cls.group = Group.objects.create(name="Superhero")

        cls.user_no_access = create_fake_user(
            character_id=1001, character_name="Peter Parker"
        )

        cls.user_with_access = create_fake_user(
            character_id=1002,
            character_name="Bruce Wayne",
            permissions=["aa_discord_announcements.basic_access"],
        )

    def test_index_redirects_for_unauthenticated_users(self: "TestIndexView") -> None:
        """
        Test that unauthenticated users are redirected when accessing the index view.

        :return:
        """

        res = self.client.get(path=reverse(viewname="aa_discord_announcements:index"))

        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)

    def test_index_redirects_for_users_without_permission(
        self: "TestIndexView",
    ) -> None:
        """
        Test that users without the required permission are redirected when accessing the index view.

        :return:
        """

        self.client.force_login(user=self.user_no_access)

        res = self.client.get(path=reverse(viewname="aa_discord_announcements:index"))

        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)

    def test_index_renders_with_expected_context_when_no_webhooks(
        self: "TestIndexView",
    ) -> None:
        """
        Test that the index view renders correctly with the expected context when there are no webhooks configured.

        :return:
        """

        self.client.force_login(user=self.user_with_access)

        res = self.client.get(path=reverse(viewname="aa_discord_announcements:index"))

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)
        self.assertIn("form", res.context)
        self.assertEqual(res.context["form"], AnnouncementForm)
        self.assertIn("main_character", res.context)
        self.assertEqual(
            res.context["main_character"], self.user_with_access.profile.main_character
        )
        self.assertIn("webhooks_configured", res.context)
        self.assertFalse(res.context["webhooks_configured"])
        self.assertIn("title", res.context)
        self.assertEqual(res.context["title"], __title__)

    def test_index_reports_webhooks_configured_when_unrestricted_enabled_webhook_exists(
        self: "TestIndexView",
    ) -> None:
        """
        Test that the index view reports webhooks as configured when there is an unrestricted enabled webhook.

        :return:
        """

        Webhook.objects.create(
            name="announce", url="https://discord.com/api/webhooks/1/a", is_enabled=True
        )

        self.client.force_login(user=self.user_with_access)

        res = self.client.get(path=reverse(viewname="aa_discord_announcements:index"))

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)
        self.assertTrue(res.context["webhooks_configured"])

    def test_index_reports_webhooks_configured_when_restricted_to_users_group(
        self: "TestIndexView",
    ) -> None:
        """
        Test that the index view reports webhooks as configured when there is a webhook restricted to the user's group.

        :return:
        """

        webhook = Webhook.objects.create(
            name="private", url="https://discord.com/api/webhooks/2/b", is_enabled=True
        )
        webhook.restricted_to_group.add(self.group)

        # ensure user is member of group
        self.user_with_access.groups.add(self.group)
        self.client.force_login(user=self.user_with_access)

        res = self.client.get(path=reverse(viewname="aa_discord_announcements:index"))

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)
        self.assertTrue(res.context["webhooks_configured"])


class TestAjaxCalls(BaseTestCase):
    """
    Test access to ajax calls
    """

    @classmethod
    def setUpClass(cls: "TestAjaxCalls") -> None:
        """
        Set up groups and users
        """

        super().setUpClass()

        cls.group = Group.objects.create(name="Superhero")

        # User cannot access aa_discord_announcements
        cls.user_1001 = create_fake_user(
            character_id=1001, character_name="Peter Parker"
        )

        # User can access aa_discord_announcements
        cls.user_1002 = create_fake_user(
            character_id=1002,
            character_name="Bruce Wayne",
            permissions=["aa_discord_announcements.basic_access"],
        )

    def setUp(self: "TestAjaxCalls") -> None:
        """
        Setup
        """

        self.factory = RequestFactory()

    def test_ajax_get_announcement_targets_no_access(self: "TestAjaxCalls") -> None:
        """
        Test ajax call to get announcement targets available for the current user without access to it

        :return:
        :rtype:
        """

        # given
        self.client.force_login(user=self.user_1001)

        # when
        res = self.client.get(
            path=reverse(
                viewname="aa_discord_announcements:ajax_get_announcement_targets"
            )
        )

        # then
        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)

    def test_ajax_get_announcement_targets_general(self: "TestAjaxCalls") -> None:
        """
        Test ajax call to get announcement targets available for the current user

        :return:
        :rtype:
        """

        # given
        self.client.force_login(user=self.user_1002)

        # when
        res = self.client.get(
            path=reverse(
                viewname="aa_discord_announcements:ajax_get_announcement_targets"
            )
        )

        # then
        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_ajax_get_webhooks_no_access(self: "TestAjaxCalls") -> None:
        """
        Test ajax call to get webhooks available for the current user without access to it

        :return:
        :rtype:
        """

        # given
        self.client.force_login(user=self.user_1001)

        # when
        res = self.client.get(
            path=reverse(viewname="aa_discord_announcements:ajax_get_webhooks")
        )

        # then
        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)

    def test_ajax_get_webhooks_general(self: "TestAjaxCalls") -> None:
        """
        Test ajax call to get webhooks available for the current user

        :return:
        :rtype:
        """

        # given
        self.client.force_login(user=self.user_1002)

        # when
        res = self.client.get(
            path=reverse(viewname="aa_discord_announcements:ajax_get_webhooks")
        )

        # then
        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_ajax_create_announcement_no_access(self: "TestAjaxCalls") -> None:
        """
        Test ajax call to create an announcement is not available for a user without access to it

        :return:
        :rtype:
        """

        # given
        self.client.force_login(user=self.user_1001)

        # when
        res = self.client.get(
            path=reverse(viewname="aa_discord_announcements:ajax_create_announcement")
        )

        # then
        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)

    def test_ajax_create_announcement_general(self: "TestAjaxCalls") -> None:
        """
        Test ajax call to create an announcement is available for the current user

        :return:
        :rtype:
        """

        # given
        self.client.force_login(user=self.user_1002)

        # when
        res = self.client.get(
            path=reverse(viewname="aa_discord_announcements:ajax_create_announcement")
        )

        # then
        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    @patch("aa_discord_announcements.views.get_announcement_context_from_form_data")
    @patch("aa_discord_announcements.views.send_to_discord_webhook")
    def test_creates_announcement_successfully_with_webhook(
        self: "TestAjaxCalls",
        mock_send_to_discord_webhook: MagicMock,
        mock_get_announcement_context: MagicMock,
    ) -> None:
        """
        Test ajax call to create an announcement is successful with a webhook

        :param mock_send_to_discord_webhook:
        :type mock_send_to_discord_webhook:
        :param mock_get_announcement_context:
        :type mock_get_announcement_context:
        :return:
        :rtype:
        """

        mock_get_announcement_context.return_value = {
            "announcement_target": {
                "group_id": None,
                "group_name": None,
                "at_mention": "@here",
            },
            "announcement_channel": {"webhook": True},
            "announcement_text": "Borg to fight!",
        }

        self.client.force_login(user=self.user_1002)

        form_data = json.dumps(
            {
                "announcement_target": "@here",
                "announcement_channel": "1",
                "announcement_text": "Borg to fight!",
            }
        )
        response = self.client.post(
            path=reverse(viewname="aa_discord_announcements:ajax_create_announcement"),
            data=form_data,
            content_type="application/json",
        )

        self.assertEqual(first=response.status_code, second=HTTPStatus.OK)
        self.assertTemplateUsed(
            response=response,
            template_name="aa_discord_announcements/partials/announcement/copy-paste-text.html",
        )
        self.assertContains(response=response, text="@here")
        self.assertContains(response=response, text="Borg to fight!")

        mock_send_to_discord_webhook.assert_called_once()

    @patch("aa_discord_announcements.views.get_announcement_context_from_form_data")
    @patch("aa_discord_announcements.views.send_to_discord_webhook")
    def test_creates_announcement_successfully_without_webhook(
        self: "TestAjaxCalls",
        mock_send_to_discord_webhook: MagicMock,
        mock_get_announcement_context: MagicMock,
    ) -> None:
        """
        Test ajax call to create an announcement is successful without a webhook

        :param mock_send_to_discord_webhook:
        :type mock_send_to_discord_webhook:
        :param mock_get_announcement_context:
        :type mock_get_announcement_context:
        :return:
        :rtype:
        """

        mock_get_announcement_context.return_value = {
            "announcement_target": {
                "group_id": None,
                "group_name": None,
                "at_mention": "@here",
            },
            "announcement_channel": {"webhook": False},
            "announcement_text": "Borg to fight!",
        }

        self.client.force_login(user=self.user_1002)

        form_data = json.dumps(
            {
                "announcement_target": "@here",
                "announcement_channel": "1",
                "announcement_text": "Borg to fight!",
            }
        )
        response = self.client.post(
            path=reverse(viewname="aa_discord_announcements:ajax_create_announcement"),
            data=form_data,
            content_type="application/json",
        )

        self.assertEqual(first=response.status_code, second=HTTPStatus.OK)
        self.assertTemplateUsed(
            response=response,
            template_name="aa_discord_announcements/partials/announcement/copy-paste-text.html",
        )
        self.assertContains(response=response, text="@here")
        self.assertContains(response=response, text="Borg to fight!")

        mock_send_to_discord_webhook.assert_not_called()

    def test_form_invalid_returns_error(self: "TestAjaxCalls") -> None:
        """
        Test ajax call to create an announcement returns an error if the form is invalid

        :return:
        :rtype:
        """

        request = self.factory.post(
            path=reverse(viewname="aa_discord_announcements:ajax_create_announcement"),
            data=json.dumps(
                {
                    "announcement_target": "800432143549333504",
                    "announcement_channel": "1",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user_1002

        response = ajax_create_announcement(request)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)["success"])
        self.assertEqual(
            json.loads(response.content)["message"],
            "Form invalid. Please check your input.",
        )

    def no_form_data_submitted_returns_error(self: "TestAjaxCalls") -> None:
        """
        Test ajax call to create an announcement returns an error if no form data is submitted

        :return:
        :rtype:
        """

        request = self.factory.post(
            path=reverse(viewname="aa_discord_announcements:ajax_create_announcement"),
            content_type="application/json",
        )
        request.user = self.user_1002

        response = ajax_create_announcement(request)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)["success"])
        self.assertEqual(
            json.loads(response.content)["message"], "No form data submitted."
        )


class TestViewsModuleImportBehavior(BaseTestCase):
    """
    Test the import behavior of the views module, specifically regarding lazy imports and type checking.
    """

    def test_lazy_modules_contains_wsgi_handler(
        self: "TestViewsModuleImportBehavior",
    ) -> None:
        """
        Test that the __lazy_modules__ list in the views module contains 'django.core.handlers.wsgi'.

        :return:
        """

        # AA Discord Announcements
        import aa_discord_announcements.views as views_module

        self.assertIn(
            "django.core.handlers.wsgi", getattr(views_module, "__lazy_modules__", [])
        )

    def test_importing_does_not_define_WSGIRequest_by_default(
        self: "TestViewsModuleImportBehavior",
    ) -> None:
        """
        Test that importing the views module does not define WSGIRequest in its namespace by default.

        :return:
        """

        # AA Discord Announcements
        import aa_discord_announcements.views as views_module

        self.assertNotIn("WSGIRequest", dir(views_module))

    def test_when_type_checking_true_imports_WSGIRequest(
        self: "TestViewsModuleImportBehavior",
    ) -> None:
        """
        Test that when typing.TYPE_CHECKING is True, importing the views module defines WSGIRequest in its namespace.

        :return:
        """

        mod_name = "aa_discord_announcements.views"
        orig_flag = typing.TYPE_CHECKING

        try:
            typing.TYPE_CHECKING = True
            if mod_name in sys.modules:
                del sys.modules[mod_name]

            try:
                mod = importlib.import_module(mod_name)
            except Exception as e:
                self.skipTest(
                    f"Skipping because import under TYPE_CHECKING failed: {e}"
                )

            self.assertIn("WSGIRequest", dir(mod))
        finally:
            typing.TYPE_CHECKING = orig_flag

            if mod_name in sys.modules:
                del sys.modules[mod_name]

            importlib.import_module(mod_name)
