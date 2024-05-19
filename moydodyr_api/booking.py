from datetime import date

from moydodyr_api.els.types import AvailableLaundries


class Booking:
    def __init__(self, laundry_id: AvailableLaundries, element_name: str, event_target: str, event_argument: str, date: date, time_from, time_to, is_available: bool):
        self._id = self.make_id(laundry_id.name, date, time_from, time_to)
        self._date = date
        self.form_data = {
            '__EVENTTARGET': event_target,
            '__EVENTARGUMENT': event_argument,
            element_name: None,
        }
        self.time_from = time_from
        self.time_to = time_to
        self.is_available = is_available
    @staticmethod
    def make_id(laundry_id: str, date: date, time_from: str, time_to: str) -> str:
        return ':'.join([laundry_id, date.isoformat(), time_from + '-' + time_to])
    
    @property
    def id(self):
        return self._id
    
    @property
    def date(self):
        return self._date

    def __repr__(self) -> str:
        return f"""
Booking(
    id={self.id},
    form_data=<...missed...>,
    date={self.date},
    time_from={self.time_from},
    time_to={self.time_to},
    is_available={self.is_available}
)
"""