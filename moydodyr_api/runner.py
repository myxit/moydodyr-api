import logging
from re import S
import els
from config import get_settings
from booking_parser import parse_bookings
from moydodyr_api.booking import AvailableLaundries

logging.basicConfig( level= logging.DEBUG)
logger = logging.getLogger()
config = get_settings()

def main_run():    
    try:
        session = els.ELSSession(config.els_url)
        logger.info("1. session initialized")
        
        logger.info("2. fetching Login Form")
        els.login_fetch(session)
        
        logger.info("3. posting credentials")
        els.login_submit(session, config.els_username, config.els_password)
        
        logger.info("4. Fetching Laundry List")
        els.laundries_list_fetch(session)
        
        logger.info(f"5. Requesting Laundry 'ELSSession.LAUNDRY_3' bookings")
        raw_data, weekdays_cells_data = els.laundry_bookings_fetch(session, AvailableLaundries.LAUNDRY_3)

        bookings = parse_bookings(AvailableLaundries.LAUNDRY_3, raw_data, weekdays_cells_data)
        logger.info(f"6. total parsed bookings: {len(bookings)}")
        
        is_available = lambda booking: booking.is_available
        FIRST_FREE_BOOKING = next((booking for booking in bookings if is_available(booking)), None)
        if not FIRST_FREE_BOOKING:
            raise Exception("No free bookings available for selected laundry")
        
        logger.info(f"7. selecting booking : {FIRST_FREE_BOOKING}")
        els.laundry_booking_fetch(session, FIRST_FREE_BOOKING.form_data)
        els.laundry_booking_submit(session)
    except Exception as ex:
        return False, "Exception: " + str(ex)

   
    return True, "no errors"
        
if __name__ == "__main__":
    result = main_run()
    print(f"main_run() result {result}")
