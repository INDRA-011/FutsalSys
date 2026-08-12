from django.urls import path
from . import views_browse, views_manager, views_mybookings, views_history

urlpatterns = [

    #feature/browse-slots
    path("", views_browse.browse_slots, name="browse_slots"),
    path("book/<int:slot_id>/", views_browse.request_booking, name="request_booking"),

    #feature/my-bookings
    path("my-bookings/", views_mybookings.my_bookings, name="my_bookings"),
    path("my-bookings/<int:booking_id>/cancel/", views_mybookings.cancel_booking, name="cancel_booking"),

    #feature/manager-dashboard
    path("manager/dashboard/", views_manager.manager_dashboard, name="manager_dashboard"),
    path("manager/bookings/<int:booking_id>/approve/", views_manager.approve_booking, name="approve_booking"),
    path("manager/bookings/<int:booking_id>/reject/", views_manager.reject_booking, name="reject_booking"),

    #feature/all-bookings-polish 
    path("manager/all-bookings/", views_history.all_bookings, name="all_bookings"),
]