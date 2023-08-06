import datetime
from dataclasses import dataclass


@dataclass(order=True, frozen=True)
class Slot:
    """Class representing a date & a moment."""
    date: datetime.date
    moment: str

    def __str__(self):
        if self.moment is None or self.moment == '':
            return f'{self.date.isoformat()}'
        else:
            return f'{self.date.isoformat()} ({self.moment})'
