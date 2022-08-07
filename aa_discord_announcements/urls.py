"""
Pages url config
"""

# Django
from django.urls import path

# AA Discord Announcements
# AA Fleet Pings
from aa_discord_announcements import views

app_name: str = "aa_discord_announcements"

urlpatterns = [
    path("", views.index, name="index"),
    # Ajax calls
    # path(
    #     "ajax/get-ping-targets-for-user/",
    #     views.ajax_get_ping_targets,
    #     name="ajax_get_ping_targets",
    # ),
    # path(
    #     "ajax/get-webhooks-for-user/",
    #     views.ajax_get_webhooks,
    #     name="ajax_get_webhooks",
    # ),
    # path(
    #     "ajax/create-announcement/",
    #     views.ajax_create_announcement,
    #     name="ajax_create_announcement",
    # ),
]
