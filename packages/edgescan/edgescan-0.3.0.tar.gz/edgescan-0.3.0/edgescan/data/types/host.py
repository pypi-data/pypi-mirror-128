from dataclasses import dataclass
from typing import Optional, List, Union
from edgescan.data.types.object import Object

import hodgepodge.pattern_matching
import hodgepodge.platforms
import hodgepodge.time
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
        return self.os_name

    @property
    def locations(self) -> List[str]:
        return [self.location] + self.hostnames

    @property
    def update_time(self) -> datetime.datetime:
        return self.updated_at

    def is_alive(self) -> bool:
        return self.status == 'alive'

    def matches(
            self, 
            ids: Optional[List[int]] = None,
            asset_ids: Optional[List[int]] = None,
            locations: Optional[List[str]] = None,
            os_types: Optional[List[str]] = None,
            os_versions: Optional[List[str]] = None,
            alive: Optional[bool] = None,
            min_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None) -> bool:

        #: Filter hosts by ID.
        if ids and self.id not in ids:
            return False

        #: Filter hosts by asset ID.
        if asset_ids and self.asset_id not in asset_ids:
            return False

        #: Filter hosts by IP address and/or hostname.
        if locations and not hodgepodge.pattern_matching.str_matches_glob(self.locations, locations):
            return False

        #: Filter hosts by OS type.
        if os_types:
            os_types = [hodgepodge.platforms.parse_os_type(os_type) for os_type in os_types]
            if not hodgepodge.pattern_matching.str_matches_glob(self.os_type, os_types):
                return False

        #: Filter hosts by OS version.
        if os_versions and not hodgepodge.pattern_matching.str_matches_glob(self.os_version, os_versions):
            return False

        #: Filter hosts based on whether they're dead or alive.
        if alive is not None and alive != self.is_alive():
            return False

        #: Filter hosts based on when they were last seen.
        if (min_update_time or max_update_time) and \
                not hodgepodge.time.in_range(self.update_time, min_update_time, max_update_time):
            return False
        return True
