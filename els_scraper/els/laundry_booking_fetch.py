import logging
from . import page_checkers, ELSSession
  
logger = logging.getLogger()

request_payload = {
    # Custom value
    "__EVENTTARGET": '',
    # Custom value
    "__EVENTARGUMENT": '',
    # Custom value
    "__VIEWSTATE": "/wEPDwUKLTQwMTEzOTIzNA9kFgJmD2QWAgIDD2QWGGYPDxYGHgRUZXh0BRRTw7ZuZGFnIDE5IE1haiAxNjo1Nh4JRm9yZUNvbG9yCQAAAAAeBF8hU0ICBGRkAgEPDxYCHgdWaXNpYmxlaGQWAmYPFQEFUGFuZWxkAgIPZBYCZg8VAQRJbmZvZAIDD2QWAmYPFQEITWluIHNpZGFkAgQPD2QWAh4FU3R5bGUFNG1pbi13aWR0aDo3NXB4O2JvcmRlcjoycHggc29saWQgIzlDRjtjdXJzb3I6ZGVmYXVsdDsWAmYPFQEEQm9rYWQCBQ8PFgIfA2hkFgJmDxUBBlN0YXR1c2QCBg8PFgIfA2hkFgJmDxUBBVNhbGRvZAIHD2QWAmYPFQEOSW5zdMOkbGxuaW5nYXJkAggPZBYCZg8VAQhMb2dnYSB1dGQCCg9kFgQCAQ9kFgICAQ8PFgYfAAUEQm9rYR8BCQAAAAAfAgIEZGQCAw9kFgxmDw8WBh8ABQlWYWxkIHRpZDofAQkAAAAAHwICBGRkAgEPDxYGHwAFDkzDtnJkYWcgMjUgbWFqHwEJAAAAAB8CAgRkZAICDw8WBh8ABQ0xOTowMCAtIDIzOjAwHwEJAAAAAB8CAgRkZAIjDw8WBh4HVG9vbFRpcGUfAAUNVHbDpHR0c3R1Z2EgMx8DZxYCHgVzdHlsZQVUd2lkdGg6MTIwcHg7aGVpZ2h0OjUwcHg7Y29sb3I6MDAwMDAwO2JhY2tncm91bmQtY29sb3I6IzAwQTAwMDtib3JkZXI6c29saWQgM3B4ICMwMDA7ZAJDDw8WAh8ABQhUaWxsYmFrYWRkAkQPDxYCHwAFBEJva2FkZAIMDw8WAh8ABVFWZXJzaW9uOiAxLjIuMC4xMiwgVXNlcndlYjogMS4yLjAuOSBDb3B5cmlnaHQgRWxlY3Ryb2x1eCBMYXVuZHJ5IFN5c3RlbSBTd2VkZW4gQUJkZAINDw8WAh8ABSFBbnbDpG5kwqBtb2JpbGVuwqBmw7ZywqBhdHTCoGJva2FkZGQ4SIv2BhfTBAYikKHU5tSbbW2ruQ==",
    "__VIEWSTATEGENERATOR": "09214D5A",
    # Custom value
    "__EVENTVALIDATION": "/wEWCgK7q/KGBgLgiPbTBQK/zcjICgLZh5iXDwLty8WuCgLBubeEAgKi8/y9CAKP2LPLDgLcnsyKAQKsx+fzBtaLqyQDCoJvwcIZGkaKiIVXA1T8",
    "ctl00$MessageType": "ERROR",
    # Custom key, value None
    "ctl00$ContentPlaceHolder1$6,4,1,": None
}

def run(session: ELSSession, value_specific_payload: dict[str, str]):
    """Preselects a booking
    Tip: must be called after goto_laundries_list(), goto_laundry_bookings()
    """
    request_data = request_payload | value_specific_payload
    response = session.post_back(data = request_data)
    if response.status_code not in [200, 302]:
        logger.debug(response.content.decode())
        raise Exception(f"{response.status_code} for url: {response.request.url}")
    
    if not page_checkers.is_booking_confirmation_page(response.content):
        raise Exception("Not authenticated")
