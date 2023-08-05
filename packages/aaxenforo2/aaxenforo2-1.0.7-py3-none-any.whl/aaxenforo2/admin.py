from django.contrib import admin

from allianceauth.services.admin import ServicesUserAdmin

from .models import AAXenForo2User


@admin.register(AAXenForo2User)
class Xenforo2UserAdmin(ServicesUserAdmin):
    list_display = ServicesUserAdmin.list_display + ("username",)
    search_fields = ServicesUserAdmin.search_fields + ("username",)
