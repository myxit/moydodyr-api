import logging
import peewee
from datetime import datetime, date, timedelta

logger = logging.getLogger()

# Define the SQLite database
db = peewee.SqliteDatabase('my_database.db')

# Define a model class
class BaseModel(peewee.Model):
    class Meta:
        database = db

class Booking(BaseModel):
    booking_id = peewee.CharField(unique=True)
    is_available = peewee.BooleanField(default=False)
    valid_on = peewee.DateField(default=date.today)
    updated_at = peewee.DateTimeField(default=datetime.now)

def connect():
    # Connect to the database and create the tables
    db.connect()
    db.create_tables([Booking])

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
        (Booking.valid_on.between(datetime.now(), two_days_plus)) & (Booking.is_available == True) 
    )
    return available_bookings

def disconnect():
    try:
        db.close()
    except Exception as ex:
        logger.warning(f"Could not close database connection. Error: " + str(ex))
