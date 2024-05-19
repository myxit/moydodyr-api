from moydodyr_api.els import page_checkers
from moydodyr_api.els.elssession import ELSSession
  
request_payload = {
    "__EVENTTARGET": None, 
    "__EVENTARGUMENT": None,
    "__VIEWSTATE": "/wEPDwUKLTQwMTEzOTIzNA9kFgJmD2QWAgIDD2QWGGYPDxYGHgRUZXh0BRRTw7ZuZGFnIDE5IE1haiAxNjo1Nh4JRm9yZUNvbG9yCQAAAAAeBF8hU0ICBGRkAgEPDxYCHgdWaXNpYmxlaGQWAmYPFQEFUGFuZWxkAgIPZBYCZg8VAQRJbmZvZAIDD2QWAmYPFQEITWluIHNpZGFkAgQPD2QWAh4FU3R5bGUFNG1pbi13aWR0aDo3NXB4O2JvcmRlcjoycHggc29saWQgIzlDRjtjdXJzb3I6ZGVmYXVsdDsWAmYPFQEEQm9rYWQCBQ8PFgIfA2hkFgJmDxUBBlN0YXR1c2QCBg8PFgIfA2hkFgJmDxUBBVNhbGRvZAIHD2QWAmYPFQEOSW5zdMOkbGxuaW5nYXJkAggPZBYCZg8VAQhMb2dnYSB1dGQCCg9kFgQCAQ9kFgICAQ8PFgYfAAUEQm9rYR8BCQAAAAAfAgIEZGQCAw9kFgxmDw8WBh8ABQlWYWxkIHRpZDofAQkAAAAAHwICBGRkAgEPDxYGHwAFDkzDtnJkYWcgMjUgbWFqHwEJAAAAAB8CAgRkZAICDw8WBh8ABQ0xOTowMCAtIDIzOjAwHwEJAAAAAB8CAgRkZAIjDw8WBh4HVG9vbFRpcGUfAAUNVHbDpHR0c3R1Z2EgMx8DZxYCHgVzdHlsZQVUd2lkdGg6MTIwcHg7aGVpZ2h0OjUwcHg7Y29sb3I6MDAwMDAwO2JhY2tncm91bmQtY29sb3I6IzAwQTAwMDtib3JkZXI6c29saWQgM3B4ICMwMDA7ZAJDDw8WAh8ABQhUaWxsYmFrYWRkAkQPDxYCHwAFBEJva2FkZAIMDw8WAh8ABVFWZXJzaW9uOiAxLjIuMC4xMiwgVXNlcndlYjogMS4yLjAuOSBDb3B5cmlnaHQgRWxlY3Ryb2x1eCBMYXVuZHJ5IFN5c3RlbSBTd2VkZW4gQUJkZAINDw8WAh8ABSFBbnbDpG5kwqBtb2JpbGVuwqBmw7ZywqBhdHTCoGJva2FkZGQ4SIv2BhfTBAYikKHU5tSbbW2ruQ==",
    "__VIEWSTATEGENERATOR": "BE703319",
    "__EVENTVALIDATION": "/wEWCgK7q/KGBgLgiPbTBQK/zcjICgLZh5iXDwLty8WuCgLBubeEAgKi8/y9CAKP2LPLDgLcnsyKAQKsx+fzBtaLqyQDCoJvwcIZGkaKiIVXA1T8",
    "ctl00$MessageType": "INFO",
    "ctl00$ContentPlaceHolder1$btMaskingruppRandom": "Boka",
}

url = '/Booking/BookingCalendar.aspx'

def run(session: ELSSession):
    """
    Tip: must be called after goto_laundry_bookings(), select_booking() 
    """
    request_data = request_payload
    response = session.post(url, request_data)
    response.raise_for_status()
    if not page_checkers.is_login_page(response.content):
        raise Exception("Not authenticated")
