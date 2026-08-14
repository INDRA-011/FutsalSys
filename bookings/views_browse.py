"""
OWNER: feature/browse-slots
Only this file + templates/bookings/player_home.html belong to this branch.
"""
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Booking, Court, TimeSlot


@login_required
def browse_slots(request):
    raw_date = request.GET.get("date")
    if raw_date:
        try:
            selected_date = date.fromisoformat(raw_date)
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()

    # Each court gets its own list of that day's slots (court.day_slots),
    # including already-booked ones, so we can show "Booked" instead of hiding them.
    courts = Court.objects.prefetch_related(
        Prefetch(
            "slots",
            queryset=TimeSlot.objects.filter(date=selected_date).order_by("start_time"),
            to_attr="day_slots",
        )
    )

    return render(request, "bookings/player_home.html", {
        "courts": courts,
        "selected_date": selected_date,
    })


@login_required
@require_POST
def request_booking(request, slot_id):
    slot = get_object_or_404(TimeSlot, pk=slot_id)

    if slot.is_booked:
        messages.error(request, "Sorry, that slot was just booked by someone else.")
        return redirect("browse_slots")

    Booking.objects.create(
        player=request.user,
        slot=slot,
        status="pending",
    )

    messages.success(request, "Your booking request has been submitted.")
    return redirect("my_bookings")