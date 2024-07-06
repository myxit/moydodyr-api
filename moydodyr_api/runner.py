from datetime import date, datetime
import time
import logging
import logging.config
from re import S
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
        db.connect()
        logger.info('[OK]')

        session = els.ELSSession(config.els_url)
        logger.info("1. session initialized")
        
        logger.info("2. fetching Login Form")
        els.login_fetch(session)
        
        logger.info("3. posting credentials")
        els.login_submit(session, config.els_username, config.els_password)
        
        logger.info("4. Fetching Laundry List")
        els.laundries_list_fetch(session)
        # ### LOADING #Laundry3
        # logger.info(f"5. Requesting Laundry 'ELSSession.LAUNDRY_3' bookings")
        # raw_data, weekdays_cells_data = els.laundry_bookings_fetch(session, AvailableLaundries.LAUNDRY_3)

        # bookings = parse_bookings(AvailableLaundries.LAUNDRY_3, raw_data, weekdays_cells_data)
        # logger.info(f"6. total parsed bookings: {len(bookings)}")
        
        is_available = lambda booking: booking.is_available
        # active_bookings = list(filter(is_available, bookings))
        # logger.info(f"Active bookings for {AvailableLaundries.LAUNDRY_3} is {len(active_bookings)}")
        THREAD_SLEEP = 5
        try:
            left = 1
            while left > 0:
                ## Laundry 3
                fetching_for = AvailableLaundries.LAUNDRY_3
                raw_data, weekdays_cells_data = els.laundry_bookings_fetch(session, fetching_for)
                bookings = parse_bookings(fetching_for, raw_data, weekdays_cells_data)
                active_bookings = list(filter(is_available, bookings))
                logger.info(f"5. Active bookings for #{fetching_for} is {len(active_bookings)} of {len(bookings)}")
                db_ids = [db.create_or_update(booking.id, date.today(), booking.is_available) for booking in bookings]
                #### Next 7 days bookings
                raw_data, weekdays_cells_data = els.laundry_bookings_fetch_next_page(session)
                bookings = parse_bookings(fetching_for, raw_data, weekdays_cells_data)
                active_bookings = list(filter(is_available, bookings))
                logger.info(f"6. Active bookings for #{fetching_for} is {len(active_bookings)} of {len(bookings)}")
                db_ids = [db.create_or_update(booking.id, date.today(), booking.is_available) for booking in bookings]

                # ## Switching Laundry
                # fetching_for = AvailableLaundries.LAUNDRY_4
                # logger.info("7. Fetching Laundry List before switch on {fetching_for}")
                # els.laundries_list_fetch(session)
                # ## Laundry 4
                # raw_data, weekdays_cells_data = els.laundry_bookings_fetch(session, fetching_for)
                # bookings = parse_bookings(fetching_for, raw_data, weekdays_cells_data)
                # active_bookings = list(filter(is_available, bookings))
                # logger.info(f"Active bookings for #{fetching_for} is {len(active_bookings)} of {len(bookings)}")
                # db_ids = [db.create_or_update(booking.id, date.today(), booking.is_available) for booking in bookings]
                # #### Next 7 days bookings
                # raw_data, weekdays_cells_data = els.laundry_bookings_fetch_next_page(session)
                # bookings = parse_bookings(fetching_for, raw_data, weekdays_cells_data)
                # active_bookings = list(filter(is_available, bookings))
                # logger.info(f"Active bookings for #{fetching_for} is {len(active_bookings)} of {len(bookings)}")
                # db_ids = [db.create_or_update(booking.id, date.today(), booking.is_available) for booking in bookings]

                # ## Sleep
                # time.sleep(THREAD_SLEEP)
                if left <= 0:
                    break
                else:
                    left -= 1
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
