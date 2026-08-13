"""
Manager dashboard views.

Manager access is restricted to Django staff users.
"""

from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Booking


def is_manager(user):
    return user.is_authenticated and user.is_staff


manager_required = user_passes_test(
    is_manager,
    login_url="login"
)


@manager_required
def manager_dashboard(request):
    """
    Display all pending booking requests.
    """

    pending = (
        Booking.objects
        .filter(status=Booking.Status.PENDING)
        .select_related(
            "player",
            "slot",
            "slot__court",
        )
        .order_by(
            "slot__date",
            "slot__start_time",
            "created_at",
        )
    )

    return render(
        request,
        "bookings/manager_dashboard.html",
        {
            "pending": pending,
        },
    )


@manager_required
def approve_booking(request, booking_id):
    """
    Approve a pending booking.

    When approved:
    - booking becomes approved
    - slot becomes booked
    - competing pending requests are rejected
    """

    if request.method != "POST":
        return redirect("manager_dashboard")

    booking = get_object_or_404(
        Booking,
        pk=booking_id,
        status=Booking.Status.PENDING,
    )

    if booking.slot.is_booked:
        messages.error(
            request,
            "This slot has already been booked."
        )
        return redirect("manager_dashboard")

    booking.approve()

    messages.success(
        request,
        f"Booking for {booking.player.username} "
        f"has been approved."
    )

    return redirect("manager_dashboard")


@manager_required
def reject_booking(request, booking_id):
    """
    Reject a pending booking.
    """

    if request.method != "POST":
        return redirect("manager_dashboard")

    booking = get_object_or_404(
        Booking,
        pk=booking_id,
        status=Booking.Status.PENDING,
    )

    booking.reject()

    messages.success(
        request,
        f"Booking for {booking.player.username} "
        f"has been rejected."
    )

    return redirect("manager_dashboard")