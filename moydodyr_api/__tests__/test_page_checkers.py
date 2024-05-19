from testfixtures import compare

from moydodyr_api.page_checkers import is_booking_confirmation_page, is_login_page

def test_is_login_page():
    CONTENT_WITH_FORGOT_PASSWORD_LINK = """<form><a id="ctl00_ContentPlaceHolder1_LinkButtonRecoverPassword" href="javascript:__doPostBack(\'ctl00$ContentPlaceHolder1$LinkButtonRecoverPassword\',\'\')">Glömt lösenord</a></form>"""
    CONTENT_WITHOUT_LINK = """<form><a id="not_it" href="javascript:__doPostBack(\'ctl00$ContentPlaceHolder1$LinkButtonRecoverPassword\',\'\')">Glömt lösenord</a></form>"""
    compare(True, is_login_page(CONTENT_WITH_FORGOT_PASSWORD_LINK.encode('utf-8')))
    compare(False, is_login_page(CONTENT_WITHOUT_LINK.encode('utf-8')))

def test_is_booking_confirmation_page():
    CONTENT_CONTAINS_ELEMENTS = """<form name="aspnetForm">
        <table>
            <tr>
                <input type="submit" id="ctl00_ContentPlaceHolder1_bt2Maskingrupp0" value="first" />
                <input type="submit" id="ctl00_ContentPlaceHolder1_btMaskingruppBack.ELS_M" value="second" />
                <input type="submit" id="ctl00_ContentPlaceHolder1_btMaskingruppRandom.ELS_M" value="third" />
            </tr>
        </table>
    </form>"""
    CONTENT_WITH_FORGOT_PASSWORD_LINK = """<form><a id="ctl00_ContentPlaceHolder1_LinkButtonRecoverPassword" href="javascript:__doPostBack(\'ctl00$ContentPlaceHolder1$LinkButtonRecoverPassword\',\'\')">Glömt lösenord</a></form>"""
    
    compare(True, is_booking_confirmation_page(CONTENT_CONTAINS_ELEMENTS.encode('utf-8')))
    compare(False, is_booking_confirmation_page(CONTENT_WITH_FORGOT_PASSWORD_LINK.encode('utf-8')))
    