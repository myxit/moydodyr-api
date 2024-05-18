import logging
import re
import requests
from bs4 import BeautifulSoup


user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

logger = logging.getLogger("ELSSession")

onclick_pattern = re.compile(r"('BookPass\d,\d,\d,'),('\d,\d,\d,')")

onclick_pattern = re.compile(r"('BookPass\d,\d,\d,'),('\d,\d,\d,')")

class ELSSession:
    LAUNDRY_3 = 'ctl00$ContentPlaceHolder1$dgForval$ctl02$ctl00'
    LAUNDRY_4 = 'ctl00$ContentPlaceHolder1$dgForval$ctl03$ctl00'
    
    def __init__(self, els_url):
        # """Initialize ELS sakrafast session object."""
        session = requests.Session()
        session.headers.update({
            'User-Agent': user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Origin": els_url,
            "Pragma": "no-cache",
            "Referer": els_url + "/Default.aspx",
        })
        self.session = session
        self.els_url = els_url

    def get_login_form_data(self):
        # try:
        response = self.session.get(self.els_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {tag.get('name'): tag.get('value', '') for tag in soup.find_all('input')}
        data.update({
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$btOK',
        })
        del data['ctl00$ContentPlaceHolder1$btOK']
        
        return data
        # except Exception as ex:
        #     return False, str(ex)
                    
    def do_login(self, username, password, login_form_values):
        url = self.els_url + "/Default.aspx"
        request_data = dict(login_form_values, **{'ctl00$ContentPlaceHolder1$tbUsername': username, 'ctl00$ContentPlaceHolder1$tbPassword': password})
        response = self.session.post(url, request_data)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        inputs_data = {tag.get('name'): tag.get('value', '') for tag in soup.find_all('input')}
        REQUIRED_INPUTS_COUNT = 7
        if len(inputs_data) < REQUIRED_INPUTS_COUNT:
            raise Exception(f"inputs number less than required={REQUIRED_INPUTS_COUNT}, actual={len(inputs_data)}")        
        return inputs_data
        
    def get_booking_main(self):
        """a.k.a. "Min Sida"
        Tip: use only to get my bookings
        """
        REQUIRED_INPUTS_COUNT = 6
        url = self.els_url + '/Booking/BookingMain.aspx'
        response = self.session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        #  data = {tag.get('name'): tag.get('value', '') for tag in soup.find_all('input')}
        data = {tag.get('name'): tag.get('value', '') for tag in soup.find_all('input')}
        if len(data) != REQUIRED_INPUTS_COUNT:
             raise Exception(f"input number must be {REQUIRED_INPUTS_COUNT} actual={len(data)}")
        
        return data
        # except Exception as ex:
        #     return False, str(ex)
        
    def goto_laundries_list(self, form_data):
        """Returns "Tvattstuga3/Tvattstuga4" list selection
        Tip: 
        """
        url = self.els_url + '/Booking/BookingMain.aspx'        
        request_data = dict(form_data, **{'__EVENTTARGET': 'ctl00$LinkBooking'})
        response = self.session.post(url, request_data)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {tag.get('name'): tag.get('value', '') for tag in soup.find_all('input')}
        REQUIRED_INPUTS_COUNT = 6
        if len(data) != REQUIRED_INPUTS_COUNT:
            raise Exception(f"input number must be {REQUIRED_INPUTS_COUNT} actual={len(data)}")
        
        return data
        
    def goto_laundry_bookings(self, form_data, laundry_id):
        url = self.els_url + '/Booking/Prechoices.aspx'
        request_data = dict(form_data, **{'__EVENTTARGET': laundry_id})
        response = self.session.post(url, request_data)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        hidden_inputs_data = {tag.get('name'): tag.get('value', '') for tag in soup.find_all('input', {'type': 'hidden'})}
        REQUIRED_INPUTS_NUMBER = 6
        if len(hidden_inputs_data) != REQUIRED_INPUTS_NUMBER:
            raise Exception(f"Input number does not match required={REQUIRED_INPUTS_NUMBER}, actual={len(hidden_inputs_data)}")

        cell_bookings = [(tag.get('name', ''), tag.get('onclick', ''), tag.get('title', '')) for tag in soup.find_all('input', {'type': 'submit', 'onclick': onclick_pattern})]
        
        # 3. Week days extraction table > tr td
        soup_week_cells = soup.select('tr[valign="top"] td[align="center"] span')
        weekdays_cells_data = [tag.text.strip() for tag in soup_week_cells]
        WEEKDAYS_CONTROL_NR = 7
        if len(weekdays_cells_data) != WEEKDAYS_CONTROL_NR:
            raise Exception(f"Weekdays control number {WEEKDAYS_CONTROL_NR} does not match {len(weekdays_cells_data)}")
    
        return hidden_inputs_data, cell_bookings, weekdays_cells_data
        