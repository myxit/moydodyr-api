import re
from bs4 import BeautifulSoup
from moydodyr_api.els import page_checkers
from moydodyr_api.els.elssession import ELSSession
from .types import AvailableLaundries 

laundry3_request_payload = {
    '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$dgForval$ctl02$ctl00',
    '__EVENTARGUMENT': '',
    'ctl00$MessageType': 'ERROR',
}

laundry4_request_payload = {
    '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$dgForval$ctl03$ctl00',
    '__EVENTARGUMENT': '',
    'ctl00$MessageType': 'ERROR',
}

onclick_pattern = re.compile(r"('BookPass\d,\d,\d,'),('\d,\d,\d,')")

def run(session: ELSSession, laundry_id: AvailableLaundries) -> tuple[list[tuple[str, str, str]], list[str]]:
    """
    Tip: must be called after goto_laundry_bookings(), select_booking() 
    """
    request_data = laundry3_request_payload if laundry_id == AvailableLaundries.LAUNDRY_3 else laundry4_request_payload
    response = session.post_back(data = request_data)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    # 2. Sanity check
    view_state = {tag.get('name'): tag.get('value', '') for tag in soup.find_all('input', {'type': 'hidden'})}
    REQUIRED_INPUTS_NUMBER = 6
    if len(view_state) != REQUIRED_INPUTS_NUMBER:
        raise Exception(f"Input number does not match required={REQUIRED_INPUTS_NUMBER}, actual={len(view_state)}")

    cell_bookings = [(tag.get('name', ''), tag.get('onclick', ''), tag.get('title', '')) for tag in soup.find_all('input', {'type': 'submit', 'onclick': onclick_pattern})]
    
    # 3. Week days extraction table > tr td
    soup_week_cells = soup.select('tr[valign="top"] td[align="center"] span')
    weekdays_cells_data = [tag.text.strip() for tag in soup_week_cells]
    WEEKDAYS_CONTROL_NR = 7
    if len(weekdays_cells_data) != WEEKDAYS_CONTROL_NR:
        raise Exception(f"Weekdays control number {WEEKDAYS_CONTROL_NR} does not match {len(weekdays_cells_data)}")

    return cell_bookings, weekdays_cells_data
