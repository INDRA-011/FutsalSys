from django.conf import settings
from django.db import models


class Court(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name="slots")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.court.name} | {self.date} {self.start_time}-{self.end_time}"


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name="bookings")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.player.username} -> {self.slot} [{self.status}]"

    def approve(self):
        self.status = self.Status.APPROVED
        self.save()
        self.slot.is_booked = True
        self.slot.save()
        Booking.objects.filter(slot=self.slot, status=self.Status.PENDING).exclude(pk=self.pk).update(
            status=self.Status.REJECTED
        )

    def reject(self):
        self.status = self.Status.REJECTED
        self.save()