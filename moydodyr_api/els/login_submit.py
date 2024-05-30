from bs4 import BeautifulSoup
from moydodyr_api.els.elssession import ELSSession
  

def run(session: ELSSession, username: str, password: str):
    """Posts login data

    Returns: state
    """
    request_data = {
        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$btOK',
        '__EVENTARGUMENT': None,
        'ctl00$MessageType': 'ERROR',
        'ctl00$ContentPlaceHolder1$tbUsername': username, 
        'ctl00$ContentPlaceHolder1$tbPassword': password
    }
    response = session.post("/Default.aspx", request_data)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    inputs_data = {tag.get('name'): tag.get('value', '') for tag in soup.find_all('input')}
    REQUIRED_INPUTS_COUNT = 7
    if len(inputs_data) < REQUIRED_INPUTS_COUNT:
        raise Exception(f"inputs number less than required={REQUIRED_INPUTS_COUNT}, actual={len(inputs_data)}")        
    
    return inputs_data