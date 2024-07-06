import logging
from bs4 import BeautifulSoup
from requests import Session
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class ELSSession():
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Origin": base_url,
            "Pragma": "no-cache",
            "Referer": base_url + "/Default.aspx",
        })
        self.view_state_inputs = {}
        self.prev_url = ''

    @staticmethod
    def _extract_view_state_related(input_kv: dict[str, str]) -> dict[str, str]:
        keys_to_keep = ['__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION']
        result = {}
        for key in keys_to_keep:
            if key in input_kv:
                value = input_kv[key]
                if value is None or value == '':
                    raise ValueError(f"The value for key '{key}' is empty in input_kv")
                result[key] = value

        logger.debug(f"Parsed view state-related dump: \n {result}")
        return result

    @staticmethod
    def _validate_response(response):
        if not response.status_code in [200, 302]:
            logger.warn(f"Unexpected status_code for {method} {url} ({response.status_code})")
            logger.debug(f"Body dump: \n {response.content.decode('utf-8')}")
            return False
        
        soup = BeautifulSoup(response.content, 'html.parser')
        hidden_inputs = soup.find_all('input', {'type': 'hidden'})
        if not len(hidden_inputs):
            logger.warn(f"Seems error: no hidden_inputs found for {method} {url}")
            # TODO: need reset self.view_related_inputs = {} ?????
            return False
    
        return True

    def get_login(self):
        response = self.session.get(self.base_url + "/Default.aspx")
        if not ELSSession._validate_response(response):
            raise Exception("ELSSession._validate_response() returned False")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        hidden_inputs = soup.find_all('input', {'type': 'hidden'})
        if not len(hidden_inputs):
            logger.warn(f"Seems error: no hidden_inputs found for GET {url}")
            # TODO: need reset self.view_related_inputs = {} ?????
        else:
            inputs_kv = {tag.get('name'): tag.get('value', '') for tag in hidden_inputs}
            self.view_state_inputs = ELSSession._extract_view_state_related(inputs_kv)
    
        self.prev_url = response.url
        logger.debug(f"Response URL for the next call: {self.prev_url}")

        return response

    def post_back(self, *args, **kwargs):
        if not self.prev_url:
            raise Exception("No prev_url is set, run get_login() first")

        kwargs['data'] = kwargs['data'] | self.view_state_inputs if kwargs.get('data') else self.view_state_inputs
        if kwargs:
            logger.debug(f"POST {self.prev_url} payload:\n{kwargs}")

        response = self.session.post(self.prev_url, *args, **kwargs)
        response.raise_for_status()
        if not ELSSession._validate_response(response):
            raise Exception("Response validation error, check logs")

        soup = BeautifulSoup(response.content, 'html.parser')
        hidden_inputs = soup.find_all('input', {'type': 'hidden'})
        inputs_kv = {tag.get('name'): tag.get('value', '') for tag in hidden_inputs}
        self.view_state_inputs = ELSSession._extract_view_state_related(inputs_kv)
    
        self.prev_url = response.url
        logger.debug(f"Response URL for the next call: {self.prev_url}")

        return response