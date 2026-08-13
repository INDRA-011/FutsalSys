"""
OWNER: feature/my-bookings
Player booking history and cancellation.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Booking


@login_required
def my_bookings(request):
    """
    Show all bookings belonging to the logged-in player.

    Includes:
    - Pending
    - Approved
    - Rejected
    """

    bookings = (
        Booking.objects
        .filter(player=request.user)
        .select_related(
            "slot",
            "slot__court",
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "bookings/my_booking.html",
        {
            "bookings": bookings,
        },
    )


@login_required
def cancel_booking(request, booking_id):
    """
    Cancel the player's own booking.

    Pending booking:
        Delete the booking.

    Approved booking:
        Delete the booking and reopen the slot.

    Rejected booking:
        Cannot be cancelled.

    Only POST requests are accepted.
    """

    if request.method != "POST":
        return redirect("my_bookings")

    booking = get_object_or_404(
        Booking,
        pk=booking_id,
        player=request.user,
    )

    # -----------------------------
    # PENDING
    # -----------------------------
    if booking.status == Booking.Status.PENDING:

        booking.delete()

        messages.success(
            request,
            "Your pending booking request has been cancelled.",
        )

        return redirect("my_bookings")

    # -----------------------------
    # APPROVED
    # -----------------------------
    if booking.status == Booking.Status.APPROVED:

        slot = booking.slot

        # Re-open the slot.
        slot.is_booked = False
        slot.save(update_fields=["is_booked"])

        # Remove the booking.
        booking.delete()

        messages.success(
            request,
            "Your approved booking has been cancelled. "
            "The time slot is now available again.",
        )

        return redirect("my_bookings")

    # -----------------------------
    # REJECTED
    # -----------------------------
    messages.error(
        request,
        "Rejected bookings cannot be cancelled.",
    )

    return redirect("my_bookings")