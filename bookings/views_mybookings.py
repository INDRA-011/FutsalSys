"""
OWNER: feature/my-bookings
Only this file + templates/bookings/my_bookings.html belong to this branch.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Booking


@login_required
def my_bookings(request):
    """
    TODO:
    - List request.user's own Booking objects, newest first.
    - Show a status badge (pending=yellow, approved=green, rejected=red).
    - Show a Cancel button only when status == 'pending'.
    """
    bookings = Booking.objects.filter(player=request.user)
    return render(request, "bookings/my_bookings.html", {"bookings": bookings})


@login_required
def cancel_booking(request, booking_id):
    """
    TODO:
    - Only allow the owning player to cancel, and only if status == 'pending'.
    - Delete the Booking row completely (hard delete, no 'cancelled' status).
    - Redirect back to my_bookings.
    """
    booking = get_object_or_404(Booking, pk=booking_id, player=request.user)
    return redirect("my_bookings")