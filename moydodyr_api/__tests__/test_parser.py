from datetime import date
from ..booking_parser import parse_booking, parse_bookings 
from ..booking import AvailableLaundries, Booking
from testfixtures import compare
import copy
from freezegun import freeze_time

raw_available = ('ctl00$ContentPlaceHolder1$6,5,1,', "javascript:__doPostBack('BookPass6,5,1,','6,5,1,');", '19:00-23:00 (Ledigt);')
raw_not_available = ('ctl00$ContentPlaceHolder1$0,1,1,', "javascript:__doPostBack('BookPass0,1,1,','0,1,1,');", '07:00-10:00 (Ej bokningsbar)')

today = date(2024, 5, 13)
booking_available = Booking(AvailableLaundries.LAUNDRY_3, 'ctl00$ContentPlaceHolder1$6,5,1,', "BookPass6,5,1,", "6,5,1,", today, '19:00', '23:00', True)
booking_na = Booking(AvailableLaundries.LAUNDRY_3, 'ctl00$ContentPlaceHolder1$0,1,1,', "BookPass0,1,1,", "0,1,1,", today, '07:00', '10:00', False)

def test_it_can_parse_available_slot():    
    compare(
        booking_available,
        parse_booking(AvailableLaundries.LAUNDRY_3, today, raw_available)
    )

def test_it_can_parse_unavailable_slot():
    compare(
        booking_na,
        parse_booking(AvailableLaundries.LAUNDRY_3, today, raw_not_available)
    )

@freeze_time("2024-05-13")
def test_parse_bookings_ok():
    START_DAY = 13
    raw_dates = [f"Mon{START_DAY}", 'Tue14', 'Wed15', 'Thu16', 'Fri17', 'Sat18', 'Sun19']
    one_week_bookings_raw = [raw_available, raw_not_available, raw_not_available, raw_available, raw_available, raw_available, raw_not_available]
    bookings = list(map(copy.deepcopy, [booking_available, booking_na, booking_na, booking_available, booking_available, booking_available, booking_na]))
    for idx, booking in enumerate(bookings):
        date_to_set = booking.date.replace(day=START_DAY+idx)
        booking._id = Booking.make_id(AvailableLaundries.LAUNDRY_3.name, date_to_set, booking.time_from, booking.time_to)
        booking._date = date_to_set

    compare(bookings, parse_bookings(AvailableLaundries.LAUNDRY_3, one_week_bookings_raw, raw_dates))