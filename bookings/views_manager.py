"""
OWNER: feature/manager-dashboard
Only this file + templates/bookings/manager_dashboard.html belong to this branch.
"""
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .models import Booking

is_manager = user_passes_test(lambda u: u.is_staff)


@is_manager
def manager_dashboard(request):
    """
    TODO:
    - List all Booking objects with status='pending'.
    - Group/sort by slot, then by created_at ascending.
    - Each row needs Approve / Reject buttons.
    """
    pending = Booking.objects.filter(status=Booking.Status.PENDING)
    return render(request, "bookings/manager_dashboard.html", {"pending": pending})


@is_manager
def approve_booking(request, booking_id):
    """
    TODO:
    - Only accept POST.
    - Call booking.approve() — logic already exists in bookings/models.py.
      Do NOT reimplement the auto-reject-competitors logic here.
    - Redirect back to manager_dashboard.
    """
    booking = get_object_or_404(Booking, pk=booking_id)
    return redirect("manager_dashboard")


@is_manager
def reject_booking(request, booking_id):
    """
    TODO:
    - Only accept POST.
    - Call booking.reject().
    - Redirect back to manager_dashboard.
    """
    booking = get_object_or_404(Booking, pk=booking_id)
    return redirect("manager_dashboard")