import datetime
from django.core.management.base import BaseCommand
from bookings.models import Court, TimeSlot


class Command(BaseCommand):
    help = "Seed 2 courts and a week of hourly slots (6am-11pm)."

    def handle(self, *args, **options):
        courts = []
        for name in ["Court A", "Court B"]:
            court, _ = Court.objects.get_or_create(name=name, defaults={"location": "Main Futsal Venue"})
            courts.append(court)

        today = datetime.date.today()
        created = 0
        for day_offset in range(7):
            date = today + datetime.timedelta(days=day_offset)
            for court in courts:
                for hour in range(6, 23):
                    start = datetime.time(hour, 0)
                    end = datetime.time((hour + 1) % 24, 0)
                    _, was_created = TimeSlot.objects.get_or_create(
                        court=court, date=date, start_time=start, end_time=end
                    )
                    if was_created:
                        created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(courts)} courts and {created} new time slots."))