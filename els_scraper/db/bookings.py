import logging
import peewee
from datetime import datetime, date, timedelta
from .db import BaseModel

logger = logging.getLogger(__name__)


class Booking(BaseModel):
    booking_id = peewee.CharField(unique=True)
    is_available = peewee.BooleanField(default=False)
    valid_on = peewee.DateField(default=date.today)
    updated_at = peewee.DateTimeField(default=datetime.now)

def create_or_update(booking_id: str, valid_on: date, is_available: bool):
    db_instance_id = (Booking
             .insert(booking_id=booking_id, valid_on=valid_on, is_available=is_available)
             .on_conflict_replace()
             .execute()
    )
    return db_instance_id

def show_near_available():
    two_days_plus = datetime.now() + timedelta(days=2)
    available_bookings = Booking.select().where(
        (Booking.valid_on.between(datetime.now(), two_days_plus)) and (Booking.is_available) 
    )
    return available_bookings
