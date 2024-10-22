from bs4 import BeautifulSoup
from . import page_checkers, ELSSession
  

def run(session: ELSSession):
    """Requests login form and returns form_data for the next request
    
    Returns the form data for the next submit_login() request
    """
    response = session.get_login()    
    soup = BeautifulSoup(response.content, 'html.parser')
    if not page_checkers.is_login_page(response.content):
        raise Exception("Response is not login form")
    
    return
