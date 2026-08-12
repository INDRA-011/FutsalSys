from django.contrib import admin
from .models import Court, TimeSlot, Booking


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ("name", "location")


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("court", "date", "start_time", "end_time", "is_booked")
    list_filter = ("court", "date", "is_booked")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("player", "slot", "status", "created_at")
    list_filter = ("status",)