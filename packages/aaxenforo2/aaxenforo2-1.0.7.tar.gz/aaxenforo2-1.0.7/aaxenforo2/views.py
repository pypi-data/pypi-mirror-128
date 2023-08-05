import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from allianceauth.services.forms import ServicePasswordForm

from .manager import AAXenForo2Manager
from .models import AAXenForo2User
from .tasks import AAXenforo2Tasks

logger = logging.getLogger(__name__)

ACCESS_PERM = "aaxenforo2.access_xenforo2"


@login_required
@permission_required(ACCESS_PERM)
def activate_xenforo2_forum(request):
    logger.debug(f"activate_xenforo2_forum called by user {request.user}")
    character = request.user.profile.main_character
    logger.debug(
        f"Adding XenForo2 user for user {request.user} with main character {character}"
    )
    result = AAXenForo2Manager.add_user(request)
    # Based on XenAPI's response codes
    if result["response"]["status_code"] == 200:
        AAXenForo2User.objects.update_or_create(
            user=request.user,
            defaults={"username": result["username"], "remote_user": result["user_id"]},
        )

        logger.info(
            f"Updated user {request.user} with XenForo2 credentials. Updating groups."
        )
        messages.success(request, _("Activated XenForo2 account."))
        credentials = {
            "username": result["username"],
            "password": result["password"],
        }
        return render(
            request,
            "services/service_credentials.html",
            context={"credentials": credentials, "service": "XenForo2"},
        )

    else:
        logger.error(
            f"Unsuccessful attempt to activate xenforo2 for user {request.user}"
        )
        messages.error(
            request, _("An error occurred while processing your XenForo2 account.")
        )
    return redirect("services:services")


@login_required
@permission_required(ACCESS_PERM)
def deactivate_xenforo2_forum(request):
    logger.debug(f"deactivate_xenforo2_forum called by user {request.user}")
    if AAXenforo2Tasks.delete_user(request.user):
        logger.info(f"Successfully deactivated XenForo2 for user {request.user}")
        messages.success(request, _("Deactivated XenForo2 account."))
    else:
        messages.error(
            request, _("An error occurred while processing your XenForo2 account.")
        )
    return redirect("services:services")


@login_required
@permission_required(ACCESS_PERM)
def reset_xenforo2_password(request):
    logger.debug(f"reset_xenforo2_password called by user {request.user}")
    if AAXenforo2Tasks.has_account(request.user):
        result = AAXenForo2Manager.reset_password(request.user.aaxenforo2)
        # Based on XenAPI's response codes
        if result["response"]["status_code"] == 200:
            logger.info(f"Successfully reset XenForo2 password for user {request.user}")
            messages.success(request, _("Reset XenForo2 account password."))
            credentials = {
                "username": request.user.aaxenforo2.username,
                "password": result["password"],
            }
            return render(
                request,
                "services/service_credentials.html",
                context={"credentials": credentials, "service": "XenForo2"},
            )
    logger.error(
        f"Unsuccessful attempt to reset XenForo2 password for user {request.user}"
    )
    messages.error(
        request, _("An error occurred while processing your XenForo2 account.")
    )
    return redirect("services:services")


@login_required
@permission_required(ACCESS_PERM)
def set_xenforo2_password(request):
    logger.debug(f"set_xenforo2_password called by user {request.user}")
    if request.method == "POST":
        logger.debug("Received POST request with form.")
        form = ServicePasswordForm(request.POST)
        logger.debug(f"Form is valid: {form.is_valid()}")
        if form.is_valid() and AAXenforo2Tasks.has_account(request.user):
            password = form.cleaned_data["password"]
            logger.debug(f"Form contains password of length {len(password)}")
            result = AAXenForo2Manager.update_user_password(
                request.user.aaxenforo2, password
            )

            if result["response"]["status_code"] == 200:
                logger.info(
                    f"Successfully reset XenForo2 password for user {request.user}"
                )
                messages.success(request, _("Changed XenForo2 password."))
            else:
                status_code = result["response"]["status_code"]
                message = result["response"]["message"]
                logger.error(
                    f"Failed to install custom XenForo2 password for user {request.user}: {status_code} {message}"
                )
                messages.error(
                    request,
                    _("An error occurred while processing your XenForo2 account."),
                )
            return redirect("services:services")
    else:
        logger.debug("Request is not type POST - providing empty form.")
        form = ServicePasswordForm()

    logger.debug(f"Rendering form for user {request.user}")
    context = {"form": form, "service": "Forum"}
    return render(request, "services/service_password.html", context=context)
