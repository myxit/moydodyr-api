from bs4 import BeautifulSoup
from moydodyr_api.els.elssession import ELSSession

url = '/Booking/BookingMain.aspx'

def run(session: ELSSession):
    """a.k.a. "Min Sida"
    Tip: use only to get my bookings
    """
    MIN_INPUTS_COUNT = 6
    MAX_INPUTS_COUNT = 7
    response = session.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    data = {tag.get('name'): tag.get('value', '') for tag in soup.find_all('input')}
    if not (len(data) > MIN_INPUTS_COUNT and len(data) < MAX_INPUTS_COUNT):
            raise Exception(f"input number must be between {MIN_INPUTS_COUNT} and {MAX_INPUTS_COUNT} actual={len(data)}")
    
    return data
