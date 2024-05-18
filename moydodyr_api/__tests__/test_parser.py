from datetime import date
from ..booking_parser import parse_booking, parse_bookings 
from ..booking import Booking
from testfixtures import compare
import copy

raw_available = ('ctl00$ContentPlaceHolder1$6,5,1,', "javascript:__doPostBack('BookPass6,5,1,','6,5,1,');", '19:00-23:00 (Ledigt);')
raw_not_available = ('ctl00$ContentPlaceHolder1$0,1,1,', "javascript:__doPostBack('BookPass0,1,1,','0,1,1,');", '07:00-10:00 (Ej bokningsbar)')

today = date.today()
booking_available = Booking('ctl00$ContentPlaceHolder1$6,5,1,', "BookPass6,5,1,", "6,5,1,", today, '19:00', '23:00', True)
booking_na = Booking('ctl00$ContentPlaceHolder1$0,1,1,', "BookPass0,1,1,", "0,1,1,", today, '07:00', '10:00', False)

def test_it_can_parse_available_slot():    
    compare(
        booking_available,
        parse_booking(*raw_available, today)
    )

def test_it_can_parse_unavailable_slot():
    compare(
        booking_na,
        parse_booking(*raw_not_available, today)
    )

def test_parse_bookings_ok():
    raw_dates = ['Mon10', 'Tue11', 'Wed12', 'Thu13', 'Fri14', 'Sat15', 'Sun16']
    one_week_bookings_raw = [raw_available, raw_not_available, raw_not_available, raw_available, raw_available, raw_available, raw_not_available]
    bookings = list(map(copy.deepcopy, [booking_available, booking_na, booking_na, booking_available, booking_available, booking_available, booking_na]))
    for idx, booking in enumerate(bookings):
        booking.date = booking.date.replace(day=10+idx)
        print(f"new booking.date: {booking.date}")
    for booking in bookings:
        print(f"booking.date= {booking.date}")

    compare(bookings, parse_bookings(one_week_bookings_raw, raw_dates))