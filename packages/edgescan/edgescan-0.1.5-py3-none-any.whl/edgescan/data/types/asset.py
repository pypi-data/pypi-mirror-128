from dataclasses import dataclass
from typing import List, Any, Optional
from edgescan.data.types.assessment import Assessment
from edgescan.data.types.license import License
from edgescan.data.types.location_specifier import LocationSpecifier
from edgescan.data.types.object import Object

import datetime


@dataclass(frozen=True)
class Asset(Object):
    asset_status: str
    authenticated: bool
    active_license: License
    blocked_status: str
    created_at: datetime.datetime
    current_assessment: Assessment
    host_count: int
    hostname: str
    id: int
    last_assessment_date: datetime.datetime
    last_host_scan: datetime.datetime
    linked_assets: List[Any]
    location_specifiers: List[LocationSpecifier]
    name: str
    network_access: str
    next_assessment_date: Optional[datetime.datetime]
    pci_enabled: Optional[bool]
    priority: int
    tags: List[str]
    targeting_mode: str
    type: str
    updated_at: datetime.datetime

    @property
    def create_time(self):
        return self.created_at

    @property
    def update_time(self):
        return self.updated_at
