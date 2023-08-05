import logging

from django.template.loader import render_to_string

from allianceauth import hooks
from allianceauth.services.hooks import ServicesHook

from .tasks import AAXenforo2Tasks
from .urls import urlpatterns

logger = logging.getLogger(__name__)


class AAXenforo2Service(ServicesHook):
    def __init__(self):
        ServicesHook.__init__(self)
        self.name = "aaxenforo2"
        self.urlpatterns = urlpatterns
        self.access_perm = "aaxenforo2.access_xenforo2"
        self.name_format = "[{corp_ticker}] {character_name}"

    @property
    def title(self):
        return "XenForo 2 Forums"

    def delete_user(self, user, notify_user=False):
        logger.debug(f"Deleting user {user} {self.name} account")
        return AAXenforo2Tasks.delete_user(user, notify_user=notify_user)

    def validate_user(self, user):
        logger.debug(f"Validating user {user} {self.name} account")
        if AAXenforo2Tasks.has_account(user) and not self.service_active_for_user(user):
            self.delete_user(user, notify_user=True)

    def service_active_for_user(self, user):
        return user.has_perm(self.access_perm)

    def render_services_ctrl(self, request):
        urls = self.Urls()
        urls.auth_activate = "aaxenforo2:activate"
        urls.auth_deactivate = "aaxenforo2:deactivate"
        urls.auth_reset_password = "aaxenforo2:reset_password"
        urls.auth_set_password = "aaxenforo2:set_password"
        return render_to_string(
            self.service_ctrl_template,
            {
                "service_name": self.title,
                "urls": urls,
                "service_url": "",
                "username": request.user.aaxenforo2.username
                if AAXenforo2Tasks.has_account(request.user)
                else "",
            },
            request=request,
        )


@hooks.register("services_hook")
def register_service():
    return AAXenforo2Service()
