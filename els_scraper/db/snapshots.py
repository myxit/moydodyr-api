import logging
import peewee
from datetime import datetime
from .db import BaseModel

logger = logging.getLogger(__name__)

# Here are three example rows for a database table named "snapshots" with the columns id, created_at, laundry_id, date, time_slot_id, and is_occupied:
#
# id	created_at	        laundry_id	    on_date	    time_slot_id	is_available    booked_by
# 1	    2024-10-17 10:30:45 	3	        2024-10-17	"07-10"	            true            0
# 2	    2024-10-17 10:35:22	    4	        2024-10-17	"07-11"	            false           123
# 3	    2024-10-17 10:40:18	    3	        2024-10-18	"10-13"             true            0

#   select s1.*, s2.id, printf("%d=>%d", s1.booked_by, s2.booked_by), s2.laundry_id, s2.time_slot_id 
#       from snapshot as s1 
#       inner join snapshot s2 on s1.id-1 = s2.id 
#           and s1.laundry_id = s2.laundry_id
#           and s1.on_date = s2.on_date
#           and s1.time_slot_id = s2.time_slot_id
#   where s1.id in (select 3 from snapshot) and s1.booked_by != 0 and s2.booked_by = 0;
# ....
# 3|2024-10-20 21:38:45.284105|LAUNDRY_3|2024-10-31|13:00-16:00|0|1|2|1=>0|LAUNDRY_3|13:00-16:00
# 3|2024-10-20 21:38:45.284105|LAUNDRY_3|2024-10-31|13:00-16:00|0|1|2|1=>0|LAUNDRY_3|13:00-16:00
#
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
        # indexes = (
            # ("id", "laundry_id", "on_date", "time_slot_id"), True), 
            # ("on_date", "time_slot_id"), False), 
            # )


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