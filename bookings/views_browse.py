"""
OWNER: feature/browse-slots
Only this file + templates/bookings/player_home.html belong to this branch.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import TimeSlot


@login_required
def browse_slots(request):
    """
    TODO:
    - Show a date picker (default = today) and list TimeSlots for that date
      where is_booked=False.
    - Each row needs a "Request Booking" button -> POST to request_booking.
    """
    slots = TimeSlot.objects.filter(is_booked=False)
    return render(request, "bookings/player_home.html", {"slots": slots})


@login_required
def request_booking(request, slot_id):
    """
    TODO:
    - Only accept POST.
    - Create Booking(player=request.user, slot=slot, status='pending').
    - Multiple players CAN request the same slot (no blocking).
    - Redirect to my_bookings with a success message.
    """
    slot = get_object_or_404(TimeSlot, pk=slot_id)
    return redirect("browse_slots")