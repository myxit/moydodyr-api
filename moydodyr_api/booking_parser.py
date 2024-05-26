from datetime import date, timedelta
import re
from moydodyr_api.booking import Booking, AvailableLaundries

# Define the regular expression pattern
pattern_element_onclick_str = r"'(BookPass\d,\d,\d,)','(\d,\d,\d,)'"

pattern_available = r'(\d{2}:\d{2})-(\d{2}:\d{2}) \((Ledigt|Ej bokningsbar)\)'

class ParserException(Exception):
    pass


def _parse_target_arguments(input_string: str):
    """Extracts values from HTML attributes for future usage as __EVENTTARGET, __EVENTARGUMENT 
     Example: input "javascript:__doPostBack('BookPass6,5,1,','6,5,1,');"
     Expected: (True, "BookPass6,5,1,", "6,5,1,")
    """
    match = re.search(pattern_element_onclick_str, input_string)

    # Check if a match is found
    if match:
        # Extract the two strings
        event_target = match.group(1)
        event_argument = match.group(2)
        
        return (True, event_target, event_argument)
    
    return (False, None, None)

def _parse_timerange_availablity(input_string: str):
    match = re.search(pattern_available, input_string)

    # Check if a match is found
    if match:
        # Extract the start and end times
        start_time = match.group(1)
        end_time = match.group(2)
        availability = match.group(3)
        if availability in ["Ledigt", "Ej bokningsbar"]:
            return (True, start_time, end_time, availability == "Ledigt")
    return (False, None, None, None)

def _weekdays_as_date(weekdays_raw_data):
    today = date.today()
    # Extract the initial day number from the first item
    match = re.search(r'\d+', weekdays_raw_data[0])
    if not match:
        raise ValueError("No day number found in the first item")
    
    start_day = int(match.group())
    start_date = date(today.year, today.month, start_day)
    result = [start_date]
    
    # Sequentially add remaining dates
    for i in range(1, len(weekdays_raw_data)):
        start_date_inc = timedelta(days=i)
        next_day = start_date + start_date_inc
        result.append(next_day)
    
    return result

def parse_bookings(laundry_id: AvailableLaundries, raw_data, weekdays_raw_data: list[str]):
    DAYS_COUNT = 7
    # Sanity check: weekdays len always 7
    if len(weekdays_raw_data) != DAYS_COUNT:
        raise ParserException(f"weekdays_raw_data len() must be 7, actual: {len(weekdays_raw_data)}")
    # Sanity check: weekdays in sync with total time slots count
    if len(raw_data) % len(weekdays_raw_data):
        raise ParserException(f"raw_data length: #{len(raw_data)} not in sync with weekdays_raw_data length: #{weekdays_raw_data}")

    range_days = _weekdays_as_date(weekdays_raw_data)
    bookings = list(
            map(lambda tuple2: parse_booking(laundry_id, range_days[tuple2[0] % DAYS_COUNT], tuple2[1]), enumerate(raw_data)) # type: ignore
        )
    
    return bookings

def parse_booking(laundry_id, on_date: date, raw_data: tuple[str, str, str]):
    (element_name, element_onclick_str, element_title_str) = raw_data
    (is_ok, event_target, event_argument) = _parse_target_arguments(element_onclick_str)
    if not is_ok:
        raise ParserException(f"Could not parse target aguments for element='{element_name}',string='{element_onclick_str}'")
    
    (is_ok, time_from, time_to, is_available) = _parse_timerange_availablity(element_title_str)

    return Booking(laundry_id, element_name, event_target, event_argument, on_date, time_from, time_to, is_available) # type: ignore
