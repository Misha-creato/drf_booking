from django.contrib import admin

from solo.admin import SingletonModelAdmin

from bookings.models import (
    BookingSettings,
)


@admin.register(BookingSettings)
class BookingSettingsAdmin(SingletonModelAdmin):
    pass
