from typing import Optional
from edgescan.api.client import EdgeScan
from edgescan.constants import DEFAULT_INDENT, SORT_KEYS_BY_DEFAULT
from hodgepodge.time import HOUR, DAY, MONTH

import hodgepodge.time
import edgescan.cli.click as click
import collections
import json


@click.group()
@click.pass_context
def vulnerabilities(_):
    """
    Query or count vulnerabilities.
    """
    pass


@vulnerabilities.command()
@click.option('--id', 'vulnerability_id', type=int, required=True)
@click.pass_context
def get_vulnerability(ctx: click.Context, vulnerability_id: int):
    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    vulnerability = api.get_vulnerability(vulnerability_id)
    if vulnerability:
        click.echo(vulnerability.to_json())


@vulnerabilities.command()
@click.option('--ids')
@click.option('--names')
@click.option('--cve-ids')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--locations')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--affects-pci-compliance/--does-not-affect-pci-compliance', default=None)
@click.option('--include-application-layer-vulnerabilities/--exclude-application-layer-vulnerabilities', default=True)
@click.option('--include-network-layer-vulnerabilities/--exclude-network-layer-vulnerabilities', default=True)
@click.option('--min-create-time')
@click.option('--max-create-time')
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--min-open-time')
@click.option('--max-open-time')
@click.option('--min-close-time')
@click.option('--max-close-time')
@click.option('--limit', type=int)
@click.pass_context
def get_vulnerabilities(
        ctx: click.Context,
        ids: Optional[str],
        names: Optional[str],
        cve_ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        locations: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        affects_pci_compliance: Optional[bool],
        include_application_layer_vulnerabilities: Optional[bool],
        include_network_layer_vulnerabilities: Optional[bool],
        min_create_time: Optional[str],
        max_create_time: Optional[str],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        min_open_time: Optional[str],
        max_open_time: Optional[str],
        min_close_time: Optional[str],
        max_close_time: Optional[str],
        limit: int):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    for vulnerability in api.iter_vulnerabilities(
            ids=click.str_to_ints(ids),
            names=click.str_to_strs(names),
            cve_ids=click.str_to_strs(cve_ids),
            asset_ids=click.str_to_ints(asset_ids),
            asset_tags=click.str_to_strs(asset_tags),
            locations=click.str_to_strs(locations),
            os_types=click.str_to_strs(os_types),
            os_versions=click.str_to_strs(os_versions),
            affects_pci_compliance=affects_pci_compliance,
            include_application_layer_vulnerabilities=include_application_layer_vulnerabilities,
            include_network_layer_vulnerabilities=include_network_layer_vulnerabilities,
            min_create_time=click.str_to_datetime(min_create_time),
            max_create_time=click.str_to_datetime(max_create_time),
            min_update_time=click.str_to_datetime(min_update_time),
            max_update_time=click.str_to_datetime(max_update_time),
            min_open_time=click.str_to_datetime(min_open_time),
            max_open_time=click.str_to_datetime(max_open_time),
            min_close_time=click.str_to_datetime(min_close_time),
            max_close_time=click.str_to_datetime(max_close_time),
            limit=limit,
    ):
        click.echo(vulnerability.to_json())


@vulnerabilities.command()
@click.option('--ids')
@click.option('--names')
@click.option('--cve-ids')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--locations')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--affects-pci-compliance/--does-not-affect-pci-compliance', default=None)
@click.option('--include-application-layer-vulnerabilities/--exclude-application-layer-vulnerabilities', default=True)
@click.option('--include-network-layer-vulnerabilities/--exclude-network-layer-vulnerabilities', default=True)
@click.option('--min-create-time')
@click.option('--max-create-time')
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--min-open-time')
@click.option('--max-open-time')
@click.option('--min-close-time')
@click.option('--max-close-time')
@click.pass_context
def count_vulnerabilities(
        ctx: click.Context,
        ids: Optional[str],
        names: Optional[str],
        cve_ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        locations: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        affects_pci_compliance: Optional[bool],
        include_application_layer_vulnerabilities: Optional[bool],
        include_network_layer_vulnerabilities: Optional[bool],
        min_create_time: Optional[str],
        max_create_time: Optional[str],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        min_open_time: Optional[str],
        max_open_time: Optional[str],
        min_close_time: Optional[str],
        max_close_time: Optional[str]):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    total = api.count_vulnerabilities(
        ids=click.str_to_ints(ids),
        names=click.str_to_strs(names),
        cve_ids=click.str_to_strs(cve_ids),
        asset_ids=click.str_to_ints(asset_ids),
        asset_tags=click.str_to_strs(asset_tags),
        locations=click.str_to_strs(locations),
        os_types=click.str_to_strs(os_types),
        os_versions=click.str_to_strs(os_versions),
        affects_pci_compliance=affects_pci_compliance,
        include_application_layer_vulnerabilities=include_application_layer_vulnerabilities,
        include_network_layer_vulnerabilities=include_network_layer_vulnerabilities,
        min_create_time=click.str_to_datetime(min_create_time),
        max_create_time=click.str_to_datetime(max_create_time),
        min_update_time=click.str_to_datetime(min_update_time),
        max_update_time=click.str_to_datetime(max_update_time),
        min_open_time=click.str_to_datetime(min_open_time),
        max_open_time=click.str_to_datetime(max_open_time),
        min_close_time=click.str_to_datetime(min_close_time),
        max_close_time=click.str_to_datetime(max_close_time),
    )
    click.echo(total)


@vulnerabilities.command()
@click.option('--ids')
@click.option('--names')
@click.option('--cve-ids')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--locations')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--affects-pci-compliance/--does-not-affect-pci-compliance', default=None)
@click.option('--include-application-layer-vulnerabilities/--exclude-application-layer-vulnerabilities', default=True)
@click.option('--include-network-layer-vulnerabilities/--exclude-network-layer-vulnerabilities', default=True)
@click.option('--min-create-time')
@click.option('--max-create-time')
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--min-open-time')
@click.option('--max-open-time')
@click.option('--min-close-time')
@click.option('--max-close-time')
@click.pass_context
def count_vulnerabilities_by_asset_group_name(
        ctx: click.Context,
        ids: Optional[str],
        names: Optional[str],
        cve_ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        locations: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        affects_pci_compliance: Optional[bool],
        include_application_layer_vulnerabilities: Optional[bool],
        include_network_layer_vulnerabilities: Optional[bool],
        min_create_time: Optional[str],
        max_create_time: Optional[str],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        min_open_time: Optional[str],
        max_open_time: Optional[str],
        min_close_time: Optional[str],
        max_close_time: Optional[str]):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])

    #: Count vulnerabilities by `asset.id`.
    vulnerabilities_by_asset_id = collections.defaultdict(int)
    for vulnerability in api.get_vulnerabilities(
            ids=click.str_to_ints(ids),
            names=click.str_to_strs(names),
            cve_ids=click.str_to_strs(cve_ids),
            asset_ids=click.str_to_ints(asset_ids),
            asset_tags=click.str_to_strs(asset_tags),
            locations=click.str_to_strs(locations),
            os_types=click.str_to_strs(os_types),
            os_versions=click.str_to_strs(os_versions),
            affects_pci_compliance=affects_pci_compliance,
            include_application_layer_vulnerabilities=include_application_layer_vulnerabilities,
            include_network_layer_vulnerabilities=include_network_layer_vulnerabilities,
            min_create_time=click.str_to_datetime(min_create_time),
            max_create_time=click.str_to_datetime(max_create_time),
            min_update_time=click.str_to_datetime(min_update_time),
            max_update_time=click.str_to_datetime(max_update_time),
            min_open_time=click.str_to_datetime(min_open_time),
            max_open_time=click.str_to_datetime(max_open_time),
            min_close_time=click.str_to_datetime(min_close_time),
            max_close_time=click.str_to_datetime(max_close_time),
    ):
        vulnerabilities_by_asset_id[vulnerability.asset_id] += 1

    #: List the number of vulnerabilities by `asset.name`.
    tally = {}
    for asset in api.get_assets():
        if asset.id in vulnerabilities_by_asset_id:
            tally[asset.name] = vulnerabilities_by_asset_id[asset.id]

    click.echo(json.dumps(tally, indent=DEFAULT_INDENT, sort_keys=SORT_KEYS_BY_DEFAULT))


@vulnerabilities.command()
@click.option('--ids')
@click.option('--names')
@click.option('--cve-ids')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--locations')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--affects-pci-compliance/--does-not-affect-pci-compliance', default=None)
@click.option('--include-application-layer-vulnerabilities/--exclude-application-layer-vulnerabilities', default=True)
@click.option('--include-network-layer-vulnerabilities/--exclude-network-layer-vulnerabilities', default=True)
@click.option('--min-create-time')
@click.option('--max-create-time')
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--min-open-time')
@click.option('--max-open-time')
@click.option('--min-close-time')
@click.option('--max-close-time')
@click.pass_context
def count_vulnerabilities_by_location(
        ctx: click.Context,
        ids: Optional[str],
        names: Optional[str],
        cve_ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        locations: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        affects_pci_compliance: Optional[bool],
        include_application_layer_vulnerabilities: Optional[bool],
        include_network_layer_vulnerabilities: Optional[bool],
        min_create_time: Optional[str],
        max_create_time: Optional[str],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        min_open_time: Optional[str],
        max_open_time: Optional[str],
        min_close_time: Optional[str],
        max_close_time: Optional[str]):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])

    tally = collections.defaultdict(int)
    for vulnerability in api.get_vulnerabilities(
            ids=click.str_to_ints(ids),
            names=click.str_to_strs(names),
            cve_ids=click.str_to_strs(cve_ids),
            asset_ids=click.str_to_ints(asset_ids),
            asset_tags=click.str_to_strs(asset_tags),
            locations=click.str_to_strs(locations),
            os_types=click.str_to_strs(os_types),
            os_versions=click.str_to_strs(os_versions),
            affects_pci_compliance=affects_pci_compliance,
            include_application_layer_vulnerabilities=include_application_layer_vulnerabilities,
            include_network_layer_vulnerabilities=include_network_layer_vulnerabilities,
            min_create_time=click.str_to_datetime(min_create_time),
            max_create_time=click.str_to_datetime(max_create_time),
            min_update_time=click.str_to_datetime(min_update_time),
            max_update_time=click.str_to_datetime(max_update_time),
            min_open_time=click.str_to_datetime(min_open_time),
            max_open_time=click.str_to_datetime(max_open_time),
            min_close_time=click.str_to_datetime(min_close_time),
            max_close_time=click.str_to_datetime(max_close_time),
    ):
        tally[vulnerability.location] += 1
    click.echo(json.dumps(tally, indent=DEFAULT_INDENT, sort_keys=SORT_KEYS_BY_DEFAULT))


@vulnerabilities.command()
@click.option('--ids')
@click.option('--names')
@click.option('--cve-ids')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--locations')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--affects-pci-compliance/--does-not-affect-pci-compliance', default=None)
@click.option('--include-application-layer-vulnerabilities/--exclude-application-layer-vulnerabilities', default=True)
@click.option('--include-network-layer-vulnerabilities/--exclude-network-layer-vulnerabilities', default=True)
@click.option('--min-create-time')
@click.option('--max-create-time')
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--min-open-time')
@click.option('--max-open-time')
@click.option('--min-close-time')
@click.option('--max-close-time')
@click.pass_context
def count_vulnerabilities_by_cve_id(
        ctx: click.Context,
        ids: Optional[str],
        names: Optional[str],
        cve_ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        locations: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        affects_pci_compliance: Optional[bool],
        include_application_layer_vulnerabilities: Optional[bool],
        include_network_layer_vulnerabilities: Optional[bool],
        min_create_time: Optional[str],
        max_create_time: Optional[str],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        min_open_time: Optional[str],
        max_open_time: Optional[str],
        min_close_time: Optional[str],
        max_close_time: Optional[str]):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])

    tally = collections.defaultdict(int)
    for vulnerability in api.get_vulnerabilities(
            ids=click.str_to_ints(ids),
            names=click.str_to_strs(names),
            cve_ids=click.str_to_strs(cve_ids),
            asset_ids=click.str_to_ints(asset_ids),
            asset_tags=click.str_to_strs(asset_tags),
            locations=click.str_to_strs(locations),
            os_types=click.str_to_strs(os_types),
            os_versions=click.str_to_strs(os_versions),
            affects_pci_compliance=affects_pci_compliance,
            include_application_layer_vulnerabilities=include_application_layer_vulnerabilities,
            include_network_layer_vulnerabilities=include_network_layer_vulnerabilities,
            min_create_time=click.str_to_datetime(min_create_time),
            max_create_time=click.str_to_datetime(max_create_time),
            min_update_time=click.str_to_datetime(min_update_time),
            max_update_time=click.str_to_datetime(max_update_time),
            min_open_time=click.str_to_datetime(min_open_time),
            max_open_time=click.str_to_datetime(max_open_time),
            min_close_time=click.str_to_datetime(min_close_time),
            max_close_time=click.str_to_datetime(max_close_time),
    ):
        for cve in vulnerability.cves:
            tally[cve] += 1
    click.echo(json.dumps(tally, indent=DEFAULT_INDENT, sort_keys=SORT_KEYS_BY_DEFAULT))


@vulnerabilities.command()
@click.option('--ids')
@click.option('--names')
@click.option('--cve-ids')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--locations')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--affects-pci-compliance/--does-not-affect-pci-compliance', default=None)
@click.option('--include-application-layer-vulnerabilities/--exclude-application-layer-vulnerabilities', default=True)
@click.option('--include-network-layer-vulnerabilities/--exclude-network-layer-vulnerabilities', default=True)
@click.option('--min-create-time')
@click.option('--max-create-time')
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--min-open-time')
@click.option('--max-open-time')
@click.option('--min-close-time')
@click.option('--max-close-time')
@click.pass_context
def count_vulnerabilities_by_os_type(
        ctx: click.Context,
        ids: Optional[str],
        names: Optional[str],
        cve_ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        locations: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        affects_pci_compliance: Optional[bool],
        include_application_layer_vulnerabilities: Optional[bool],
        include_network_layer_vulnerabilities: Optional[bool],
        min_create_time: Optional[str],
        max_create_time: Optional[str],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        min_open_time: Optional[str],
        max_open_time: Optional[str],
        min_close_time: Optional[str],
        max_close_time: Optional[str]):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])

    #: Lookup hosts.
    hosts = api.get_hosts(
        asset_ids=click.str_to_ints(asset_ids),
        asset_tags=click.str_to_strs(asset_tags),
        os_types=click.str_to_strs(os_types),
        os_versions=click.str_to_strs(os_versions),
        min_vulnerability_create_time=click.str_to_datetime(min_create_time),
        max_vulnerability_create_time=click.str_to_datetime(max_create_time),
        min_vulnerability_update_time=click.str_to_datetime(min_update_time),
        max_vulnerability_update_time=click.str_to_datetime(max_update_time),
        min_vulnerability_open_time=click.str_to_datetime(min_open_time),
        max_vulnerability_open_time=click.str_to_datetime(max_open_time),
        min_vulnerability_close_time=click.str_to_datetime(min_close_time),
        max_vulnerability_close_time=click.str_to_datetime(max_close_time),
    )
    hosts_by_id = dict((host.id, host) for host in hosts)
    host_ids_by_location = collections.defaultdict(set)
    for host in hosts:
        host_ids_by_location[host.location].add(host.id)

    #: Lookup vulnerabilities.
    tally = collections.defaultdict(int)
    for vulnerability in api.get_vulnerabilities(
            ids=click.str_to_ints(ids),
            names=click.str_to_strs(names),
            cve_ids=click.str_to_strs(cve_ids),
            asset_ids=click.str_to_ints(asset_ids),
            asset_tags=click.str_to_strs(asset_tags),
            locations=click.str_to_strs(locations),
            os_types=click.str_to_strs(os_types),
            os_versions=click.str_to_strs(os_versions),
            affects_pci_compliance=affects_pci_compliance,
            include_application_layer_vulnerabilities=include_application_layer_vulnerabilities,
            include_network_layer_vulnerabilities=include_network_layer_vulnerabilities,
            min_create_time=click.str_to_datetime(min_create_time),
            max_create_time=click.str_to_datetime(max_create_time),
            min_update_time=click.str_to_datetime(min_update_time),
            max_update_time=click.str_to_datetime(max_update_time),
            min_open_time=click.str_to_datetime(min_open_time),
            max_open_time=click.str_to_datetime(max_open_time),
            min_close_time=click.str_to_datetime(min_close_time),
            max_close_time=click.str_to_datetime(max_close_time),
    ):
        if vulnerability.location in host_ids_by_location:
            for host_id in host_ids_by_location[vulnerability.location]:
                host = hosts_by_id[host_id]
                if host.os_type:
                    tally[host.os_type] += 1

    click.echo(json.dumps(tally, indent=DEFAULT_INDENT, sort_keys=SORT_KEYS_BY_DEFAULT))


@vulnerabilities.command()
@click.option('--ids')
@click.option('--names')
@click.option('--cve-ids')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--locations')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--affects-pci-compliance/--does-not-affect-pci-compliance', default=None)
@click.option('--include-application-layer-vulnerabilities/--exclude-application-layer-vulnerabilities', default=True)
@click.option('--include-network-layer-vulnerabilities/--exclude-network-layer-vulnerabilities', default=True)
@click.option('--min-create-time')
@click.option('--max-create-time')
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--min-open-time')
@click.option('--max-open-time')
@click.option('--min-close-time')
@click.option('--max-close-time')
@click.pass_context
def count_vulnerabilities_by_os_version(
        ctx: click.Context,
        ids: Optional[str],
        names: Optional[str],
        cve_ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        locations: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        affects_pci_compliance: Optional[bool],
        include_application_layer_vulnerabilities: Optional[bool],
        include_network_layer_vulnerabilities: Optional[bool],
        min_create_time: Optional[str],
        max_create_time: Optional[str],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        min_open_time: Optional[str],
        max_open_time: Optional[str],
        min_close_time: Optional[str],
        max_close_time: Optional[str]):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])

    #: Lookup hosts.
    hosts = api.get_hosts(
        asset_ids=click.str_to_ints(asset_ids),
        asset_tags=click.str_to_strs(asset_tags),
        os_types=click.str_to_strs(os_types),
        os_versions=click.str_to_strs(os_versions),
        min_vulnerability_create_time=click.str_to_datetime(min_create_time),
        max_vulnerability_create_time=click.str_to_datetime(max_create_time),
        min_vulnerability_update_time=click.str_to_datetime(min_update_time),
        max_vulnerability_update_time=click.str_to_datetime(max_update_time),
        min_vulnerability_open_time=click.str_to_datetime(min_open_time),
        max_vulnerability_open_time=click.str_to_datetime(max_open_time),
        min_vulnerability_close_time=click.str_to_datetime(min_close_time),
        max_vulnerability_close_time=click.str_to_datetime(max_close_time),
    )
    hosts_by_id = dict((host.id, host) for host in hosts)
    host_ids_by_location = collections.defaultdict(set)
    for host in hosts:
        host_ids_by_location[host.location].add(host.id)

    #: Lookup vulnerabilities.
    tally = collections.defaultdict(int)
    for vulnerability in api.get_vulnerabilities(
            ids=click.str_to_ints(ids),
            names=click.str_to_strs(names),
            cve_ids=click.str_to_strs(cve_ids),
            asset_ids=click.str_to_ints(asset_ids),
            asset_tags=click.str_to_strs(asset_tags),
            locations=click.str_to_strs(locations),
            os_types=click.str_to_strs(os_types),
            os_versions=click.str_to_strs(os_versions),
            affects_pci_compliance=affects_pci_compliance,
            include_application_layer_vulnerabilities=include_application_layer_vulnerabilities,
            include_network_layer_vulnerabilities=include_network_layer_vulnerabilities,
            min_create_time=click.str_to_datetime(min_create_time),
            max_create_time=click.str_to_datetime(max_create_time),
            min_update_time=click.str_to_datetime(min_update_time),
            max_update_time=click.str_to_datetime(max_update_time),
            min_open_time=click.str_to_datetime(min_open_time),
            max_open_time=click.str_to_datetime(max_open_time),
            min_close_time=click.str_to_datetime(min_close_time),
            max_close_time=click.str_to_datetime(max_close_time),
    ):
        if vulnerability.location in host_ids_by_location:
            for host_id in host_ids_by_location[vulnerability.location]:
                host = hosts_by_id[host_id]
                if host.os_version:
                    tally[host.os_version] += 1

    click.echo(json.dumps(tally, indent=DEFAULT_INDENT, sort_keys=SORT_KEYS_BY_DEFAULT))


@vulnerabilities.command()
@click.option('--ids')
@click.option('--names')
@click.option('--cve-ids')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--locations')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--affects-pci-compliance/--does-not-affect-pci-compliance', default=None)
@click.option('--include-application-layer-vulnerabilities/--exclude-application-layer-vulnerabilities', default=True)
@click.option('--include-network-layer-vulnerabilities/--exclude-network-layer-vulnerabilities', default=True)
@click.option('--min-create-time')
@click.option('--max-create-time')
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--min-open-time')
@click.option('--max-open-time')
@click.option('--min-close-time')
@click.option('--max-close-time')
@click.option('--granularity', type=click.Choice(['hour', 'day', 'month']), default='day')
@click.pass_context
def count_vulnerabilities_by_open_time(
        ctx: click.Context,
        ids: Optional[str],
        names: Optional[str],
        cve_ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        locations: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        affects_pci_compliance: Optional[bool],
        include_application_layer_vulnerabilities: Optional[bool],
        include_network_layer_vulnerabilities: Optional[bool],
        min_create_time: Optional[str],
        max_create_time: Optional[str],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        min_open_time: Optional[str],
        max_open_time: Optional[str],
        min_close_time: Optional[str],
        max_close_time: Optional[str],
        granularity: str):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])

    tally = collections.defaultdict(int)
    for vulnerability in api.get_vulnerabilities(
            ids=click.str_to_ints(ids),
            names=click.str_to_strs(names),
            cve_ids=click.str_to_strs(cve_ids),
            asset_ids=click.str_to_ints(asset_ids),
            asset_tags=click.str_to_strs(asset_tags),
            locations=click.str_to_strs(locations),
            os_types=click.str_to_strs(os_types),
            os_versions=click.str_to_strs(os_versions),
            affects_pci_compliance=affects_pci_compliance,
            include_application_layer_vulnerabilities=include_application_layer_vulnerabilities,
            include_network_layer_vulnerabilities=include_network_layer_vulnerabilities,
            min_create_time=click.str_to_datetime(min_create_time),
            max_create_time=click.str_to_datetime(max_create_time),
            min_update_time=click.str_to_datetime(min_update_time),
            max_update_time=click.str_to_datetime(max_update_time),
            min_open_time=click.str_to_datetime(min_open_time),
            max_open_time=click.str_to_datetime(max_open_time),
            min_close_time=click.str_to_datetime(min_close_time),
            max_close_time=click.str_to_datetime(max_close_time),
    ):
        open_time = vulnerability.open_time
        if granularity in [HOUR, DAY, MONTH]:
            open_time = hodgepodge.time.round_datetime(open_time, granularity=granularity)
            if granularity == HOUR:
                open_time = open_time.strftime('%Y-%m-%dT%H:%M')
            else:
                open_time = open_time.date().isoformat()
        else:
            open_time = open_time.isoformat()
        tally[open_time] += 1

    click.echo(json.dumps(tally, indent=DEFAULT_INDENT, sort_keys=SORT_KEYS_BY_DEFAULT))


@vulnerabilities.command()
@click.option('--ids')
@click.option('--names')
@click.option('--cve-ids')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--locations')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--affects-pci-compliance/--does-not-affect-pci-compliance', default=None)
@click.option('--include-application-layer-vulnerabilities/--exclude-application-layer-vulnerabilities', default=True)
@click.option('--include-network-layer-vulnerabilities/--exclude-network-layer-vulnerabilities', default=True)
@click.option('--min-create-time')
@click.option('--max-create-time')
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--min-open-time')
@click.option('--max-open-time')
@click.option('--min-close-time')
@click.option('--max-close-time')
@click.option('--granularity', type=click.Choice(['hour', 'day', 'month']), default='day')
@click.pass_context
def count_vulnerabilities_by_close_time(
        ctx: click.Context,
        ids: Optional[str],
        names: Optional[str],
        cve_ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        locations: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        affects_pci_compliance: Optional[bool],
        include_application_layer_vulnerabilities: Optional[bool],
        include_network_layer_vulnerabilities: Optional[bool],
        min_create_time: Optional[str],
        max_create_time: Optional[str],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        min_open_time: Optional[str],
        max_open_time: Optional[str],
        min_close_time: Optional[str],
        max_close_time: Optional[str],
        granularity: str):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])

    tally = collections.defaultdict(int)
    for vulnerability in api.get_vulnerabilities(
            ids=click.str_to_ints(ids),
            names=click.str_to_strs(names),
            cve_ids=click.str_to_strs(cve_ids),
            asset_ids=click.str_to_ints(asset_ids),
            asset_tags=click.str_to_strs(asset_tags),
            locations=click.str_to_strs(locations),
            os_types=click.str_to_strs(os_types),
            os_versions=click.str_to_strs(os_versions),
            affects_pci_compliance=affects_pci_compliance,
            include_application_layer_vulnerabilities=include_application_layer_vulnerabilities,
            include_network_layer_vulnerabilities=include_network_layer_vulnerabilities,
            min_create_time=click.str_to_datetime(min_create_time),
            max_create_time=click.str_to_datetime(max_create_time),
            min_update_time=click.str_to_datetime(min_update_time),
            max_update_time=click.str_to_datetime(max_update_time),
            min_open_time=click.str_to_datetime(min_open_time),
            max_open_time=click.str_to_datetime(max_open_time),
            min_close_time=click.str_to_datetime(min_close_time),
            max_close_time=click.str_to_datetime(max_close_time),
    ):
        close_time = vulnerability.close_time
        if not close_time:
            continue

        if granularity in [HOUR, DAY, MONTH]:
            close_time = hodgepodge.time.round_datetime(close_time, granularity=granularity)
            if granularity == HOUR:
                close_time = close_time.strftime('%Y-%m-%dT%H:%M')
            else:
                close_time = close_time.date().isoformat()
        else:
            close_time = close_time.isoformat()
        tally[close_time] += 1

    click.echo(json.dumps(tally, indent=DEFAULT_INDENT, sort_keys=SORT_KEYS_BY_DEFAULT))
