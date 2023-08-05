from unittest import mock

from django import urls
from django.contrib.auth.models import Group, Permission, User
from django.core.exceptions import ObjectDoesNotExist
from django.test import RequestFactory, TestCase

from allianceauth.tests.auth_utils import AuthUtils

from .auth_hooks import AAXenforo2Service
from .models import AAXenForo2User
from .tasks import AAXenforo2Tasks

MODULE_PATH = "aaxenforo2"
DEFAULT_AUTH_GROUP = "Member"


def add_permissions():
    permission = Permission.objects.get(codename="access_xenforo2")
    members = Group.objects.get_or_create(name=DEFAULT_AUTH_GROUP)[0]
    AuthUtils.add_permissions_to_groups([permission], [members])


class AAXenforo2HooksTestCase(TestCase):
    def setUp(self):
        self.member = "member_user"
        member = AuthUtils.create_member(self.member)
        AAXenForo2User.objects.create(user=member, username=self.member, remote_user=2)

        self.none_user = "none_user"
        AuthUtils.create_user(self.none_user)

        self.service = AAXenforo2Service
        add_permissions()

    def test_has_account(self):
        member = User.objects.get(username=self.member)
        none_user = User.objects.get(username=self.none_user)
        self.assertTrue(AAXenforo2Tasks.has_account(member))
        self.assertFalse(AAXenforo2Tasks.has_account(none_user))

    def test_service_enabled(self):
        service = self.service()
        member = User.objects.get(username=self.member)
        none_user = User.objects.get(username=self.none_user)

        self.assertTrue(service.service_active_for_user(member))
        self.assertFalse(service.service_active_for_user(none_user))

    @mock.patch(MODULE_PATH + ".tasks.AAXenForo2Manager")
    def test_validate_user(self, manager):
        service = self.service()
        # Test member is not deleted
        member = User.objects.get(username=self.member)
        manager.disable_user.return_value = 200

        service.validate_user(member)
        self.assertTrue(member.aaxenforo2)

        # Test none user is deleted
        none_user = User.objects.get(username=self.none_user)
        AAXenForo2User.objects.create(user=none_user, username="abc123", remote_user=2)
        service.validate_user(none_user)
        self.assertTrue(manager.disable_user.called)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username=self.none_user).aaxenforo2

    @mock.patch(MODULE_PATH + ".tasks.AAXenForo2Manager")
    def test_delete_user(self, manager):
        member = User.objects.get(username=self.member)
        manager.disable_user.return_value = 200
        service = self.service()

        result = service.delete_user(member)

        self.assertTrue(result)
        self.assertTrue(manager.disable_user.called)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username=self.member).aaxenforo2

    def test_render_services_ctrl(self):
        service = self.service()
        member = User.objects.get(username=self.member)
        request = RequestFactory().get("/en/services/")
        request.user = member

        response = service.render_services_ctrl(request)
        self.assertTemplateUsed(service.service_ctrl_template)
        self.assertIn(urls.reverse("aaxenforo2:deactivate"), response)
        self.assertIn(urls.reverse("aaxenforo2:reset_password"), response)
        self.assertIn(urls.reverse("aaxenforo2:set_password"), response)

        # Test register becomes available
        member.aaxenforo2.delete()
        member = User.objects.get(username=self.member)
        request.user = member
        response = service.render_services_ctrl(request)
        self.assertIn(urls.reverse("aaxenforo2:activate"), response)


class AAXenforo2ViewsTestCase(TestCase):
    def setUp(self):
        self.member = AuthUtils.create_member("auth_member")
        self.member.email = "auth_member@example.com"
        self.member.save()
        AuthUtils.add_main_character(
            self.member,
            "auth_member",
            "12345",
            corp_id="111",
            corp_name="Test Corporation",
        )
        add_permissions()

    def login(self):
        self.client.force_login(self.member)

    @mock.patch(MODULE_PATH + ".tasks.AAXenForo2Manager")
    @mock.patch(MODULE_PATH + ".views.AAXenForo2Manager")
    def test_activate(self, manager, tasks_manager):
        self.login()
        expected_username = "auth_member"
        manager.add_user.return_value = {
            "response": {"status_code": 200},
            "password": "hunter2",
            "username": expected_username,
            "user_id": 2,
        }

        response = self.client.get(urls.reverse("aaxenforo2:activate"))

        self.assertTrue(manager.add_user.called)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("services/service_credentials.html")
        self.assertContains(response, expected_username)
        xenforo2_user2 = AAXenForo2User.objects.get(user=self.member)
        self.assertEqual(xenforo2_user2.username, expected_username)

    @mock.patch(MODULE_PATH + ".tasks.AAXenForo2Manager")
    def test_deactivate(self, manager):
        self.login()
        AAXenForo2User.objects.create(
            user=self.member, username="some member", remote_user=2
        )

        manager.disable_user.return_value = 200

        response = self.client.get(urls.reverse("aaxenforo2:deactivate"))

        self.assertTrue(manager.disable_user.called)
        self.assertRedirects(
            response,
            expected_url=urls.reverse("services:services"),
            target_status_code=200,
        )
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=self.member.pk).aaxenforo2

    @mock.patch(MODULE_PATH + ".views.AAXenForo2Manager")
    def test_set_password(self, manager):
        self.login()
        AAXenForo2User.objects.create(
            user=self.member, username="some member", remote_user=2
        )

        manager.update_user_password.return_value = {
            "response": {"status_code": 200, "message": "ok"},
            "username": "some member",
        }

        response = self.client.post(
            urls.reverse("aaxenforo2:set_password"), data={"password": "1234asdf"}
        )

        self.assertTrue(manager.update_user_password.called)
        args, _ = manager.update_user_password.call_args
        self.assertEqual(args[1], "1234asdf")
        self.assertRedirects(
            response,
            expected_url=urls.reverse("services:services"),
            target_status_code=200,
        )

    @mock.patch(MODULE_PATH + ".views.AAXenForo2Manager")
    def test_reset_password(self, manager):
        self.login()
        AAXenForo2User.objects.create(
            user=self.member, username="some member", remote_user=2
        )

        manager.reset_password.return_value = {
            "response": {"status_code": 200, "message": "ok"},
            "password": "hunter2",
        }

        response = self.client.get(urls.reverse("aaxenforo2:reset_password"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/service_credentials.html")
        self.assertContains(response, "some member")
        self.assertContains(response, "hunter2")


class AAXenforo2ManagerTestCase(TestCase):
    def setUp(self):
        from .manager import AAXenForo2Manager

        self.manager = AAXenForo2Manager

    def test_generate_password(self):
        password = self.manager._AAXenForo2Manager__generate_password()

        self.assertEqual(len(password), 12)
        self.assertIsInstance(password, str)
