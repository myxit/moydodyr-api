import re
from bs4 import BeautifulSoup
from moydodyr_api.els import page_checkers
from moydodyr_api.els.elssession import ELSSession
from .types import AvailableLaundries 

laundry3_request_payload = {
    '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$dgForval$ctl02$ctl00',
    '__EVENTARGUMENT': None,
    '__VIEWSTATE': '/wEPDwUJLTIzODE2OTAzD2QWAmYPZBYCAgMPZBYYZg8PFgYeBFRleHQFFFPDtm5kYWcgMTkgTWFqIDIwOjEzHglGb3JlQ29sb3IJAAAAAB4EXyFTQgIEZGQCAQ8PFgIeB1Zpc2libGVoZBYCZg8VAQVQYW5lbGQCAg9kFgJmDxUBBEluZm9kAgMPZBYCZg8VAQhNaW4gc2lkYWQCBA8PZBYCHgVTdHlsZQU0bWluLXdpZHRoOjc1cHg7Ym9yZGVyOjJweCBzb2xpZCAjOUNGO2N1cnNvcjpkZWZhdWx0OxYCZg8VAQRCb2thZAIFDw8WAh8DaGQWAmYPFQEGU3RhdHVzZAIGDw8WAh8DaGQWAmYPFQEFU2FsZG9kAgcPZBYCZg8VAQ5JbnN0w6RsbG5pbmdhcmQCCA9kFgJmDxUBCExvZ2dhIHV0ZAIKD2QWBAIBD2QWAgIBDw8WAh8ABQRCb2thZGQCAw9kFgQCAQ8PFgYfAAUWVsOkbGogdmFkIGR1IHZpbGwgYm9rYR8BCfAAAAAfAgIEZGQCAw88KwALAgAPFggeCERhdGFLZXlzFgAeC18hSXRlbUNvdW50AgIeCVBhZ2VDb3VudAIBHhVfIURhdGFTb3VyY2VJdGVtQ291bnQCAmQJFgQfAQkAAAAAHwICBBYCZg9kFgQCAQ9kFgZmDw8WAh8ABQExZGQCAQ9kFgJmDw8WAh8ABQ1UdsOkdHRzdHVnYSAzZGQCAg8PFgIfAAUNVHbDpHR0c3R1Z2EgM2RkAgIPZBYGZg8PFgIfAAUBMmRkAgEPZBYCZg8PFgIfAAUNVHbDpHR0c3R1Z2EgNGRkAgIPDxYCHwAFDVR2w6R0dHN0dWdhIDRkZAIMDw8WAh8ABVFWZXJzaW9uOiAxLjIuMC4xMiwgVXNlcndlYjogMS4yLjAuOSBDb3B5cmlnaHQgRWxlY3Ryb2x1eCBMYXVuZHJ5IFN5c3RlbSBTd2VkZW4gQUJkZAINDw8WAh8ABSFBbnbDpG5kwqBtb2JpbGVuwqBmw7ZywqBhdHTCoGJva2FkZGT/cDgfkhyCVykXbx5Bn+g/g2LiXA==',
    '__VIEWSTATEGENERATOR': '05560514',
    '__EVENTVALIDATION': '/wEWCQLfueXmAwLgiPbTBQK/zcjICgLZh5iXDwLty8WuCgLBubeEAgKi8/y9CAL25eyzDgL25YDSBqcD8TQv7CIKaoZJ1veFmVqwvXXs',
    'ctl00$MessageType': 'ERROR',
}

laundry4_request_payload = {
    '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$dgForval$ctl03$ctl00',
    '__EVENTARGUMENT': None,
    '__VIEWSTATE': '/wEPDwUJLTIzODE2OTAzD2QWAmYPZBYCAgMPZBYYZg8PFgYeBFRleHQFFFPDtm5kYWcgMTkgTWFqIDIwOjIxHglGb3JlQ29sb3IJAAAAAB4EXyFTQgIEZGQCAQ8PFgIeB1Zpc2libGVoZBYCZg8VAQVQYW5lbGQCAg9kFgJmDxUBBEluZm9kAgMPZBYCZg8VAQhNaW4gc2lkYWQCBA8PZBYCHgVTdHlsZQU0bWluLXdpZHRoOjc1cHg7Ym9yZGVyOjJweCBzb2xpZCAjOUNGO2N1cnNvcjpkZWZhdWx0OxYCZg8VAQRCb2thZAIFDw8WAh8DaGQWAmYPFQEGU3RhdHVzZAIGDw8WAh8DaGQWAmYPFQEFU2FsZG9kAgcPZBYCZg8VAQ5JbnN0w6RsbG5pbmdhcmQCCA9kFgJmDxUBCExvZ2dhIHV0ZAIKD2QWBAIBD2QWAgIBDw8WAh8ABQRCb2thZGQCAw9kFgQCAQ8PFgYfAAUWVsOkbGogdmFkIGR1IHZpbGwgYm9rYR8BCfAAAAAfAgIEZGQCAw88KwALAgAPFggeCERhdGFLZXlzFgAeC18hSXRlbUNvdW50AgIeCVBhZ2VDb3VudAIBHhVfIURhdGFTb3VyY2VJdGVtQ291bnQCAmQJFgQfAQkAAAAAHwICBBYCZg9kFgQCAQ9kFgZmDw8WAh8ABQExZGQCAQ9kFgJmDw8WAh8ABQ1UdsOkdHRzdHVnYSAzZGQCAg8PFgIfAAUNVHbDpHR0c3R1Z2EgM2RkAgIPZBYGZg8PFgIfAAUBMmRkAgEPZBYCZg8PFgIfAAUNVHbDpHR0c3R1Z2EgNGRkAgIPDxYCHwAFDVR2w6R0dHN0dWdhIDRkZAIMDw8WAh8ABVFWZXJzaW9uOiAxLjIuMC4xMiwgVXNlcndlYjogMS4yLjAuOSBDb3B5cmlnaHQgRWxlY3Ryb2x1eCBMYXVuZHJ5IFN5c3RlbSBTd2VkZW4gQUJkZAINDw8WAh8ABSFBbnbDpG5kwqBtb2JpbGVuwqBmw7ZywqBhdHTCoGJva2FkZGQuS+6WRSJGdxi2mh7BYqZlWZPw2Q==',
    '__VIEWSTATEGENERATOR': '05560514',
    '__EVENTVALIDATION': '/wEWCQKNzJ3rAQLgiPbTBQK/zcjICgLZh5iXDwLty8WuCgLBubeEAgKi8/y9CAL25eyzDgL25YDSBkTZa174MVn/cmZMIrceg2iUaSN8',
    'ctl00$MessageType': 'ERROR',
}

url = '/Booking/Prechoices.aspx'
onclick_pattern = re.compile(r"('BookPass\d,\d,\d,'),('\d,\d,\d,')")

def run(session: ELSSession, laundry_id: AvailableLaundries) -> tuple[dict[str, str], list[tuple[str, str, str]], list[str]]:
    """
    Tip: must be called after goto_laundry_bookings(), select_booking() 
    """
    request_data = laundry3_request_payload if laundry_id == AvailableLaundries.LAUNDRY_3 else laundry4_request_payload
    response = session.post(url, request_data)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
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

    return view_state, cell_bookings, weekdays_cells_data
