from dataclasses import dataclass
from edgescan.data.types.object import Object

import datetime


@dataclass(frozen=True)
class Assessment(Object):
    id: int
    type: str
    status: str
    created_at: datetime.datetime

    @property
    def create_time(self) -> datetime.datetime:
        return self.created_at
