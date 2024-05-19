from bs4 import BeautifulSoup
from moydodyr_api.els import page_checkers
from moydodyr_api.els.elssession import ELSSession
  
request_payload = {
    "__EVENTTARGET": "ctl00$LinkBooking", 
    "__EVENTARGUMENT": None,
    "__VIEWSTATE": "/wEPDwUKLTMwMDcxNzU2NA9kFgJmD2QWAgIDD2QWGGYPDxYGHgRUZXh0BRRTw7ZuZGFnIDE5IE1haiAyMDowOB4JRm9yZUNvbG9yCQAAAAAeBF8hU0ICBGRkAgEPDxYCHgdWaXNpYmxlaGQWAmYPFQEFUGFuZWxkAgIPZBYCZg8VAQRJbmZvZAIDDw9kFgIeBVN0eWxlBTRtaW4td2lkdGg6NzVweDtib3JkZXI6MnB4IHNvbGlkICM5Q0Y7Y3Vyc29yOmRlZmF1bHQ7FgJmDxUBCE1pbiBzaWRhZAIED2QWAmYPFQEEQm9rYWQCBQ8PFgIfA2hkFgJmDxUBBlN0YXR1c2QCBg8PFgIfA2hkFgJmDxUBBVNhbGRvZAIHD2QWAmYPFQEOSW5zdMOkbGxuaW5nYXJkAggPZBYCZg8VAQhMb2dnYSB1dGQCCg9kFggCAQ9kFgICAQ8PFgYfAAUTRHUgaGFyIGluZ2V0IGJva2F0Lh8BCQAAAAAfAgIEZGQCAw9kFgICAw88KwALAgAPFggeCERhdGFLZXlzFgAeC18hSXRlbUNvdW50Zh4JUGFnZUNvdW50AgEeFV8hRGF0YVNvdXJjZUl0ZW1Db3VudGZkCRYEHwEJAAAAAB8CAgRkAgUPDxYCHwNoZBYEAgEPZBYCAgEPDxYCHwAFFVBlcnNvbmxpZyBpbmZvcm1hdGlvbmRkAgMPZBYCAgEPDxYCHwBlZGQCBw8PFgIfA2hkFgICAw9kFgICAQ9kFgICAQ9kFgICAQ8PFgIfAAUGRW5lcmdpZGQCDA8PFgIfAAVRVmVyc2lvbjogMS4yLjAuMTIsIFVzZXJ3ZWI6IDEuMi4wLjkgQ29weXJpZ2h0IEVsZWN0cm9sdXggTGF1bmRyeSBTeXN0ZW0gU3dlZGVuIEFCZGQCDQ8PFgIfAAUhQW52w6RuZMKgbW9iaWxlbsKgZsO2csKgYXR0wqBib2thZGRktd8v9JhXLFuE9/mBtxKkB74/yA8=",
    "__VIEWSTATEGENERATOR": "21AF7994",
    "__EVENTVALIDATION": "/wEWCALOkZS9CALgiPbTBQK/zcjICgLZh5iXDwLty8WuCgLBubeEAgKi8/y9CALs5b67ArmQrkS8YmloNVUzq+J7OOnWjFtx",
    "ctl00$MessageType": "ERROR",
    "ctl00$ContentPlaceHolder1$ShowExpand": False,
}

url = '/Booking/BookingMain.aspx'

def run(session: ELSSession) -> dict[str, str]:
    """Returns "Tvattstuga3/Tvattstuga4" list selection
    Tip: Must be called, before fetching laundry bookings,ie goto_laundry_bookings()
    """
    request_data = request_payload
    response = session.post(url, request_data)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    data = {tag.get('name'): tag.get('value', '') for tag in soup.find_all('input')}
    REQUIRED_INPUTS_COUNT = 6
    if len(data) != REQUIRED_INPUTS_COUNT:
        raise Exception(f"input number must be {REQUIRED_INPUTS_COUNT} actual={len(data)}")
    
    return data
