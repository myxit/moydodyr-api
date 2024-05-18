class Booking:
    def __init__(self, element_name, event_target, event_argument, date, time_from, time_to, is_available):
        self.element_name = element_name
        self.event_target = event_target
        self.event_argument = event_argument
        self.date = date
        self.time_from = time_from
        self.time_to = time_to
        self.is_available = is_available
    
    def __repr__(self) -> str:
        return f"""
Booking(
    element_name={self.element_name}, 
    event_target={self.event_target},
    event_argument={self.event_argument},
    date={self.date},
    time_from={self.time_from},
    time_to={self.time_to},
    is_available={self.is_available}
)
"""