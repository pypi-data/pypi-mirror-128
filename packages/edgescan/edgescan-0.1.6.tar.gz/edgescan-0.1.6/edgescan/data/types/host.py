from dataclasses import dataclass
from typing import Optional, List
from edgescan.data.types.object import Object

import hodgepodge.platforms
import datetime


@dataclass(frozen=True)
class Host(Object):
    id: int
    asset_id: int
    location: str
    hostnames: List[str]
    label: Optional[str]
    status: str
    updated_at: datetime.datetime
    os_name: str
    apis_detected: bool

    @property
    def os_type(self) -> str:
        return hodgepodge.platforms.parse_os_type(self.os_name)

    @property
    def os_version(self) -> str:
        return self.os_version

    @property
    def update_time(self) -> datetime.datetime:
        return self.updated_at

    def is_alive(self) -> bool:
        return self.status == 'alive'
