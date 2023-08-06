from typing import Optional
from edgescan.api.client import EdgeScan

import edgescan.cli.click as click


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
@click.option('--affects-pci-compliance/--does-not-affect-pci-compliance', default=None)
@click.option('--include-application-layer-vulnerabilities/--exclude-application-layer-vulnerabilities', default=True)
@click.option('--include-network-layer-vulnerabilities/--exclude-network-layer-vulnerabilities', default=True)
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
        affects_pci_compliance: Optional[bool],
        include_application_layer_vulnerabilities: Optional[bool],
        include_network_layer_vulnerabilities: Optional[bool],
        limit: int):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    for vulnerability in api.iter_vulnerabilities(
        ids=click.str_to_ints(ids),
        names=click.str_to_strs(names),
        cve_ids=click.str_to_strs(cve_ids),
        asset_ids=click.str_to_ints(asset_ids),
        asset_tags=click.str_to_strs(asset_tags),
        locations=click.str_to_strs(locations),
        affects_pci_compliance=affects_pci_compliance,
        include_application_layer_vulnerabilities=include_application_layer_vulnerabilities,
        include_network_layer_vulnerabilities=include_network_layer_vulnerabilities,
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
@click.option('--affects-pci-compliance/--does-not-affect-pci-compliance', default=None)
@click.option('--include-application-layer-vulnerabilities/--exclude-application-layer-vulnerabilities', default=True)
@click.option('--include-network-layer-vulnerabilities/--exclude-network-layer-vulnerabilities', default=True)
@click.pass_context
def count_vulnerabilities(
        ctx: click.Context,
        ids: Optional[str],
        names: Optional[str],
        cve_ids: Optional[str],
        asset_ids: Optional[str],
        asset_tags: Optional[str],
        locations: Optional[str],
        affects_pci_compliance: Optional[bool],
        include_application_layer_vulnerabilities: Optional[bool],
        include_network_layer_vulnerabilities: Optional[bool]):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    total = api.count_vulnerabilities(
        ids=click.str_to_ints(ids),
        names=click.str_to_strs(names),
        cve_ids=click.str_to_strs(cve_ids),
        asset_ids=click.str_to_ints(asset_ids),
        asset_tags=click.str_to_strs(asset_tags),
        locations=click.str_to_strs(locations),
        affects_pci_compliance=affects_pci_compliance,
        include_application_layer_vulnerabilities=include_application_layer_vulnerabilities,
        include_network_layer_vulnerabilities=include_network_layer_vulnerabilities,
    )
    click.echo(total)
