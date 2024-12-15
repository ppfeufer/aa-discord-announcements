"""
Handling Discord webhooks
"""

# Third Party
from dhooks_lite import UserAgent, Webhook

# Django
from django.contrib.auth.models import User
from django.utils import dateformat, timezone

# AA Discord Announcements
from aa_discord_announcements import __version__
from aa_discord_announcements.constants import APP_NAME, GITHUB_URL
from aa_discord_announcements.helper.announcement_context import (
    get_webhook_announcement_context,
)


def get_user_agent() -> UserAgent:
    """
    Set the user agent

    :return: User agent
    :rtype: UserAgent
    """

    return UserAgent(APP_NAME, GITHUB_URL, __version__)


def send_to_discord_webhook(announcement_context: dict, user: User) -> None:
    """
    Send the announcement to a Discord webhook

    :param announcement_context: Announcement context
    :type announcement_context: dict
    :param user: User sending the announcement
    :type user: User
    :return:
    :rtype: None
    """

    discord_webhook = Webhook(
        url=announcement_context["announcement_channel"]["webhook"],
        user_agent=get_user_agent(),
    )
    webhook_announcement_context = get_webhook_announcement_context(
        announcement_context=announcement_context
    )
    message_body = webhook_announcement_context["content"]
    author_eve_name = user.profile.main_character.character_name

    message_footer = (
        f"_Sent by {author_eve_name} "
        f"@ {dateformat.format(value=timezone.now(), format_string='Y-m-d H:i')} (Eve Time)_"
    )
    message_to_send = f"{message_body}\n\n{message_footer}"

    discord_webhook.execute(
        content=message_to_send,
        wait_for_response=True,
    )
