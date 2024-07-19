from django.contrib import admin

from areas.forms import AreaAdminForm
from areas.models import (
    Area,
    Contact,
    Photo,
)


class ContactInline(admin.StackedInline):
    model = Contact
    extra = 1


class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 1


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    form = AreaAdminForm
    inlines = [
        ContactInline,
        PhotoInline,
    ]
    list_display = [
        'name',
        'available',
    ]
    list_filter = [
        'name',
        'available',
    ]
    search_fields = [
        'name',
    ]
