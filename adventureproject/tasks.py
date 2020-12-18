from celery import shared_task

from time import sleep
from adventureapp.models import *

@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def insurance_date():
    now = timezone.now()
    bookings = Booking.objects.all()
    for booking in bookings:
        if booking.check_out < timezone.datetime.today():
            booking.room.is_reserved = True
            booking.room.save()
        else:
            booking.room.is_reserved = False
            booking.room.save()