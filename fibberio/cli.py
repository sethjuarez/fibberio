import click


@click.group()
@click.version_option()
def cli():
    pass


@cli.command()
@click.option("--config")
def run(config):
    print(f"made it! {config}")
