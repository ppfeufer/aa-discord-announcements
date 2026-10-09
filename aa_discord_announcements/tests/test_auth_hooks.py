"""
Test auth_hooks
"""

# Standard Library
import importlib
import sys
import typing
from http import HTTPStatus

# Django
from django.urls import reverse

# AA Discord Announcements
from aa_discord_announcements.tests import BaseTestCase
from aa_discord_announcements.tests.utils import create_fake_user


class TestHooks(BaseTestCase):
    """
    Test the app hook into allianceauth
    """

    @classmethod
    def setUpClass(cls: "TestHooks") -> None:
        """
        Set up groups and users
        """

        super().setUpClass()

        # User cannot access
        cls.user_1001 = create_fake_user(
            character_id=1001, character_name="Peter Parker"
        )

        # User can access
        cls.user_1002 = create_fake_user(
            character_id=1002,
            character_name="Bruce Wayne",
            permissions=["aa_discord_announcements.basic_access"],
        )

        cls.html_menu = f"""
            <li class="d-flex flex-wrap m-2 p-2 pt-0 pb-0 mt-0 mb-0 me-0 pe-0">
                <i class="nav-link fa-regular fa-bell fa-fw align-self-center me-3 "></i>
                <a class="nav-link flex-fill align-self-center me-auto" href="{reverse('aa_discord_announcements:index')}">
                    Discord Announcements
                </a>
            </li>
        """

    def test_render_hook_success(self: "TestHooks") -> None:
        """
        Test should show the link to the app in the navigation to user with access
        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_1002)

        response = self.client.get(path=reverse(viewname="authentication:dashboard"))

        self.assertEqual(first=response.status_code, second=HTTPStatus.OK)
        self.assertContains(response=response, text=self.html_menu, html=True)

    def test_render_hook_fail(self: "TestHooks") -> None:
        """
        Test should not show the link to the app in the
        navigation to user without access
        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_1001)

        response = self.client.get(path=reverse(viewname="authentication:dashboard"))

        self.assertEqual(first=response.status_code, second=HTTPStatus.OK)
        self.assertNotContains(response=response, text=self.html_menu, html=True)

    def test_type_checking_block_imports_wsgi_request_when_enabled(
        self: "TestHooks",
    ) -> None:
        """
        Ensure that when typing.TYPE_CHECKING is True at import time the
        module-level name `WSGIRequest` is present in the `auth_hooks`
        module namespace.

        :return:
        """

        module_name = "aa_discord_announcements.auth_hooks"
        orig_module = sys.modules.get(module_name)
        orig_flag = typing.TYPE_CHECKING

        try:
            # Ensure django is available for this check, otherwise skip.
            try:
                # Django
                import django.core.handlers.wsgi  # noqa: F401
            except Exception:
                self.skipTest("Django WSGIRequest unavailable in this environment")

            if module_name in sys.modules:
                del sys.modules[module_name]

            typing.TYPE_CHECKING = True
            mod = importlib.import_module(module_name)

            self.assertTrue(hasattr(mod, "WSGIRequest"))
        finally:
            typing.TYPE_CHECKING = orig_flag
            if orig_module is not None:
                sys.modules[module_name] = orig_module
            else:
                sys.modules.pop(module_name, None)

    def test_type_checking_block_does_not_import_wsgi_request_when_disabled(
        self: "TestHooks",
    ) -> None:
        """
        Ensure that when typing.TYPE_CHECKING is False at import time the
        module-level name `WSGIRequest` is not present in the `auth_hooks`
        module namespace.

        :return:
        """

        module_name = "aa_discord_announcements.auth_hooks"
        orig_module = sys.modules.get(module_name)
        orig_flag = typing.TYPE_CHECKING

        try:
            if module_name in sys.modules:
                del sys.modules[module_name]

            typing.TYPE_CHECKING = False
            mod = importlib.import_module(module_name)

            self.assertFalse(hasattr(mod, "WSGIRequest"))
        finally:
            typing.TYPE_CHECKING = orig_flag
            if orig_module is not None:
                sys.modules[module_name] = orig_module
            else:
                sys.modules.pop(module_name, None)
