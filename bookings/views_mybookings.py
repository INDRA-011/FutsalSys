"""
OWNER: feature/my-bookings
Only this file + templates/bookings/my_bookings.html belong to this branch.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Booking


@login_required
def my_bookings(request):
    bookings = (
        Booking.objects
        .filter(player=request.user)
        .select_related("slot", "slot__court")
        .order_by("-created_at")
    )
    return render(request, "bookings/my_bookings.html", {"bookings": bookings})


@login_required
@require_POST
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        pk=booking_id,
        player=request.user,
        status=Booking.Status.PENDING,
    )
    booking.delete()
    messages.info(request, "Your booking request has been cancelled.")
    return redirect("my_bookings")