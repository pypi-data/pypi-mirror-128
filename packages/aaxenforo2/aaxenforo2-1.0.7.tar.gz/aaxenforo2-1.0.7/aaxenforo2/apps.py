from django.apps import AppConfig

from aaxenforo2 import __version__


class AAXenforo2ServiceConfig(AppConfig):
    name = "aaxenforo2"
    label = "aaxenforo2"
    verbose_name = f"AA XenForo 2.x Services Integration v{__version__}"
