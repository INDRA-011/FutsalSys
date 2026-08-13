"""
OWNER: feature/all-bookings-polish
Only this file + templates/bookings/all_bookings.html + static/css/style.css
belong to this branch.
"""
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from .models import Booking

is_manager = user_passes_test(lambda u: u.is_staff)


@is_manager
def all_bookings(request):
    bookings = (
        Booking.objects
        .select_related("slot", "slot__court", "player")
        .order_by("-created_at")
    )

    status = request.GET.get("status")
    valid_statuses = {choice for choice, _ in Booking.Status.choices}
    if status in valid_statuses:
        bookings = bookings.filter(status=status)

    return render(request, "bookings/all_bookings.html", {
        "bookings": bookings,
        "selected_status": status,
        "status_choices": Booking.Status.choices,
    })