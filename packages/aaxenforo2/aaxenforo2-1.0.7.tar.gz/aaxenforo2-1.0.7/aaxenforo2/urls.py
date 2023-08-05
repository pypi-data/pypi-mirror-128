from django.conf.urls import include, url

from . import views

app_name = "aaxenforo2"

module_urls = [
    # XenForo2 service control
    url(r"^activate/$", views.activate_xenforo2_forum, name="activate"),
    url(r"^deactivate/$", views.deactivate_xenforo2_forum, name="deactivate"),
    url(r"^reset_password/$", views.reset_xenforo2_password, name="reset_password"),
    url(r"^set_password/$", views.set_xenforo2_password, name="set_password"),
]

urlpatterns = [
    url(r"^aaxenforo2/", include((module_urls, app_name), namespace=app_name)),
]
