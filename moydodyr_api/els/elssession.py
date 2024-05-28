import logging
from bs4 import BeautifulSoup
from requests import Session
from urllib.parse import urljoin

logger = logging.getLogger()

class ELSSession(Session):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Origin": base_url,
            "Pragma": "no-cache",
            "Referer": base_url + "/Default.aspx",
        })
        self.view_related_inputs = {}

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

        return result

    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self.base_url, url)
        if method == 'POST':
            kwargs['data'] = kwargs['data'] | self.view_related_inputs if kwargs['data'] else self.view_related_inputs
        response = super().request(method, joined_url, *args, **kwargs)
        soup = BeautifulSoup(response.content, 'html.parser')
        hidden_inputs = soup.find_all('input', {'type': 'hidden'})
        if not len(hidden_inputs):
            logger.warn(f"no hidden_inputs found for {method} {joined_url}")
            # self.view_related_inputs = {} ?????
        else:
            inputs_kv = {tag.get('name'): tag.get('value', '') for tag in hidden_inputs}
            self.view_related_inputs = ELSSession._extract_view_state_related(inputs_kv)

        return response