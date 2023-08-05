from django.db import models


class AAXenForo2User(models.Model):
    user = models.OneToOneField(
        "auth.User",
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="aaxenforo2",
    )
    remote_user = models.BigIntegerField()
    username = models.CharField(max_length=254)

    def __str__(self):
        return self.username

    class Meta:
        permissions = (("access_xenforo2", "Can access the XenForo2 service"),)
