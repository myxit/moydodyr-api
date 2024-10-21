import logging
import logging.config
import els
import db
from config import get_settings
from booking_parser import parse_bookings
from moydodyr_api.booking import AvailableLaundries
import traceback

logging.config.fileConfig('logger.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

config = get_settings()

def main_run():    
    try:
        logger.info("0. Connecting to db")
        db.db_init()
        
        logger.info('[OK]')

        session = els.ELSSession(config.els_url)
        logger.info("1. session initialized")
        
        logger.info("2. fetching Login Form")
        els.login_fetch(session)
        
        logger.info("3. posting credentials")
        els.login_submit(session, config.els_username, config.els_password)        
        
        def is_available(booking):
            return booking.is_available
        
        try:
            prev_snapshot_id = db.get_last_id()
            snapshot_id = 1 if prev_snapshot_id is None else prev_snapshot_id + 1
            logger.info(f"4. Starting snapshot snapshot_id#{snapshot_id}")
        
            for fetching_for in [AvailableLaundries.LAUNDRY_3, AvailableLaundries.LAUNDRY_4]:
                logger.info("4. Fetching Laundry List")
                els.laundries_list_fetch(session)
                
                logger.info(f"pointcut=[START] Start fetching booking for #{fetching_for}")
                raw_data, weekdays_cells_data = els.laundry_bookings_fetch(session, fetching_for)
                bookings = parse_bookings(fetching_for, raw_data, weekdays_cells_data)
                #### Snapshots
                for booking in bookings:
                    laundry_id = booking.id.split(":")[0]
                    time_slot_id = "-".join([booking.time_from, booking.time_to])
                    booked_by = 1 if booking.is_available else 0
                    db.insert(
                        snapshot_id, laundry_id, booking.date, time_slot_id, booked_by
                    ) 
                
                active_bookings = list(filter(is_available, bookings))
                
                # db_ids = [db.create_or_update(booking.id, date.today(), booking.is_available) for booking in bookings]
                #### Next 7 days bookings
                raw_data, weekdays_cells_data = els.laundry_bookings_fetch_next_page(session)
                bookings = parse_bookings(fetching_for, raw_data, weekdays_cells_data)
                #### Snapshots
                for booking in bookings:
                    laundry_id = booking.id.split(":")[0]
                    time_slot_id = "-".join([booking.time_from, booking.time_to])
                    booked_by = 1 if booking.is_available else 0
                    db.insert(snapshot_id, laundry_id, booking.date, time_slot_id, booked_by)
                    
                active_bookings = list(filter(is_available, bookings))
                logger.info(f"pointcut=[SUCCESS] Active bookings for #{fetching_for} is {len(active_bookings)} of {len(bookings)}")
                # db_ids = [db.create_or_update(booking.id, date.today(), booking.is_available) for booking in bookings]
        except KeyboardInterrupt:
            logger.info("Interrupted")
        
        
        # FIRST_FREE_BOOKING = next((booking for booking in bookings if is_available(booking)), None)
        # if not FIRST_FREE_BOOKING:
        #     raise Exception("No free bookings available for selected laundry")
        
        # logger.info(f"7. selecting booking : {FIRST_FREE_BOOKING}")
        # els.laundry_booking_fetch(session, FIRST_FREE_BOOKING.form_data)
        # els.laundry_booking_submit(session)
    except Exception as ex:
        print(traceback.format_exc())
        return False, "Exception: " + str(ex)
    finally:
        db.disconnect()

   
    return True, "no errors"
        
if __name__ == "__main__":
    result = main_run()
    print(f"main_run() result {result}")
