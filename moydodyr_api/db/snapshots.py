import logging
import peewee
from datetime import datetime
from .db import BaseModel

logger = logging.getLogger(__name__)

# Here are three example rows for a database table named "snapshots" with the columns id, created_at, laundry_id, date, time_slot_id, and is_occupied:
#
# id	created_at	        laundry_id	    date	    time_slot_id	is_available    booked_by
# 1	    2024-10-17 10:30:45 	3	        2024-10-17	"07-10"	            true            0
# 2	    2024-10-17 10:35:22	    4	        2024-10-17	"07-11"	            false           123
# 3	    2024-10-17 10:40:18	    3	        2024-10-18	"10-13"             true            0
class Snapshot(BaseModel):
    id = peewee.IntegerField(unique=False, primary_key=False)
    created_at = peewee.DateTimeField(default=datetime.now)
    laundry_id = peewee.CharField(index=True)
    on_date = peewee.DateField()
    time_slot_id = peewee.CharField()
    is_available = peewee.BooleanField(default=False)
    booked_by = peewee.IntegerField(default=0)
    class Meta:
        primary_key = peewee.CompositeKey("id", "laundry_id", "created_at")

def insert(snapshot_id: int, laundry_id: int, on_date, time_slot_id: str, booked_by: int):
    db_instance_id = Snapshot.insert(
        id=snapshot_id,
        laundry_id=laundry_id,
        on_date=on_date,
        time_slot_id=time_slot_id,
        is_available=booked_by == 0,
        booked_by=booked_by,
    ).execute()
    
    return db_instance_id

def get_last_id()->int|None:
    query = Snapshot.select(peewee.fn.MAX(Snapshot.id))
    return query.scalar()