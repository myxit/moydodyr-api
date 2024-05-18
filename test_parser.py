import unittest
from asp_form_commands.booking import Booking

class TestBookingParser(unittest.TestCase):
            
    def test_target_arguments_parsing(self):
        (is_ok, event_target, event_argument) = Booking.parse_target_arguments("javascript:__doPostBack('BookPass0,1,1,','0,1,1,');")
        self.assertEqual(is_ok, True)
        self.assertEqual(event_target, "BookPass0,1,1,")
        self.assertEqual(event_argument, "0,1,1,")
        
    def test_parse_timerange_availability(self):
        (is_ok, time_start, time_end, is_available) = Booking.parse_timerange_availablity("10:00-13:00 (Ej bokningsbar)")
        self.assertEqual(is_ok, True)
        self.assertEqual(time_start, "10:00")
        self.assertEqual(time_end, "13:00")
        self.assertEqual(is_available, False)
        
    def test_parse_timerange_availability2(self):
        (is_ok, time_start, time_end, is_available) = Booking.parse_timerange_availablity("10:00-13:00 (Ledigt)")
        self.assertEqual(is_ok, True)
        self.assertEqual(time_start, "10:00")
        self.assertEqual(time_end, "13:00")
        self.assertEqual(is_available, True)
    
    def test_parse_timerange_availability_ERROR(self):
        (is_ok, *_) = Booking.parse_timerange_availablity("10:0-13:00(Leigt)")
        self.assertEqual(is_ok, False)
        
        
        
if __name__ == '__main___':
    unittest.main()