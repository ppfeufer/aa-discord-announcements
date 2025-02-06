"""
App Settings
"""

# Django
from django.apps import apps
from django.conf import settings


def discord_service_installed() -> bool:
    """
    Check if the Discord service is installed
    :return: bool
    """

    return apps.is_installed(app_name="allianceauth.services.modules.discord")


def debug_enabled() -> bool:
    """
    Check if DEBUG is enabled

    :return:
    :rtype:
    """

    return settings.DEBUG
