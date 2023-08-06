from typing import Optional

from edgescan.api.client import EdgeScan

import itertools
import json
import edgescan.cli.click as click


@click.group()
@click.pass_context
def assets(_):
    """
    Query or count assets.
    """
    pass


@assets.command()
@click.option('--id', 'asset_id', type=int, required=True)
@click.pass_context
def get_asset(ctx: click.Context, asset_id: int):
    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    asset = api.get_asset(asset_id)
    if asset:
        click.echo(asset.to_json())


@assets.command()
@click.option('--ids')
@click.option('--names')
@click.option('--tags')
@click.option('--min-create-time')
@click.option('--max-create-time')
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--min-next-assessment-time')
@click.option('--max-next-assessment-time')
@click.option('--min-last-assessment-time')
@click.option('--max-last-assessment-time')
@click.option('--min-last-host-scan-time')
@click.option('--max-last-host-scan-time')
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
def get_assets(
        ctx: click.Context,
        ids: Optional[str],
        names: Optional[str],
        tags: Optional[str],
        min_create_time: Optional[str],
        max_create_time: Optional[str],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        min_next_assessment_time: Optional[str],
        max_next_assessment_time: Optional[str],
        min_last_assessment_time: Optional[str],
        max_last_assessment_time: Optional[str],
        min_last_host_scan_time: Optional[str],
        max_last_host_scan_time: Optional[str],
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
        limit: int):

    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    for asset in api.iter_assets(
        ids=click.str_to_ints(ids),
        names=click.str_to_strs(names),
        tags=click.str_to_strs(tags),
        min_create_time=click.str_to_datetime(min_create_time),
        max_create_time=click.str_to_datetime(max_create_time),
        min_update_time=click.str_to_datetime(min_update_time),
        max_update_time=click.str_to_datetime(max_update_time),
        min_next_assessment_time=click.str_to_datetime(min_next_assessment_time),
        max_next_assessment_time=click.str_to_datetime(max_next_assessment_time),
        min_last_assessment_time=click.str_to_datetime(min_last_assessment_time),
        max_last_assessment_time=click.str_to_datetime(max_last_assessment_time),
        min_last_host_scan_time=click.str_to_datetime(min_last_host_scan_time),
        max_last_host_scan_time=click.str_to_datetime(max_last_host_scan_time),
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
        click.echo(asset.to_json())


@assets.command()
@click.option('--ids')
@click.option('--names')
@click.option('--tags')
@click.option('--min-create-time')
@click.option('--max-create-time')
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--min-next-assessment-time')
@click.option('--max-next-assessment-time')
@click.option('--min-last-assessment-time')
@click.option('--max-last-assessment-time')
@click.option('--min-last-host-scan-time')
@click.option('--max-last-host-scan-time')
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
def get_asset_tags(
        ctx: click.Context,
        ids: Optional[str],
        names: Optional[str],
        tags: Optional[str],
        min_create_time: Optional[str],
        max_create_time: Optional[str],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        min_next_assessment_time: Optional[str],
        max_next_assessment_time: Optional[str],
        min_last_assessment_time: Optional[str],
        max_last_assessment_time: Optional[str],
        min_last_host_scan_time: Optional[str],
        max_last_host_scan_time: Optional[str],
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
    rows = api.iter_assets(
        ids=click.str_to_ints(ids),
        names=click.str_to_strs(names),
        tags=click.str_to_strs(tags),
        min_create_time=click.str_to_datetime(min_create_time),
        max_create_time=click.str_to_datetime(max_create_time),
        min_update_time=click.str_to_datetime(min_update_time),
        max_update_time=click.str_to_datetime(max_update_time),
        min_next_assessment_time=click.str_to_datetime(min_next_assessment_time),
        max_next_assessment_time=click.str_to_datetime(max_next_assessment_time),
        min_last_assessment_time=click.str_to_datetime(min_last_assessment_time),
        max_last_assessment_time=click.str_to_datetime(max_last_assessment_time),
        min_last_host_scan_time=click.str_to_datetime(min_last_host_scan_time),
        max_last_host_scan_time=click.str_to_datetime(max_last_host_scan_time),
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
    tags = sorted(set(itertools.chain.from_iterable(row.tags for row in rows)))
    click.echo(json.dumps(tags))


@assets.command()
@click.option('--ids')
@click.option('--names')
@click.option('--tags')
@click.option('--min-create-time')
@click.option('--max-create-time')
@click.option('--min-update-time')
@click.option('--max-update-time')
@click.option('--min-next-assessment-time')
@click.option('--max-next-assessment-time')
@click.option('--min-last-assessment-time')
@click.option('--max-last-assessment-time')
@click.option('--min-last-host-scan-time')
@click.option('--max-last-host-scan-time')
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
def count_assets(
        ctx: click.Context,
        ids: Optional[str],
        names: Optional[str],
        tags: Optional[str],
        min_create_time: Optional[str],
        max_create_time: Optional[str],
        min_update_time: Optional[str],
        max_update_time: Optional[str],
        min_next_assessment_time: Optional[str],
        max_next_assessment_time: Optional[str],
        min_last_assessment_time: Optional[str],
        max_last_assessment_time: Optional[str],
        min_last_host_scan_time: Optional[str],
        max_last_host_scan_time: Optional[str],
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
    total = api.count_assets(
        ids=click.str_to_ints(ids),
        names=click.str_to_strs(names),
        tags=click.str_to_strs(tags),
        min_create_time=click.str_to_datetime(min_create_time),
        max_create_time=click.str_to_datetime(max_create_time),
        min_update_time=click.str_to_datetime(min_update_time),
        max_update_time=click.str_to_datetime(max_update_time),
        min_next_assessment_time=click.str_to_datetime(min_next_assessment_time),
        max_next_assessment_time=click.str_to_datetime(max_next_assessment_time),
        min_last_assessment_time=click.str_to_datetime(min_last_assessment_time),
        max_last_assessment_time=click.str_to_datetime(max_last_assessment_time),
        min_last_host_scan_time=click.str_to_datetime(min_last_host_scan_time),
        max_last_host_scan_time=click.str_to_datetime(max_last_host_scan_time),
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
