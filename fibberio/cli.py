import os
import click
from .task import Task
from pathlib import Path


def normalize_path(p, create_dir=False) -> Path:
    path = Path(p)
    if not path.is_absolute():
        path = Path(os.getcwd()).joinpath(path).absolute().resolve()
    else:
        path = path.absolute().resolve()

    if create_dir and not path.parent.exists():
        os.makedirs(str(path.parent))

    return path


@click.command()
@click.option("--task", "-t", required=True)
@click.option("--count", "-c", required=True, type=int)
@click.option(
    "--type",
    "-y",
    "file_type",
    default="csv",
    type=click.Choice(["csv", "xls"], case_sensitive=False),
)
@click.option("--output", "-o", default=".")
@click.version_option()
def cli(task, count, file_type, output):
    desc = normalize_path(task)
    if not desc.exists():
        print(f'{str(desc)} does not exist')
        return

    task = Task(str(desc))
    itms = f'Generating {count} items using "{desc.name}"'
    print(f'\n{itms}\n{"-"*len(itms)}\n')

    try:
        df = task.generate(count)
        stats = df.describe(include='all')
        print(stats)

        out = normalize_path(output, create_dir=True)
        print(f'\nSaving {file_type} to {str(out)}')
        if file_type == 'csv':
            df.to_csv(str(out))

    except Exception as e:
        print(f'Looks like there was a problem:\n\n{e}\n')

    print('Task complete\n')
