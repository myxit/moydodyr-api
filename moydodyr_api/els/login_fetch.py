from bs4 import BeautifulSoup
from moydodyr_api.els import page_checkers
from moydodyr_api.els.elssession import ELSSession
  

def run(session: ELSSession) -> dict[str, str]:
    """Requests login form and returns form_data for the next request
    
    Returns the form data for the next submit_login() request
    """
    response = session.get("/")
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    if not page_checkers.is_login_page(response.content):
        raise Exception("Response is not login form")
    
    data = {tag.get('name'): tag.get('value', '') for tag in soup.find_all('input')}
    data.update({
        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$btOK',
    })
    del data['ctl00$ContentPlaceHolder1$btOK']
    
    return data
