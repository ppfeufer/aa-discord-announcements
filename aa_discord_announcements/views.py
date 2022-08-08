"""
The views
"""

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag
from app_utils.urls import site_absolute_url

# AA Discord Announcements
from aa_discord_announcements import __title__
from aa_discord_announcements.forms import AnnouncementForm
from aa_discord_announcements.models import PingTarget, Webhook

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@login_required
@permission_required("aa_discord_announcements.basic_access")
def index(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    """

    logger.info(f"Discord Announcements view called by user {request.user}")

    context = {
        "title": __title__,
        "webhooks_configured": Webhook.objects.filter(
            Q(restricted_to_group__in=request.user.groups.all())
            | Q(restricted_to_group__isnull=True),
            is_enabled=True,
        ).exists(),
        "site_url": site_absolute_url(),
        "main_character": request.user.profile.main_character,
        "form": AnnouncementForm,
    }

    return render(request, "aa_discord_announcements/index.html", context)


@login_required
@permission_required("aa_discord_announcements.basic_access")
def ajax_get_announcement_targets(request: WSGIRequest) -> HttpResponse:
    """
    Get announcement targets for the current user
    :param request:
    :return:
    """

    logger.info(f"Getting ping targets for user {request.user}")

    additional_discord_announcement_targets = (
        PingTarget.objects.filter(
            Q(restricted_to_group__in=request.user.groups.all())
            | Q(restricted_to_group__isnull=True),
            is_enabled=True,
        )
        .distinct()
        .order_by("name")
    )

    return render(
        request,
        "aa_discord_announcements/partials/form/segments/announcement-targets.html",
        {"announcement_targets": additional_discord_announcement_targets},
    )


@login_required
@permission_required("aa_discord_announcements.basic_access")
def ajax_get_webhooks(request: WSGIRequest) -> HttpResponse:
    """
    Get webhooks for ccurrent user
    :param request:
    :return:
    """

    logger.info(f"Getting webhooks for user {request.user}")

    webhooks = (
        Webhook.objects.filter(
            Q(restricted_to_group__in=request.user.groups.all())
            | Q(restricted_to_group__isnull=True),
            is_enabled=True,
        ).distinct()
        # .order_by("type", "name")
    )

    return render(
        request,
        "aa_discord_announcements/partials/form/segments/announcement-channel.html",
        {"webhooks": webhooks},
    )
