from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Booking, TimeSlot


@login_required
def browse_slots(request):
    # 1. Get the date from the URL query string (?date=2026-08-14)
    raw_date = request.GET.get("date")
    if raw_date:
        try:
            selected_date = date.fromisoformat(raw_date)
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()

    # 2. Only unbooked slots, for that date, ordered so the table reads top-to-bottom by time
    slots = TimeSlot.objects.filter(
        date=selected_date,
        is_booked=False,
    ).order_by("start_time")

    return render(request, "bookings/player_home.html", {
        "slots": slots,
        "selected_date": selected_date,
    })


@login_required
@require_POST
def request_booking(request, slot_id):
    slot = get_object_or_404(TimeSlot, pk=slot_id)

    Booking.objects.create(
        player=request.user,
        slot=slot,
        status="pending",
    )

    messages.success(request, "Your booking request has been submitted.")
    return redirect("my_bookings")