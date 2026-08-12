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
    TODO (optional/stretch):
    - Show every Booking regardless of status, newest first.
    - Optional: filter by status via a query param (?status=approved).
    """
    bookings = Booking.objects.all()
    return render(request, "bookings/all_bookings.html", {"bookings": bookings})