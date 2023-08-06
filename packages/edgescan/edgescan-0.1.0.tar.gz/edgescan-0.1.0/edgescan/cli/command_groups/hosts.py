from typing import Optional
from edgescan.api.client import EdgeScan

import edgescan.cli.click as click


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
@click.option('--hostnames')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--ip-addresses')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--alive/--dead', default=None)
@click.option('--limit', type=int)
@click.pass_context
def get_hosts(
        ctx: click.Context,
        ids: str,
        hostnames: str,
        asset_ids: str,
        asset_tags: str,
        ip_addresses: str,
        os_types: str,
        os_versions: str,
        alive: Optional[bool],
        limit: int):

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
        limit=limit,
    ):
        click.echo(host.to_json())


@hosts.command()
@click.option('--ids')
@click.option('--hostnames')
@click.option('--asset-ids')
@click.option('--asset-tags')
@click.option('--ip-addresses')
@click.option('--os-types')
@click.option('--os-versions')
@click.option('--alive/--dead', default=None)
@click.pass_context
def count_hosts(
        ctx: click.Context,
        ids: str,
        hostnames: str,
        asset_ids: str,
        asset_tags: str,
        ip_addresses: str,
        os_types: str,
        os_versions: str,
        alive: Optional[bool]):

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
    )
    click.echo(total)
