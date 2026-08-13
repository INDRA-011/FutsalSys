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
    """
    Show all bookings for the manager.

    - Includes pending, approved, and rejected bookings.
    - Newest bookings are shown first.
    - Optional status filtering is supported.
    """

    status = request.GET.get("status")

    bookings = Booking.objects.select_related(
        "player",
        "slot",
        "slot__court"
    ).order_by("-created_at")

    if status in [
        Booking.Status.PENDING,
        Booking.Status.APPROVED,
        Booking.Status.REJECTED,
    ]:
        bookings = bookings.filter(status=status)

    return render(
        request,
        "bookings/all_bookings.html",
        {
            "bookings": bookings,
            "selected_status": status,
        }
    )