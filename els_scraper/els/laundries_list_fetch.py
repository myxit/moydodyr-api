from bs4 import BeautifulSoup
from . import ELSSession
  
request_payload = {
    "__EVENTTARGET": "ctl00$LinkBooking", 
    "__EVENTARGUMENT": '',
    "ctl00$MessageType": "ERROR",
    "ctl00$ContentPlaceHolder1$ShowExpand": False,
}

def run(session: ELSSession) -> dict[str, str]:
    """Returns "Tvattstuga3/Tvattstuga4" list selection
    Tip: Must be called, before fetching laundry bookings,ie goto_laundry_bookings()
    """
    request_data = request_payload
    response = session.post_back(data = request_data)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    data = {tag.get('name'): tag.get('value', '') for tag in soup.find_all('input')}
    REQUIRED_INPUTS_COUNT = 6
    if len(data) != REQUIRED_INPUTS_COUNT:
        raise Exception(f"input number must be {REQUIRED_INPUTS_COUNT} actual={len(data)}")
    
    return data
