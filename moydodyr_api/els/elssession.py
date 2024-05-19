from requests import Session
from urllib.parse import urljoin

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

    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self.base_url, url)
        return super().request(method, joined_url, *args, **kwargs)