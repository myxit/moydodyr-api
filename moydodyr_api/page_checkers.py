from bs4 import BeautifulSoup

def is_login_page(html_content: bytes) -> bool:
    soup = BeautifulSoup(html_content, 'html.parser')

    return soup.find(id='ctl00_ContentPlaceHolder1_LinkButtonRecoverPassword') is not None

def is_booking_confirmation_page(html_content: bytes) -> bool:
    soup = BeautifulSoup(html_content, 'html.parser')

    return len(soup.select('form[name="aspnetForm"] table tr input[type="submit"]')) == 3