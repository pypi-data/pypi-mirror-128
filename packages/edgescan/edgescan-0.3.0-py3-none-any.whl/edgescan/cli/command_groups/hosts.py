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
def hosts(_):
    """
    Query or count hosts.
    """
    pass


@hosts.command()
@click.option('--id', 'host_id', type=int, required=True)
@click.pass_context
def get_host(ctx: click.Context, host_id: int):
    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    host = api.get_host(host_id)
    if host:
        click.echo(host.to_json())


@hosts.command()
@click.option('--ids')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--ip-addresses')
@click.option('--hostnames')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--alive/--dead', default=None)
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--vulnerability-ids')
@click.option('--cve-ids')
@click.option('--min-vulnerability-create-time')
@click.option('--max-vulnerability-create-time')
@click.option('--min-vulnerability-update-time')
@click.option('--max-vulnerability-update-time')
@click.option('--min-vulnerability-open-time')
@click.option('--max-vulnerability-open-time')
@click.option('--min-vulnerability-close-time')
@click.option('--max-vulnerability-close-time')
@click.option('--limit', type=int)
@click.pass_context
def get_hosts(
        ctx: click.Context,
        ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        ip_addresses: Optional[str],
        hostnames: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        alive: Optional[bool],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        vulnerability_ids: Optional[str],
        cve_ids: Optional[str],
        min_vulnerability_create_time: Optional[str],
        max_vulnerability_create_time: Optional[str],
        min_vulnerability_update_time: Optional[str],
        max_vulnerability_update_time: Optional[str],
        min_vulnerability_open_time: Optional[str],
        max_vulnerability_open_time: Optional[str],
        min_vulnerability_close_time: Optional[str],
        max_vulnerability_close_time: Optional[str],
        limit: Optional[int]):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    for host in api.iter_hosts(
        ids=click.str_to_ints(ids),
        hostnames=click.str_to_strs(hostnames),
        asset_ids=click.str_to_ints(asset_ids),
        asset_tags=click.str_to_strs(asset_tags),
        ip_addresses=click.str_to_strs(ip_addresses),
        os_types=click.str_to_strs(os_types),
        os_versions=click.str_to_strs(os_versions),
        alive=alive,
        min_update_time=click.str_to_datetime(min_update_time),
        max_update_time=click.str_to_datetime(max_update_time),
        vulnerability_ids=click.str_to_ints(vulnerability_ids),
        cve_ids=click.str_to_strs(cve_ids),
        min_vulnerability_create_time=click.str_to_datetime(min_vulnerability_create_time),
        max_vulnerability_create_time=click.str_to_datetime(max_vulnerability_create_time),
        min_vulnerability_update_time=click.str_to_datetime(min_vulnerability_update_time),
        max_vulnerability_update_time=click.str_to_datetime(max_vulnerability_update_time),
        min_vulnerability_open_time=click.str_to_datetime(min_vulnerability_open_time),
        max_vulnerability_open_time=click.str_to_datetime(max_vulnerability_open_time),
        min_vulnerability_close_time=click.str_to_datetime(min_vulnerability_close_time),
        max_vulnerability_close_time=click.str_to_datetime(max_vulnerability_close_time),
        limit=limit,
    ):
        click.echo(host.to_json())


@hosts.command()
@click.option('--ids')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--ip-addresses')
@click.option('--hostnames')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--alive/--dead', default=None)
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--vulnerability-ids')
@click.option('--cve-ids')
@click.option('--min-vulnerability-create-time')
@click.option('--max-vulnerability-create-time')
@click.option('--min-vulnerability-update-time')
@click.option('--max-vulnerability-update-time')
@click.option('--min-vulnerability-open-time')
@click.option('--max-vulnerability-open-time')
@click.option('--min-vulnerability-close-time')
@click.option('--max-vulnerability-close-time')
@click.pass_context
def count_hosts(
        ctx: click.Context,
        ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        ip_addresses: Optional[str],
        hostnames: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        alive: Optional[bool],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        vulnerability_ids: Optional[str],
        cve_ids: Optional[str],
        min_vulnerability_create_time: Optional[str],
        max_vulnerability_create_time: Optional[str],
        min_vulnerability_update_time: Optional[str],
        max_vulnerability_update_time: Optional[str],
        min_vulnerability_open_time: Optional[str],
        max_vulnerability_open_time: Optional[str],
        min_vulnerability_close_time: Optional[str],
        max_vulnerability_close_time: Optional[str]):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    total = api.count_hosts(
        ids=click.str_to_ints(ids),
        hostnames=click.str_to_strs(hostnames),
        asset_ids=click.str_to_ints(asset_ids),
        asset_tags=click.str_to_strs(asset_tags),
        ip_addresses=click.str_to_strs(ip_addresses),
        os_types=click.str_to_strs(os_types),
        os_versions=click.str_to_strs(os_versions),
        alive=alive,
        min_update_time=click.str_to_datetime(min_update_time),
        max_update_time=click.str_to_datetime(max_update_time),
        vulnerability_ids=click.str_to_ints(vulnerability_ids),
        cve_ids=click.str_to_strs(cve_ids),
        min_vulnerability_create_time=click.str_to_datetime(min_vulnerability_create_time),
        max_vulnerability_create_time=click.str_to_datetime(max_vulnerability_create_time),
        min_vulnerability_update_time=click.str_to_datetime(min_vulnerability_update_time),
        max_vulnerability_update_time=click.str_to_datetime(max_vulnerability_update_time),
        min_vulnerability_open_time=click.str_to_datetime(min_vulnerability_open_time),
        max_vulnerability_open_time=click.str_to_datetime(max_vulnerability_open_time),
        min_vulnerability_close_time=click.str_to_datetime(min_vulnerability_close_time),
        max_vulnerability_close_time=click.str_to_datetime(max_vulnerability_close_time),
    )
    click.echo(total)


@hosts.command()
@click.option('--ids')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--ip-addresses')
@click.option('--hostnames')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--alive/--dead', default=None)
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--vulnerability-ids')
@click.option('--cve-ids')
@click.option('--min-vulnerability-create-time')
@click.option('--max-vulnerability-create-time')
@click.option('--min-vulnerability-update-time')
@click.option('--max-vulnerability-update-time')
@click.option('--min-vulnerability-open-time')
@click.option('--max-vulnerability-open-time')
@click.option('--min-vulnerability-close-time')
@click.option('--max-vulnerability-close-time')
@click.option('--granularity', type=click.Choice(['hour', 'day', 'month']), default='day')
@click.pass_context
def count_hosts_by_last_seen_time(
        ctx: click.Context,
        ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        ip_addresses: Optional[str],
        hostnames: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        alive: Optional[bool],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        vulnerability_ids: Optional[str],
        cve_ids: Optional[str],
        min_vulnerability_create_time: Optional[str],
        max_vulnerability_create_time: Optional[str],
        min_vulnerability_update_time: Optional[str],
        max_vulnerability_update_time: Optional[str],
        min_vulnerability_open_time: Optional[str],
        max_vulnerability_open_time: Optional[str],
        min_vulnerability_close_time: Optional[str],
        max_vulnerability_close_time: Optional[str],
        granularity: str):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    tally = collections.defaultdict(int)
    for host in api.get_hosts(
        ids=click.str_to_ints(ids),
        hostnames=click.str_to_strs(hostnames),
        asset_ids=click.str_to_ints(asset_ids),
        asset_tags=click.str_to_strs(asset_tags),
        ip_addresses=click.str_to_strs(ip_addresses),
        os_types=click.str_to_strs(os_types),
        os_versions=click.str_to_strs(os_versions),
        alive=alive,
        min_update_time=click.str_to_datetime(min_update_time),
        max_update_time=click.str_to_datetime(max_update_time),
        vulnerability_ids=click.str_to_ints(vulnerability_ids),
        cve_ids=click.str_to_strs(cve_ids),
        min_vulnerability_create_time=click.str_to_datetime(min_vulnerability_create_time),
        max_vulnerability_create_time=click.str_to_datetime(max_vulnerability_create_time),
        min_vulnerability_update_time=click.str_to_datetime(min_vulnerability_update_time),
        max_vulnerability_update_time=click.str_to_datetime(max_vulnerability_update_time),
        min_vulnerability_open_time=click.str_to_datetime(min_vulnerability_open_time),
        max_vulnerability_open_time=click.str_to_datetime(max_vulnerability_open_time),
        min_vulnerability_close_time=click.str_to_datetime(min_vulnerability_close_time),
        max_vulnerability_close_time=click.str_to_datetime(max_vulnerability_close_time),
    ):
        update_time = host.update_time
        if granularity in [HOUR, DAY, MONTH]:
            update_time = hodgepodge.time.round_datetime(update_time, granularity=granularity)
            if granularity == HOUR:
                update_time = update_time.strftime('%Y-%m-%dT%H:%M')
            else:
                update_time = update_time.date().isoformat()
        else:
            update_time = update_time.isoformat()
        tally[update_time] += 1

    click.echo(json.dumps(tally, indent=DEFAULT_INDENT, sort_keys=SORT_KEYS_BY_DEFAULT))


@hosts.command()
@click.option('--ids')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--ip-addresses')
@click.option('--hostnames')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--alive/--dead', default=None)
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--vulnerability-ids')
@click.option('--cve-ids')
@click.option('--min-vulnerability-create-time')
@click.option('--max-vulnerability-create-time')
@click.option('--min-vulnerability-update-time')
@click.option('--max-vulnerability-update-time')
@click.option('--min-vulnerability-open-time')
@click.option('--max-vulnerability-open-time')
@click.option('--min-vulnerability-close-time')
@click.option('--max-vulnerability-close-time')
@click.pass_context
def count_hosts_by_status(
        ctx: click.Context,
        ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        ip_addresses: Optional[str],
        hostnames: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        alive: Optional[bool],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        vulnerability_ids: Optional[str],
        cve_ids: Optional[str],
        min_vulnerability_create_time: Optional[str],
        max_vulnerability_create_time: Optional[str],
        min_vulnerability_update_time: Optional[str],
        max_vulnerability_update_time: Optional[str],
        min_vulnerability_open_time: Optional[str],
        max_vulnerability_open_time: Optional[str],
        min_vulnerability_close_time: Optional[str],
        max_vulnerability_close_time: Optional[str]):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    tally = collections.defaultdict(int)
    for host in api.get_hosts(
        ids=click.str_to_ints(ids),
        hostnames=click.str_to_strs(hostnames),
        asset_ids=click.str_to_ints(asset_ids),
        asset_tags=click.str_to_strs(asset_tags),
        ip_addresses=click.str_to_strs(ip_addresses),
        os_types=click.str_to_strs(os_types),
        os_versions=click.str_to_strs(os_versions),
        alive=alive,
        min_update_time=click.str_to_datetime(min_update_time),
        max_update_time=click.str_to_datetime(max_update_time),
        vulnerability_ids=click.str_to_ints(vulnerability_ids),
        cve_ids=click.str_to_strs(cve_ids),
        min_vulnerability_create_time=click.str_to_datetime(min_vulnerability_create_time),
        max_vulnerability_create_time=click.str_to_datetime(max_vulnerability_create_time),
        min_vulnerability_update_time=click.str_to_datetime(min_vulnerability_update_time),
        max_vulnerability_update_time=click.str_to_datetime(max_vulnerability_update_time),
        min_vulnerability_open_time=click.str_to_datetime(min_vulnerability_open_time),
        max_vulnerability_open_time=click.str_to_datetime(max_vulnerability_open_time),
        min_vulnerability_close_time=click.str_to_datetime(min_vulnerability_close_time),
        max_vulnerability_close_time=click.str_to_datetime(max_vulnerability_close_time),
    ):
        tally[host.status] += 1

    click.echo(json.dumps(tally, indent=DEFAULT_INDENT, sort_keys=SORT_KEYS_BY_DEFAULT))


@hosts.command()
@click.option('--ids')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--ip-addresses')
@click.option('--hostnames')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--alive/--dead', default=None)
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--vulnerability-ids')
@click.option('--cve-ids')
@click.option('--min-vulnerability-create-time')
@click.option('--max-vulnerability-create-time')
@click.option('--min-vulnerability-update-time')
@click.option('--max-vulnerability-update-time')
@click.option('--min-vulnerability-open-time')
@click.option('--max-vulnerability-open-time')
@click.option('--min-vulnerability-close-time')
@click.option('--max-vulnerability-close-time')
@click.pass_context
def count_hosts_by_os_type(
        ctx: click.Context,
        ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        ip_addresses: Optional[str],
        hostnames: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        alive: Optional[bool],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        vulnerability_ids: Optional[str],
        cve_ids: Optional[str],
        min_vulnerability_create_time: Optional[str],
        max_vulnerability_create_time: Optional[str],
        min_vulnerability_update_time: Optional[str],
        max_vulnerability_update_time: Optional[str],
        min_vulnerability_open_time: Optional[str],
        max_vulnerability_open_time: Optional[str],
        min_vulnerability_close_time: Optional[str],
        max_vulnerability_close_time: Optional[str]):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])

    tally = collections.defaultdict(int)
    for host in api.get_hosts(
        ids=click.str_to_ints(ids),
        hostnames=click.str_to_strs(hostnames),
        asset_ids=click.str_to_ints(asset_ids),
        asset_tags=click.str_to_strs(asset_tags),
        ip_addresses=click.str_to_strs(ip_addresses),
        os_types=click.str_to_strs(os_types),
        os_versions=click.str_to_strs(os_versions),
        alive=alive,
        min_update_time=click.str_to_datetime(min_update_time),
        max_update_time=click.str_to_datetime(max_update_time),
        vulnerability_ids=click.str_to_ints(vulnerability_ids),
        cve_ids=click.str_to_strs(cve_ids),
        min_vulnerability_create_time=click.str_to_datetime(min_vulnerability_create_time),
        max_vulnerability_create_time=click.str_to_datetime(max_vulnerability_create_time),
        min_vulnerability_update_time=click.str_to_datetime(min_vulnerability_update_time),
        max_vulnerability_update_time=click.str_to_datetime(max_vulnerability_update_time),
        min_vulnerability_open_time=click.str_to_datetime(min_vulnerability_open_time),
        max_vulnerability_open_time=click.str_to_datetime(max_vulnerability_open_time),
        min_vulnerability_close_time=click.str_to_datetime(min_vulnerability_close_time),
        max_vulnerability_close_time=click.str_to_datetime(max_vulnerability_close_time),
    ):
        if host.os_type:
            tally[host.os_type] += 1

    click.echo(json.dumps(tally, indent=DEFAULT_INDENT, sort_keys=SORT_KEYS_BY_DEFAULT))


@hosts.command()
@click.option('--ids')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--ip-addresses')
@click.option('--hostnames')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--alive/--dead', default=None)
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--vulnerability-ids')
@click.option('--cve-ids')
@click.option('--min-vulnerability-create-time')
@click.option('--max-vulnerability-create-time')
@click.option('--min-vulnerability-update-time')
@click.option('--max-vulnerability-update-time')
@click.option('--min-vulnerability-open-time')
@click.option('--max-vulnerability-open-time')
@click.option('--min-vulnerability-close-time')
@click.option('--max-vulnerability-close-time')
@click.pass_context
def count_hosts_by_os_version(
        ctx: click.Context,
        ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        ip_addresses: Optional[str],
        hostnames: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        alive: Optional[bool],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        vulnerability_ids: Optional[str],
        cve_ids: Optional[str],
        min_vulnerability_create_time: Optional[str],
        max_vulnerability_create_time: Optional[str],
        min_vulnerability_update_time: Optional[str],
        max_vulnerability_update_time: Optional[str],
        min_vulnerability_open_time: Optional[str],
        max_vulnerability_open_time: Optional[str],
        min_vulnerability_close_time: Optional[str],
        max_vulnerability_close_time: Optional[str]):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])

    tally = collections.defaultdict(int)
    for host in api.get_hosts(
        ids=click.str_to_ints(ids),
        hostnames=click.str_to_strs(hostnames),
        asset_ids=click.str_to_ints(asset_ids),
        asset_tags=click.str_to_strs(asset_tags),
        ip_addresses=click.str_to_strs(ip_addresses),
        os_types=click.str_to_strs(os_types),
        os_versions=click.str_to_strs(os_versions),
        alive=alive,
        min_update_time=click.str_to_datetime(min_update_time),
        max_update_time=click.str_to_datetime(max_update_time),
        vulnerability_ids=click.str_to_ints(vulnerability_ids),
        cve_ids=click.str_to_strs(cve_ids),
        min_vulnerability_create_time=click.str_to_datetime(min_vulnerability_create_time),
        max_vulnerability_create_time=click.str_to_datetime(max_vulnerability_create_time),
        min_vulnerability_update_time=click.str_to_datetime(min_vulnerability_update_time),
        max_vulnerability_update_time=click.str_to_datetime(max_vulnerability_update_time),
        min_vulnerability_open_time=click.str_to_datetime(min_vulnerability_open_time),
        max_vulnerability_open_time=click.str_to_datetime(max_vulnerability_open_time),
        min_vulnerability_close_time=click.str_to_datetime(min_vulnerability_close_time),
        max_vulnerability_close_time=click.str_to_datetime(max_vulnerability_close_time),
    ):
        if host.os_version:
            tally[host.os_version] += 1

    click.echo(json.dumps(tally, indent=DEFAULT_INDENT, sort_keys=SORT_KEYS_BY_DEFAULT))


@hosts.command()
@click.option('--ids')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--ip-addresses')
@click.option('--hostnames')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--alive/--dead', default=None)
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--vulnerability-ids')
@click.option('--cve-ids')
@click.option('--min-vulnerability-create-time')
@click.option('--max-vulnerability-create-time')
@click.option('--min-vulnerability-update-time')
@click.option('--max-vulnerability-update-time')
@click.option('--min-vulnerability-open-time')
@click.option('--max-vulnerability-open-time')
@click.option('--min-vulnerability-close-time')
@click.option('--max-vulnerability-close-time')
@click.pass_context
def count_hosts_by_asset_group_name(
        ctx: click.Context,
        ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        ip_addresses: Optional[str],
        hostnames: Optional[str],
        os_types: Optional[str],
        os_versions: Optional[str],
        alive: Optional[bool],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        vulnerability_ids: Optional[str],
        cve_ids: Optional[str],
        min_vulnerability_create_time: Optional[str],
        max_vulnerability_create_time: Optional[str],
        min_vulnerability_update_time: Optional[str],
        max_vulnerability_update_time: Optional[str],
        min_vulnerability_open_time: Optional[str],
        max_vulnerability_open_time: Optional[str],
        min_vulnerability_close_time: Optional[str],
        max_vulnerability_close_time: Optional[str]):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])

    #: Lookup assets.
    assets = api.get_assets(
        ids=click.str_to_ints(asset_ids),
        tags=click.str_to_strs(asset_tags),
    )
    assets_by_id = dict((asset.id, asset) for asset in assets)
    asset_ids = list(assets_by_id.keys())

    #: Lookup and count hosts.
    hosts_by_asset_id = collections.defaultdict(int)
    for host in api.get_hosts(
        ids=click.str_to_ints(ids),
        hostnames=click.str_to_strs(hostnames),
        asset_ids=asset_ids,
        ip_addresses=click.str_to_strs(ip_addresses),
        os_types=click.str_to_strs(os_types),
        os_versions=click.str_to_strs(os_versions),
        alive=alive,
        min_update_time=click.str_to_datetime(min_update_time),
        max_update_time=click.str_to_datetime(max_update_time),
        vulnerability_ids=click.str_to_ints(vulnerability_ids),
        cve_ids=click.str_to_strs(cve_ids),
        min_vulnerability_create_time=click.str_to_datetime(min_vulnerability_create_time),
        max_vulnerability_create_time=click.str_to_datetime(max_vulnerability_create_time),
        min_vulnerability_update_time=click.str_to_datetime(min_vulnerability_update_time),
        max_vulnerability_update_time=click.str_to_datetime(max_vulnerability_update_time),
        min_vulnerability_open_time=click.str_to_datetime(min_vulnerability_open_time),
        max_vulnerability_open_time=click.str_to_datetime(max_vulnerability_open_time),
        min_vulnerability_close_time=click.str_to_datetime(min_vulnerability_close_time),
        max_vulnerability_close_time=click.str_to_datetime(max_vulnerability_close_time),
    ):
        hosts_by_asset_id[host.asset_id] += 1

    tally = {}
    for asset_id, count in hosts_by_asset_id.items():
        asset_name = assets_by_id[asset_id].name
        tally[asset_name] = count

    click.echo(json.dumps(tally, indent=DEFAULT_INDENT, sort_keys=SORT_KEYS_BY_DEFAULT))
