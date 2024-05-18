import datetime
import re

# Define the regular expression pattern
pattern_element_onclick_str = r"'(BookPass\d,\d,\d,)','(\d,\d,\d,)'"

# input_string = "javascript:__doPostBack('BookPass1,1,1,','1,1,1,');"
def parse_target_arguments(input_string: str):
    match = re.search(pattern_element_onclick_str, input_string)

    # Check if a match is found
    if match:
        # Extract the two strings
        event_target = match.group(1)
        event_argument = match.group(2)
        
        return (True, event_target, event_argument)
    
    return (False, None, None)


pattern_available = r'(\d{2}:\d{2})-(\d{2}:\d{2}) \((Ledigt|Ej bokningsbar)\)'


def parse_timerange_availablity(input_string: str):
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


class ParserException(Exception):
    pass


class Booking:
    def __init__(self, element_name, event_target, event_argument, date, time_from, time_to, is_available):
        self.element_name = element_name
        self.event_target = event_target
        self.event_argument = event_argument
        self.date = date
        self.time_from = time_from
        self.time_to = time_to
        self.is_available = is_available
        self.updated_at = datetime.datetime.now()
    
    @staticmethod
    def parse_target_arguments(input_string: str):
        match = re.search(pattern_element_onclick_str, input_string)

        # Check if a match is found
        if match:
            # Extract the two strings
            event_target = match.group(1)
            event_argument = match.group(2)
            
            return (True, event_target, event_argument)
        
        return (False, None, None)

    @staticmethod
    def parse_timerange_availablity(input_string: str):
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
    
    @staticmethod
    def make_of(element_name: str, element_onclick_str: str, element_title_str: str):
        (is_ok, event_target, event_argument) = parse_target_arguments(element_onclick_str)
        if not is_ok:
            raise ParserException(f"Could not parse target aguments for element='{element_name}',string='{element_onclick_str}'")
        
        (is_ok, time_from, time_to, is_available) = parse_timerange_availablity(element_title_str)

        return Booking(element_name, event_target, event_argument, "date", time_from, time_to, is_available)

    def __repr__(self) -> str:
        return f"""
Booking(
    element_name={self.element_name}, 
    event_target={self.event_target},
    event_argument={self.event_argument},
    date={self.date},
    time_from={self.time_from},
    time_to={self.time_to},
    is_available={self.is_available},
    updated_at={self.updated_at}
)
"""