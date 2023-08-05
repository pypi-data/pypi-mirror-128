import logging

from django.core.exceptions import ObjectDoesNotExist

from allianceauth.notifications import notify
from allianceauth.services.hooks import NameFormatter

from .manager import AAXenForo2Manager
from .models import AAXenForo2User

logger = logging.getLogger(__name__)


class AAXenforo2Tasks:
    def __init__(self):
        pass

    @classmethod
    def delete_user(cls, user, notify_user=False):
        if cls.has_account(user):
            logger.debug(
                f"User {user} has a XenForo2 account {user.aaxenforo2.username}. Deleting."
            )
            if AAXenForo2Manager.disable_user(user.aaxenforo2) == 200:
                user.aaxenforo2.delete()
                if notify_user:
                    notify(user, "XenForo2 Account Disabled", level="danger")
                return True
        return False

    @staticmethod
    def has_account(user):
        try:
            return user.aaxenforo2.username != ""
        except ObjectDoesNotExist:
            return False

    @classmethod
    def disable(cls):
        logger.debug("Deleting ALL XenForo2 users")
        AAXenForo2User.objects.all().delete()

    @staticmethod
    def get_username(user):
        from .auth_hooks import AAXenforo2Service

        return NameFormatter(AAXenforo2Service(), user).format_name()
