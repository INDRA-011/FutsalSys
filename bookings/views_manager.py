"""
OWNER: feature/manager-dashboard
Only this file + templates/bookings/manager_dashboard.html belong to this branch.
"""
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Booking

is_manager = user_passes_test(lambda u: u.is_staff)


@is_manager
def manager_dashboard(request):
    pending = (
        Booking.objects
        .filter(status=Booking.Status.PENDING)
        .select_related("slot", "slot__court", "player")
        .order_by("slot__date", "slot__start_time", "created_at")
    )
    return render(request, "bookings/manager_dashboard.html", {"pending": pending})


@is_manager
@require_POST
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.approve()
    messages.success(request, f"Booking for {booking.slot} approved.")
    return redirect("manager_dashboard")


@is_manager
@require_POST
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.reject()
    messages.info(request, f"Booking for {booking.slot} rejected.")
    return redirect("manager_dashboard")