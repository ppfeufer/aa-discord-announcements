"""
The forms
"""

# Django
from django import forms
from django.utils.translation import gettext_lazy as _


class AnnouncementForm(forms.Form):
    """
    Announcement Form
    """

    announcement_target = forms.CharField(
        required=False,
        label=_("Announcement Target"),
        widget=forms.Select(choices={}),
        help_text=_("Who do you want to ping?"),
    )
    announcement_channel = forms.CharField(
        required=False,
        label=_("Announcement Channel"),
        widget=forms.Select(choices={}),
        help_text=_("Select a channel to send the announcement to automatically"),
    )
    announcement_text = forms.CharField(
        required=True,
        label=_("Announcement Text"),
        widget=forms.Textarea(
            attrs={
                "rows": 10,
                "cols": 20,
                "input_type": "textarea",
                "placeholder": _("Your announcement ...."),
            }
        ),
    )
