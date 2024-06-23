import logging
from moydodyr_api.els import page_checkers
from moydodyr_api.els.elssession import ELSSession

logger = logging.getLogger()
  
request_payload = {
    # Element specific
    "__EVENTTARGET": '',
    # Element specific 
    "__EVENTARGUMENT": '',
    # Element specific
    "__VIEWSTATE": None,
    # "__VIEWSTATEGENERATOR": "BE703319",
    # Element specific
    "__EVENTVALIDATION": None,
    "ctl00$MessageType": "INFO",
    "ctl00$ContentPlaceHolder1$btMaskingruppRandom": "Boka",
}

url = '/Booking/MachineGroup.aspx'

def run(session: ELSSession):
    """Submits selected booking
    Tip: must be called after laundry_bookings_fetch() 
    """
    # request_data = request_payload
    response = session.post(url)
    response.raise_for_status()
    if not page_checkers.is_login_page(response.content):
        logger.warn(response.content.decode())
        raise Exception("Not authenticated")
