"""
Hook into AA
"""

__lazy_modules__ = ["django.core.handlers.wsgi"]

# Standard Library
from typing import TYPE_CHECKING

# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

# AA Discord Announcements
from aa_discord_announcements import __title__, urls

if TYPE_CHECKING:
    # Django
    from django.core.handlers.wsgi import WSGIRequest


class AaDiscordAnnouncementsMenuItem(
    MenuItemHook
):  # pylint: disable=too-few-public-methods
    """
    This class ensures only authorized users will see the menu entry
    """

    def __init__(self: "AaDiscordAnnouncementsMenuItem"):
        """
        Initialize the menu item with the appropriate properties.
        """

        MenuItemHook.__init__(
            self,
            text=__title__,
            classes="fa-regular fa-bell",
            url_name="aa_discord_announcements:index",
            navactive=["aa_discord_announcements:"],
        )

    def render(self: "AaDiscordAnnouncementsMenuItem", request: "WSGIRequest"):
        """
        Render the menu item if the user has the required permission.

        :param request: The WSGI request object containing user information.
        :return: The rendered menu item or an empty string if the user lacks permission.
        """

        return (
            MenuItemHook.render(self, request=request)
            if request.user.has_perm(perm="aa_discord_announcements.basic_access")
            else ""
        )


@hooks.register("menu_item_hook")
def register_menu():
    """
    Register our menu item

    :return: The menu item hook instance.
    """

    return AaDiscordAnnouncementsMenuItem()


@hooks.register("url_hook")
def register_urls():
    """
    Register our base url

    :return: The URL hook instance.
    """

    return UrlHook(
        urls=urls,
        namespace="aa_discord_announcements",
        base_url=r"^discord-announcements/",
    )
