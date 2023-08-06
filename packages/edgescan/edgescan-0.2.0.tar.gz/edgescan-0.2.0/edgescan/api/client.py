from typing import List, Iterator, Any, Optional, Union
from edgescan.api.authentication import DEFAULT_API_KEY
from edgescan.api.host import DEFAULT_HOST
from edgescan.constants import COLLECTION_TYPES
from edgescan.data.types.asset import Asset
from edgescan.data.types.host import Host
from edgescan.data.types.license import License
from edgescan.data.types.vulnerability import Vulnerability
from edgescan.http.session import DEFAULT_MAX_RETRIES_ON_CONNECTION_ERRORS, DEFAULT_MAX_RETRIES_ON_READ_ERRORS, \
    DEFAULT_MAX_RETRIES_ON_REDIRECT, DEFAULT_BACKOFF_FACTOR

import edgescan.data.parser as parser
import edgescan.http.session
import hodgepodge.pattern_matching
import hodgepodge.platforms
import hodgepodge.time
import urllib.parse
import datetime
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class EdgeScan:
    def __init__(
            self,
            host: str = DEFAULT_HOST,
            api_key: str = DEFAULT_API_KEY,
            max_retries_on_connection_errors: int = DEFAULT_MAX_RETRIES_ON_CONNECTION_ERRORS,
            max_retries_on_read_errors: int = DEFAULT_MAX_RETRIES_ON_READ_ERRORS,
            max_retries_on_redirects: int = DEFAULT_MAX_RETRIES_ON_REDIRECT,
            backoff_factor: float = DEFAULT_BACKOFF_FACTOR):

        self.host = host
        self.url = 'https://{}'.format(host)
        self.session = edgescan.http.session.get_session(
            api_key=api_key,
            max_retries_on_connection_errors=max_retries_on_connection_errors,
            max_retries_on_read_errors=max_retries_on_read_errors,
            max_retries_on_redirects=max_retries_on_redirects,
            backoff_factor=backoff_factor,
        )

    @property
    def hosts_url(self) -> str:
        return urllib.parse.urljoin(self.url, 'api/v1/hosts.json')

    @property
    def assets_url(self) -> str:
        return urllib.parse.urljoin(self.url, 'api/v1/assets.json')

    @property
    def vulnerabilities_url(self) -> str:
        return urllib.parse.urljoin(self.url, 'api/v1/vulnerabilities.json')

    def _iter_objects(self, url: str) -> Iterator[Any]:
        collection_type = _get_collection_type_from_url(url)

        response = self.session.get(url)
        response.raise_for_status()

        reply = response.json()
        for row in reply[collection_type]:
            row = parser.parse_object(row, collection_type=collection_type)
            if row:
                yield row

    def _count_objects(self, url: str) -> int:
        response = self.session.get(url)
        response.raise_for_status()

        reply = response.json()
        return reply['total']

    def get_host(self, host_id: int) -> Optional[Host]:
        return next(self.iter_hosts(ids=[host_id]), None)

    def get_hosts(
            self,
            ids: Optional[List[int]] = None,
            hostnames: Optional[List[str]] = None,
            asset_ids: Optional[List[int]] = None,
            asset_tags: Optional[List[str]] = None,
            ip_addresses: Optional[List[str]] = None,
            os_types: Optional[List[str]] = None,
            os_versions: Optional[List[str]] = None,
            alive: Optional[bool] = None,
            min_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            vulnerability_ids: Optional[List[int]] = None,
            cve_ids: Optional[List[str]] = None,
            min_vulnerability_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            limit: Optional[int] = None) -> List[Host]:

        return list(self.iter_hosts(
            ids=ids,
            hostnames=hostnames,
            asset_ids=asset_ids,
            asset_tags=asset_tags,
            ip_addresses=ip_addresses,
            os_types=os_types,
            os_versions=os_versions,
            alive=alive,
            min_update_time=min_update_time,
            max_update_time=max_update_time,
            vulnerability_ids=vulnerability_ids,
            cve_ids=cve_ids,
            min_vulnerability_create_time=min_vulnerability_create_time,
            max_vulnerability_create_time=max_vulnerability_create_time,
            min_vulnerability_update_time=min_vulnerability_update_time,
            max_vulnerability_update_time=max_vulnerability_update_time,
            min_vulnerability_open_time=min_vulnerability_open_time,
            max_vulnerability_open_time=max_vulnerability_open_time,
            min_vulnerability_close_time=min_vulnerability_close_time,
            max_vulnerability_close_time=max_vulnerability_close_time,
            limit=limit,
        ))

    def iter_hosts(
            self,
            ids: Optional[List[int]] = None,
            hostnames: Optional[List[str]] = None,
            asset_ids: Optional[List[int]] = None,
            asset_tags: Optional[List[str]] = None,
            ip_addresses: Optional[List[str]] = None,
            os_types: Optional[List[str]] = None,
            os_versions: Optional[List[str]] = None,
            alive: Optional[bool] = None,
            min_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            vulnerability_ids: Optional[List[int]] = None,
            cve_ids: Optional[List[str]] = None,
            min_vulnerability_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            limit: Optional[int] = None) -> Iterator[Host]:

        #: The location of a host may be specified by IP address or hostname.
        ip_addresses = set(ip_addresses) if ip_addresses else set()
        hostnames = set(hostnames) if hostnames else set()
        locations = ip_addresses | hostnames

        #: If we're filtering hosts based on related vulnerabilities.
        if vulnerability_ids or cve_ids or \
                min_vulnerability_create_time or max_vulnerability_create_time or \
                min_vulnerability_update_time or max_vulnerability_update_time or \
                min_vulnerability_open_time or max_vulnerability_open_time or \
                min_vulnerability_close_time or max_vulnerability_close_time:

            vulnerabilities = self.get_vulnerabilities(
                ids=vulnerability_ids,
                cve_ids=cve_ids,
                min_create_time=min_vulnerability_create_time,
                max_create_time=max_vulnerability_create_time,
                min_update_time=min_vulnerability_update_time,
                max_update_time=max_vulnerability_update_time,
                min_open_time=min_vulnerability_open_time,
                max_open_time=max_vulnerability_open_time,
                min_close_time=min_vulnerability_close_time,
                max_close_time=max_vulnerability_close_time,
                asset_ids=asset_ids,
            )
            locations &= {vulnerability.location for vulnerability in vulnerabilities}

        #: If we're filtering hosts based on related assets.
        if asset_tags:
            assets = self.iter_assets(ids=asset_ids, tags=asset_tags)
            asset_ids = {asset.id for asset in assets}

        i = 0
        for host in self._iter_objects(url=self.hosts_url):
            if not host.matches(
                ids=ids,
                asset_ids=asset_ids,
                locations=locations,
                os_types=os_types,
                os_versions=os_versions,
                alive=alive,
                min_update_time=min_update_time,
                max_update_time=max_update_time,
            ):
                continue

            yield host

            if limit:
                i += 1
                if i >= limit:
                    return

    def count_hosts(
            self,
            ids: Optional[List[int]] = None,
            hostnames: Optional[List[str]] = None,
            asset_ids: Optional[List[int]] = None,
            asset_tags: Optional[List[str]] = None,
            ip_addresses: Optional[List[str]] = None,
            os_types: Optional[List[str]] = None,
            os_versions: Optional[List[str]] = None,
            alive: Optional[bool] = None,
            min_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            vulnerability_ids: Optional[List[int]] = None,
            cve_ids: Optional[List[str]] = None,
            min_vulnerability_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None) -> int:

        hosts = self.iter_hosts(
            ids=ids,
            hostnames=hostnames,
            asset_ids=asset_ids,
            asset_tags=asset_tags,
            ip_addresses=ip_addresses,
            os_types=os_types,
            os_versions=os_versions,
            alive=alive,
            min_update_time=min_update_time,
            max_update_time=max_update_time,
            vulnerability_ids=vulnerability_ids,
            cve_ids=cve_ids,
            min_vulnerability_create_time=min_vulnerability_create_time,
            max_vulnerability_create_time=max_vulnerability_create_time,
            min_vulnerability_update_time=min_vulnerability_update_time,
            max_vulnerability_update_time=max_vulnerability_update_time,
            min_vulnerability_open_time=min_vulnerability_open_time,
            max_vulnerability_open_time=max_vulnerability_open_time,
            min_vulnerability_close_time=min_vulnerability_close_time,
            max_vulnerability_close_time=max_vulnerability_close_time,
        )
        return sum(1 for _ in hosts)

    def get_asset(self, asset_id: int) -> Optional[Asset]:
        return next(self.iter_assets(ids=[asset_id]), None)

    def get_assets(
            self,
            ids: Optional[List[int]] = None,
            names: Optional[List[str]] = None,
            tags: Optional[List[str]] = None,
            min_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_next_assessment_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_next_assessment_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_last_assessment_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_last_assessment_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_last_host_scan_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_last_host_scan_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            vulnerability_ids: Optional[List[int]] = None,
            cve_ids: Optional[List[str]] = None,
            min_vulnerability_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            limit: Optional[int] = None) -> List[Asset]:

        return list(self.iter_assets(
            ids=ids,
            names=names,
            tags=tags,
            min_create_time=min_create_time,
            max_create_time=max_create_time,
            min_update_time=min_update_time,
            max_update_time=max_update_time,
            min_next_assessment_time=min_next_assessment_time,
            max_next_assessment_time=max_next_assessment_time,
            min_last_assessment_time=min_last_assessment_time,
            max_last_assessment_time=max_last_assessment_time,
            min_last_host_scan_time=min_last_host_scan_time,
            max_last_host_scan_time=max_last_host_scan_time,
            vulnerability_ids=vulnerability_ids,
            cve_ids=cve_ids,
            min_vulnerability_create_time=min_vulnerability_create_time,
            max_vulnerability_create_time=max_vulnerability_create_time,
            min_vulnerability_update_time=min_vulnerability_update_time,
            max_vulnerability_update_time=max_vulnerability_update_time,
            min_vulnerability_open_time=min_vulnerability_open_time,
            max_vulnerability_open_time=max_vulnerability_open_time,
            min_vulnerability_close_time=min_vulnerability_close_time,
            max_vulnerability_close_time=max_vulnerability_close_time,
            limit=limit,
        ))

    def iter_assets(
            self,
            ids: Optional[List[int]] = None,
            names: Optional[List[str]] = None,
            tags: Optional[List[str]] = None,
            min_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_next_assessment_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_next_assessment_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_last_assessment_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_last_assessment_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_last_host_scan_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_last_host_scan_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            vulnerability_ids: Optional[List[int]] = None,
            cve_ids: Optional[List[str]] = None,
            min_vulnerability_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            limit: Optional[int] = None) -> Iterator[Asset]:

        #: If we're filtering assets based on related vulnerabilities.
        if vulnerability_ids or cve_ids or \
                min_vulnerability_create_time or max_vulnerability_create_time or \
                min_vulnerability_update_time or max_vulnerability_update_time or \
                min_vulnerability_open_time or max_vulnerability_open_time or \
                min_vulnerability_close_time or max_vulnerability_close_time:

            vulnerabilities = self.get_vulnerabilities(
                ids=vulnerability_ids,
                cve_ids=cve_ids,
                min_create_time=min_vulnerability_create_time,
                max_create_time=max_vulnerability_create_time,
                min_update_time=min_vulnerability_update_time,
                max_update_time=max_vulnerability_update_time,
                min_open_time=min_vulnerability_open_time,
                max_open_time=max_vulnerability_open_time,
                min_close_time=min_vulnerability_close_time,
                max_close_time=max_vulnerability_close_time,
                asset_ids=ids,
            )
            ids = {vulnerability.asset_id for vulnerability in vulnerabilities}

        i = 0
        for asset in self._iter_objects(url=self.assets_url):
            if not asset.matches(
                ids=ids,
                names=names,
                tags=tags,
                min_create_time=min_create_time,
                max_create_time=max_create_time,
                min_update_time=min_update_time,
                max_update_time=max_update_time,
                min_next_assessment_time=min_next_assessment_time,
                max_next_assessment_time=max_next_assessment_time,
                min_last_assessment_time=min_last_assessment_time,
                max_last_assessment_time=max_last_assessment_time,
                min_last_host_scan_time=min_last_host_scan_time,
                max_last_host_scan_time=max_last_host_scan_time,
            ):
                continue

            yield asset

            if limit:
                i += 1
                if i >= limit:
                    return

    def count_assets(
            self,
            ids: Optional[List[int]] = None,
            names: Optional[List[str]] = None,
            tags: Optional[List[str]] = None,
            min_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_next_assessment_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_next_assessment_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_last_assessment_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_last_assessment_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_last_host_scan_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_last_host_scan_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            vulnerability_ids: Optional[List[int]] = None,
            cve_ids: Optional[List[str]] = None,
            min_vulnerability_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_vulnerability_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_vulnerability_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None) -> int:

        assets = self.iter_assets(
            ids=ids,
            names=names,
            tags=tags,
            min_create_time=min_create_time,
            max_create_time=max_create_time,
            min_update_time=min_update_time,
            max_update_time=max_update_time,
            min_next_assessment_time=min_next_assessment_time,
            max_next_assessment_time=max_next_assessment_time,
            min_last_assessment_time=min_last_assessment_time,
            max_last_assessment_time=max_last_assessment_time,
            min_last_host_scan_time=min_last_host_scan_time,
            max_last_host_scan_time=max_last_host_scan_time,
            vulnerability_ids=vulnerability_ids,
            cve_ids=cve_ids,
            min_vulnerability_create_time=min_vulnerability_create_time,
            max_vulnerability_create_time=max_vulnerability_create_time,
            min_vulnerability_update_time=min_vulnerability_update_time,
            max_vulnerability_update_time=max_vulnerability_update_time,
            min_vulnerability_open_time=min_vulnerability_open_time,
            max_vulnerability_open_time=max_vulnerability_open_time,
            min_vulnerability_close_time=min_vulnerability_close_time,
            max_vulnerability_close_time=max_vulnerability_close_time,
        )
        return sum(1 for _ in assets)

    def get_vulnerability(self, vulnerability_id: int) -> Optional[Vulnerability]:
        return next(self.iter_vulnerabilities(ids=[vulnerability_id]), None)

    def get_vulnerabilities(
            self,
            ids: Optional[List[int]] = None,
            names: Optional[List[str]] = None,
            cve_ids: Optional[List[str]] = None,
            asset_ids: Optional[List[int]] = None,
            asset_tags: Optional[List[str]] = None,
            locations: Optional[List[str]] = None,
            affects_pci_compliance: Optional[bool] = None,
            include_application_layer_vulnerabilities: Optional[bool] = True,
            include_network_layer_vulnerabilities: Optional[bool] = True,
            min_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            limit: Optional[int] = None) -> List[Vulnerability]:

        return list(self.iter_vulnerabilities(
            ids=ids,
            names=names,
            cve_ids=cve_ids,
            asset_ids=asset_ids,
            asset_tags=asset_tags,
            locations=locations,
            affects_pci_compliance=affects_pci_compliance,
            include_application_layer_vulnerabilities=include_application_layer_vulnerabilities,
            include_network_layer_vulnerabilities=include_network_layer_vulnerabilities,
            min_create_time=min_create_time,
            max_create_time=max_create_time,
            min_update_time=min_update_time,
            max_update_time=max_update_time,
            min_open_time=min_open_time,
            max_open_time=max_open_time,
            min_close_time=min_close_time,
            max_close_time=max_close_time,
            limit=limit,
        ))

    def iter_vulnerabilities(
            self,
            ids: Optional[List[int]] = None,
            names: Optional[List[str]] = None,
            cve_ids: Optional[List[str]] = None,
            asset_ids: Optional[List[int]] = None,
            asset_tags: Optional[List[str]] = None,
            locations: Optional[List[str]] = None,
            affects_pci_compliance: Optional[bool] = None,
            include_application_layer_vulnerabilities: Optional[bool] = None,
            include_network_layer_vulnerabilities: Optional[bool] = None,
            min_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            limit: Optional[int] = None) -> Iterator[Vulnerability]:

        if asset_tags:
            assets = self.iter_assets(ids=asset_ids, tags=asset_tags)
            asset_ids = {asset.id for asset in assets}

        i = 0
        for vulnerability in self._iter_objects(url=self.vulnerabilities_url):
            if not vulnerability.matches(
                ids=ids,
                names=names,
                cve_ids=cve_ids,
                asset_ids=asset_ids,
                locations=locations,
                affects_pci_compliance=affects_pci_compliance,
                include_application_layer_vulnerabilities=include_application_layer_vulnerabilities,
                include_network_layer_vulnerabilities=include_network_layer_vulnerabilities,
                min_create_time=min_create_time,
                max_create_time=max_create_time,
                min_update_time=min_update_time,
                max_update_time=max_update_time,
                min_open_time=min_open_time,
                max_open_time=max_open_time,
                min_close_time=min_close_time,
                max_close_time=max_close_time,
            ):
                continue

            yield vulnerability

            if limit:
                i += 1
                if i >= limit:
                    return

    def count_vulnerabilities(
            self,
            ids: Optional[List[int]] = None,
            names: Optional[List[str]] = None,
            cve_ids: Optional[List[str]] = None,
            asset_ids: Optional[List[int]] = None,
            asset_tags: Optional[List[str]] = None,
            locations: Optional[List[str]] = None,
            affects_pci_compliance: Optional[bool] = None,
            include_application_layer_vulnerabilities: Optional[bool] = None,
            include_network_layer_vulnerabilities: Optional[bool] = None,
            min_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_create_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_update_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_open_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            min_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None,
            max_close_time: Optional[Union[str, int, float, datetime.datetime, datetime.date]] = None) -> int:

        vulnerabilities = self.iter_vulnerabilities(
            ids=ids,
            names=names,
            cve_ids=cve_ids,
            asset_ids=asset_ids,
            asset_tags=asset_tags,
            locations=locations,
            affects_pci_compliance=affects_pci_compliance,
            include_application_layer_vulnerabilities=include_application_layer_vulnerabilities,
            include_network_layer_vulnerabilities=include_network_layer_vulnerabilities,
            min_create_time=min_create_time,
            max_create_time=max_create_time,
            min_update_time=min_update_time,
            max_update_time=max_update_time,
            min_open_time=min_open_time,
            max_open_time=max_open_time,
            min_close_time=min_close_time,
            max_close_time=max_close_time,
        )
        return sum(1 for _ in vulnerabilities)

    def get_license(self, license_id: int) -> Optional[License]:
        return next(self.iter_licenses(ids=[license_id]), None)

    def get_licenses(
            self,
            ids: Optional[List[int]] = None,
            names: Optional[List[str]] = None,
            expired: Optional[bool] = None,
            limit: Optional[int] = None) -> List[License]:

        return list(self.iter_licenses(
            ids=ids,
            names=names,
            expired=expired,
            limit=limit,
        ))

    def iter_licenses(
            self,
            ids: Optional[List[int]] = None,
            names: Optional[List[str]] = None,
            expired: Optional[bool] = None,
            limit: Optional[int] = None) -> Iterator[License]:

        i = 0
        for row in self._iter_licenses():
            if ids and row.id not in ids:
                continue

            if names and not hodgepodge.pattern_matching.str_matches_glob(row.name, names):
                continue

            if expired is not None and row.expired != expired:
                continue

            yield row

            if limit:
                i += 1
                if i >= limit:
                    return

    def _iter_licenses(self) -> Iterator[License]:
        seen = set()
        for asset in self.iter_assets():
            active_license = asset.active_license
            if active_license.id not in seen:
                seen.add(active_license.id)
                yield active_license

    def count_licenses(
            self,
            ids: Optional[List[int]] = None,
            names: Optional[List[str]] = None,
            expired: Optional[bool] = None) -> int:

        licenses = self.iter_licenses(
            ids=ids,
            names=names,
            expired=expired,
        )
        return sum(1 for _ in licenses)


def _get_collection_type_from_url(url: str) -> str:
    v = urllib.parse.urlsplit(url).path.split('/')[-1]
    if v.endswith('.json'):
        v = v[:-5]

    if v not in COLLECTION_TYPES:
        raise ValueError("Failed to parse collection type from URL: {} - got '{}' - allowed: {}".format(
            url, v, COLLECTION_TYPES
        ))
    return v
