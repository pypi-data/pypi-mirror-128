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
@click.option('--limit', type=int)
@click.pass_context
def get_assets(ctx: click.Context, ids: str, names: str, tags: str, limit: int):
    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    for asset in api.iter_assets(
        ids=click.str_to_ints(ids),
        names=click.str_to_strs(names),
        tags=click.str_to_strs(tags),
        limit=limit,
    ):
        click.echo(asset.to_json())


@assets.command()
@click.option('--ids')
@click.option('--names')
@click.option('--tags')
@click.pass_context
def get_asset_tags(ctx: click.Context, ids: str, names: str, tags: str):
    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    rows = api.iter_assets(
        ids=click.str_to_ints(ids),
        names=click.str_to_strs(names),
        tags=click.str_to_strs(tags),
    )
    tags = sorted(set(itertools.chain.from_iterable(row.tags for row in rows)))
    click.echo(json.dumps(tags))


@assets.command()
@click.option('--ids')
@click.option('--names')
@click.option('--tags')
@click.pass_context
def count_assets(ctx: click.Context, ids: str, names: str, tags: str):
    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    total = api.count_assets(
        ids=click.str_to_ints(ids),
        names=click.str_to_strs(names),
        tags=click.str_to_strs(tags),
    )
    click.echo(total)
