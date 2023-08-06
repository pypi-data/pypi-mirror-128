from typing import Optional
from dataclasses import dataclass
from edgescan.data.types.object import Object

import datetime


@dataclass(frozen=True)
class License(Object):
    id: int
    name: str
    license_type_id: int
    license_type_name: str
    asset_id: Optional[int]
    order_id: int
    start_date: datetime.datetime
    end_date: datetime.datetime
    expired: bool
    status: Optional[str]

    def is_expired(self):
        return self.expired
