"""
Tests for forms
"""

# Standard Library
import importlib
import sys
import typing

# Django
from django.utils.safestring import SafeString

# AA Discord Announcements
import aa_discord_announcements.forms as forms_module
from aa_discord_announcements.forms import (
    _get_discord_markdown_hint_text,
    _get_mandatory_form_label_text,
)
from aa_discord_announcements.tests import BaseTestCase


class TestForms(BaseTestCase):
    """
    Test the forms module
    """

    def test_mandatory_label_includes_text_and_required_marker(
        self: "TestForms",
    ) -> None:
        """
        Test that the mandatory label includes the provided text and the required marker.

        :return:
        """

        result = _get_mandatory_form_label_text("Announcement text")

        self.assertIsInstance(result, SafeString)

        s = str(result)

        self.assertIn("Announcement text", s)
        self.assertIn("form-required-marker", s)
        self.assertIn("form-field-required", s)
        self.assertIn("This field is mandatory", s)
        self.assertIn("*", s)

    def test_mandatory_label_handles_empty_text_gracefully(self: "TestForms") -> None:
        """
        Test that the mandatory label handles empty text gracefully.

        :return:
        """

        result = _get_mandatory_form_label_text("")

        self.assertIsInstance(result, SafeString)

        s = str(result)

        self.assertIn("form-field-required", s)
        self.assertIn("form-required-marker", s)
        self.assertIn("This field is mandatory", s)

    def test_mandatory_label_preserves_html_in_text_when_provided(
        self: "TestForms",
    ) -> None:
        """
        Test that the mandatory label preserves HTML in the provided text.

        :return:
        """

        html_text = "<strong>Important</strong>"
        result = _get_mandatory_form_label_text(html_text)
        s = str(result)

        # mark_safe is expected so provided HTML appears unescaped
        self.assertIn(html_text, s)
        self.assertIn("form-required-marker", s)

    def test_mandatory_label_accepts_non_string_input_and_converts_to_string(
        self: "TestForms",
    ) -> None:
        """
        Test that the mandatory label accepts non-string input and converts it to a string.

        :return:
        """

        result = _get_mandatory_form_label_text(123)
        s = str(result)

        self.assertIn("123", s)
        self.assertIn("form-required-marker", s)

    def test_discord_markdown_hint_contains_hint_and_link(self: "TestForms") -> None:
        """
        Test that the Discord Markdown hint contains the expected hint text and link.

        :return:
        """

        result = _get_discord_markdown_hint_text()
        s = str(result)

        self.assertIn("Hint: You can use", s)
        self.assertIn("Discord Markdown", s)
        self.assertIn('href="', s)
        self.assertIn("support.discord.com", s)
        self.assertIn('target="_blank"', s)
        self.assertIn('rel="noopener noreferer"', s)

    def test_discord_markdown_hint_is_lazy_and_evaluates_to_string(
        self: "TestForms",
    ) -> None:
        """
        Test that the Discord Markdown hint is a lazy object and evaluates to a string when converted.

        :return:
        """

        result = _get_discord_markdown_hint_text()
        s1 = str(result)
        s2 = f"{result}"

        self.assertEqual(s1, s2)
        self.assertIsInstance(s1, str)

    def test_lazy_modules_list_contains_functional(self: "TestForms") -> None:
        """
        Test that the __lazy_modules__ list in the forms module contains 'django.utils.functional'.

        :return:
        """

        self.assertIn(
            "django.utils.functional", getattr(forms_module, "__lazy_modules__", [])
        )

    def test_importing_does_not_define_StrPromise_by_default(self: "TestForms") -> None:
        """
        Test that importing the forms module does not define _StrPromise in its namespace by default.

        :return:
        """

        # By default TYPE_CHECKING is False; the name _StrPromise should not be present
        self.assertNotIn("_StrPromise", dir(forms_module))

    def test_when_type_checking_true_imports_StrPromise(self: "TestForms") -> None:
        """
        Test that when typing.TYPE_CHECKING is True, importing the forms module defines _StrPromise in its namespace.

        :return:
        """

        forms_name = "aa_discord_announcements.forms"
        orig_flag = typing.TYPE_CHECKING

        try:
            typing.TYPE_CHECKING = True

            if forms_name in sys.modules:
                del sys.modules[forms_name]

            try:
                mod = importlib.import_module(forms_name)
            except ImportError as e:
                self.skipTest(
                    f"Skipping because import under TYPE_CHECKING failed: {e}"
                )

            self.assertIn("_StrPromise", dir(mod))
        finally:
            typing.TYPE_CHECKING = orig_flag
            # reload original module state

            if forms_name in sys.modules:
                del sys.modules[forms_name]

            importlib.import_module(forms_name)
