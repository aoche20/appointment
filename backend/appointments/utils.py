from datetime import datetime, timedelta
from appointments.models import Appointment

def generate_time_slots(
    date,
    open_time,
    close_time,
    duration,
    employee
):
    slots = []
    start = datetime.combine(date, open_time)
    end = datetime.combine(date, close_time)

    while start + timedelta(minutes=duration) <= end:
        slot_end = start + timedelta(minutes=duration)

        conflict = Appointment.objects.filter(
            employee=employee,
            date=date,
            start_time__lt=slot_end.time(),
            end_time__gt=start.time(),
            status__in=['pending', 'confirmed']
        ).exists()

        if not conflict:
            slots.append({
                "start": start.time(),
                "end": slot_end.time()
            })

        start += timedelta(minutes=duration)

    return slots
