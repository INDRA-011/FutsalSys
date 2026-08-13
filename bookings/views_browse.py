from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Booking, TimeSlot


@login_required
def browse_slots(request):
    """
    Display available futsal time slots.
    """

    slots = TimeSlot.objects.all().order_by("date", "start_time")

    return render(
        request,
        "bookings/browse_slots.html",
        {
            "slots": slots,
        },
    )


@login_required
def request_booking(request, slot_id):
    """
    Create a pending booking request.

    A player cannot create another request if:
    - the slot is already booked
    - they already have a pending request
    - they already have an approved booking
    """

    # Only POST requests are allowed
    if request.method != "POST":
        return redirect("browse_slots")

    # Get the requested time slot
    slot = get_object_or_404(TimeSlot, pk=slot_id)

    # -----------------------------------------
    # 1. Check whether slot is already booked
    # -----------------------------------------
    if slot.is_booked:
        messages.error(
            request,
            "This time slot has already been booked."
        )
        return redirect("browse_slots")

    # -----------------------------------------
    # 2. Check player's existing booking
    # -----------------------------------------
    existing_booking = Booking.objects.filter(
        player=request.user,
        slot=slot,
        status__in=[
            Booking.Status.PENDING,
            Booking.Status.APPROVED,
        ],
    ).first()

    if existing_booking:

        # Player already has a pending request
        if existing_booking.status == Booking.Status.PENDING:
            messages.warning(
                request,
                "You have already requested this time slot."
            )

        # Player already has an approved booking
        elif existing_booking.status == Booking.Status.APPROVED:
            messages.warning(
                request,
                "You already have an approved booking for this time slot."
            )

        return redirect("my_bookings")

    # -----------------------------------------
    # 3. Create a new pending booking
    # -----------------------------------------
    Booking.objects.create(
        player=request.user,
        slot=slot,
        status=Booking.Status.PENDING,
    )

    messages.success(
        request,
        "Your booking request has been submitted successfully."
    )

    return redirect("my_bookings")