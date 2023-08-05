import json
import logging
import secrets
import string

import requests

from django.contrib.auth.models import User

from allianceauth.services.hooks import NameFormatter

from .app_settings import (
    AAXENFORO2_API_USER_ID,
    AAXENFORO2_APIKEY,
    AAXENFORO2_DEFAULT_GROUP,
    AAXENFORO2_ENDPOINT,
    AAXENFORO2_EXTRA_GROUP,
)
from .models import AAXenForo2User

logger = logging.getLogger(__name__)


def get_username(user):
    from .auth_hooks import AAXenforo2Service

    return NameFormatter(AAXenforo2Service(), user).format_name()


class AAXenForo2Manager:
    def __init__(self):
        if not AAXENFORO2_ENDPOINT:
            logger.debug("Could not find AAXenForo2 endpoint")
        if not AAXENFORO2_APIKEY:
            logger.debug("AAXenForo2 API Key not found")
        pass

    @staticmethod
    def __sanitize_username(username):
        sanitized = username.replace(" ", "_")
        return sanitized

    @staticmethod
    def __generate_password():
        return "".join(
            [secrets.choice(string.ascii_letters + string.digits) for i in range(12)]
        )

    @staticmethod
    def exec_http_request(route: str, http_params: dict):
        return requests.post(
            f"{AAXENFORO2_ENDPOINT}{route}",
            params=http_params,
            headers={
                "XF-Api-Key": AAXENFORO2_APIKEY,
                "XF-Api-User": AAXENFORO2_API_USER_ID,
            },
        )

    @staticmethod
    def add_user(request):

        user: User = request.user
        username: str = get_username(user)

        data = {
            "username": AAXenForo2Manager.__sanitize_username(username),
            "password": AAXenForo2Manager.__generate_password(),
            "email": user.email,
            "user_group_id": AAXENFORO2_DEFAULT_GROUP,
            "secondary_group_ids[]": AAXENFORO2_EXTRA_GROUP,
            "user_state": "valid",
            "is_staff": "0",
            "visible": "1",
        }

        r = AAXenForo2Manager.exec_http_request("api/users/", data)
        rdata: dict = json.loads(r.text)

        # check if the user already exist but was disabled
        if r.status_code != 200 or not rdata["success"]:
            if any(
                obj["code"] in ["email_addresses_must_be_unique"]
                for obj in rdata["errors"]
            ) and not any(
                obj["code"] in ["usernames_must_be_unique"] for obj in rdata["errors"]
            ):
                # log suspicious behaviour
                msg = f"Duplicate email address used for forum registration by user: [{user.id}] {user.email} ({username})"
                logger.error(msg)

                from django.contrib import messages

                messages.error(
                    request,
                    "Duplicate email address used for forum registration. Please try a different email address. "
                    "(Forums Service Error)",
                )

                raise Exception(msg)
            elif any(
                obj["code"] in ["usernames_must_be_unique"] for obj in rdata["errors"]
            ) and any(
                obj["code"] in ["email_addresses_must_be_unique"]
                for obj in rdata["errors"]
            ):
                # reactivate old account
                data = AAXenForo2Manager.reactivate_user(user.aaxenforo2)
                return data
            elif any(
                obj["code"] in ["usernames_must_be_unique"] for obj in rdata["errors"]
            ):
                # reactivate old account
                data = AAXenForo2Manager.reactivate_user(user.aaxenforo2)
                return data

        response = {
            "user_id": json.loads(r.text)["user"]["user_id"],
            "response": {"message": r.text, "status_code": r.status_code},
        }

        data.update(response)
        return data

    @staticmethod
    def reset_password(user: AAXenForo2User):

        data = {
            "password": AAXenForo2Manager.__generate_password(),
        }

        r = AAXenForo2Manager.exec_http_request(f"api/users/{user.remote_user}/", data)
        rdata = json.loads(r.text)

        # check if the request failed
        if r.status_code != 200 or not rdata["success"]:
            msg = "AAXenForo2 user account password reset failed for user: [{}] {} ({})".format(
                user.user.id, user.user.email, user.username
            )
            logger.error(msg)
            raise Exception(msg)

        response = {"response": {"message": r.text, "status_code": r.status_code}}
        data.update(response)
        return data

    @staticmethod
    def disable_user(user: AAXenForo2User):

        data = {
            "user_group_id": "1",
            "secondary_group_ids": "",
            "user_state": "disabled",
        }

        r = AAXenForo2Manager.exec_http_request(f"api/users/{user.remote_user}/", data)
        rdata = json.loads(r.text)

        # check if the request failed
        if r.status_code != 200 or not rdata["success"]:
            msg = "AAXenForo2 user deactivated for user: [{}] {} ({})".format(
                user.user.id, user.user.email, user.username
            )
            logger.error(msg)
            raise Exception(msg)

        return r

    @staticmethod
    def reactivate_user(user: AAXenForo2User):
        data = {
            "user_group_id": AAXENFORO2_DEFAULT_GROUP,
            "secondary_group_ids[]": AAXENFORO2_EXTRA_GROUP,
            "user_state": "valid",
        }

        r = AAXenForo2Manager.exec_http_request(f"api/users/{user.remote_user}/", data)
        rdata = json.loads(r.text)

        # check if the request failed
        if r.status_code != 200 or not rdata["success"]:
            msg = "AAXenForo2 user reactivated for user: [{}] {} ({})".format(
                user.user.id, user.user.email, user.username
            )
            logger.error(msg)
            raise Exception(msg)

        response = {
            "response": {"message": r.text, "status_code": r.status_code},
            "username": user.username,
        }
        data.update(response)
        return data

    @staticmethod
    def update_user_password(user: AAXenForo2User, raw_password):

        data = {
            "password": raw_password,
        }

        r = AAXenForo2Manager.exec_http_request(f"api/users/{user.remote_user}/", data)
        rdata = json.loads(r.text)

        # check if the request failed
        if r.status_code != 200 or not rdata["success"]:
            msg = "AAXenForo2 user account password update failed for user: [{}] {} ({})".format(
                user.user.id, user.user.email, user.username
            )
            logger.error(msg)
            raise Exception(msg)

        response = {
            "response": {"message": r.text, "status_code": r.status_code},
            "username": user.username,
        }
        data.update(response)
        return data
