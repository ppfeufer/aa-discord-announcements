"""
The models
"""

# Django
from django.db import models


class General(models.Model):
    """
    Meta model for app permissions
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        General :: Meta
        """

        managed = False
        default_permissions = ()
        permissions = (("basic_access", "Can access this app"),)
