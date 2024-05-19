import logging
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
        inputs_data = els.login_fetch(session)
        
        logger.info("3. posting credentials")
        inputs_data = els.login_submit(session, inputs_data, config.els_username, config.els_password)
        
        logger.info("4. Fetching Laundry List")
        inputs_data = els.laundries_list_fetch(session)
        
        logger.info(f"5. Requesting Laundry 'ELSSession.LAUNDRY_3' bookings")
        inputs_data, raw_data, weekdays_cells_data = els.laundry_bookings_fetch(session, AvailableLaundries.LAUNDRY_3)

        bookings = parse_bookings(AvailableLaundries.LAUNDRY_3, raw_data, weekdays_cells_data)
        logger.info(f"6. total parsed bookings: {len(bookings)}")
        
        # SELECTED_BOOKING_IDX = len(bookings) - 1
        # logger.info(f"7. selecting booking idx: {SELECTED_BOOKING_IDX}")
        # logger.debug(bookings[SELECTED_BOOKING_IDX])

        # els.select_booking(session, bookings[SELECTED_BOOKING_IDX].form_data)
        # els.confirm_booking(session)

    

    except Exception as ex:
        return False, "Exception: " + str(ex)

   
    return True, "no errors"
        
if __name__ == "__main__":
    result = main_run()
    print(f"main_run() result {result}")
