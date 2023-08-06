from edgescan.api.client import EdgeScan

import edgescan.cli.click as click


@click.group()
@click.pass_context
def licenses(_):
    """
    Query or count licenses.
    """
    pass


@licenses.command()
@click.option('--id', 'license_id', type=int, required=True)
@click.pass_context
def get_license(ctx: click.Context, license_id: int):
    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    row = api.get_license(license_id)
    if row:
        click.echo(row.to_json())


@licenses.command()
@click.option('--ids')
@click.option('--names')
@click.option('--expired/--not-expired', default=None)
@click.option('--limit', type=int)
@click.pass_context
def get_licenses(ctx: click.Context, ids: str, names: str, expired: bool, limit: int):
    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    for row in api.iter_licenses(
        ids=click.str_to_ints(ids),
        names=click.str_to_strs(names),
        expired=expired,
        limit=limit,
    ):
        click.echo(row.to_json())


@licenses.command()
@click.option('--ids')
@click.option('--names')
@click.option('--expired/--not-expired', default=None)
@click.pass_context
def count_licenses(ctx: click.Context, ids: str, names: str, expired: bool):
    api = EdgeScan(**ctx.obj['config']['edgescan']['api'])
    total = api.count_licenses(
        ids=click.str_to_ints(ids),
        names=click.str_to_strs(names),
        expired=expired,
    )
    click.echo(total)
