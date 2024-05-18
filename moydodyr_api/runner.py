import logging
from elssession import ELSSession
from config import get_settings
from booking_parser import parse_bookings

logging.basicConfig( level= logging.DEBUG)
logger = logging.getLogger()
# def extract_form_info(url):
#     try:
#         return {}
#     except requests.RequestException as e:
#         return {'error': str(e)}
config = get_settings()

def main_run():
    # 1. Pre-start
    #   init_session()
    # 2. while no_error:
    #   isOk, data = get_bookings()
    #   if not isOk: return False, error_code
    #   if bookings_changed = notify_subscribers()
    #
    
    try:
        session = ELSSession(config.els_url)
        logger.info("1. session initialized")
        
        logger.info("2. fetching Login Form")
        inputs_data = session.get_login_form_data()
        
        logger.info("3. posting credentials")
        # logger.info(f"1.2 get_login_form_data() {isSuccess}")
        inputs_data = session.do_login(config.els_username, config.els_password, inputs_data)
        
        logger.info("4. Fetching Laundry List")
        inputs_data = session.goto_laundries_list(inputs_data)
        
        logger.info(f"5. Requesting Laundry 'ELSSession.LAUNDRY_3' bookings")
        inputs_data, raw_data, weekdays_cells_data = session.goto_laundry_bookings(inputs_data, ELSSession.LAUNDRY_3)
        # print(f"1 inputs data: {inputs_data}")
        print(f"2 laundry bookings raw_data: {raw_data}")
        print(f"3 raw weekdays data: {weekdays_cells_data}")
        bookings = parse_bookings(raw_data, weekdays_cells_data)
        # for (element_name, element_onclick_str, element_title_str) in raw_data:
        #     Booking.make_of(element_name, element_onclick_str, element_title_str)
        # logger.debug("Parsed bookings[]: %s", bookings)
        print("4. parsed bookings data")
        print(' '.join(map(repr, bookings)))

    except Exception as ex:
        return False, "Exception: " + str(ex)

    # if not isSuccess:
    #     return False, "Command do_login() returned False, " + payload
    # logger.info(f"2.2 do_login() {isSuccess}") 

    # isSuccess, payload = session.get_booking_main()
    # logger.info(f"3.2 get_booking_main() {isSuccess}") 

    # isSuccess, payload = session.goto_laundries_selection(payload)
    # logger.info(f"4.2 goto_laundries_selection() {isSuccess}") 

    # isSuccess, payload = session.get_laundries_list()
    # logger.info(f"5.2 get_laundries_list() {isSuccess}")

    # isSuccess, payload = session.goto_laundry_bookings(payload, ELSSession.LAUNDRY_3)
    # logger.info(f"6.2 goto_laundry_bookings(ELSSession.LAUNDRY_3) {isSuccess}")

    # isSuccess, payload = session.goto_laundry_bookings(payload, ELSSession.LAUNDRY_4)
    # logger.info(f"7.2 goto_laundry_bookings(ELSSession.LAUNDRY_4) {isSuccess}")

    return True, "no errors"
        
if __name__ == "__main__":
    result = main_run()
    print(f"main_run() result {result}")
    # if 'error' in result:
    #     print(f"Error: {result['error']}")
    # else:
    #     print("Extracted Information: DONE")
        # print(f"Response Headers:\n{result['response_headers']}")
        # print(f"Input Text Fields: {result}")
        # print(f"Submit Button Name: {result['submit_button_name']}")
