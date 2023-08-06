"""A minimal command line wrapper to make ufmt compatible with VSCode's
   calling convention for standalone black.
"""

from pathlib import Path

import click
import ufmt


@click.command()
@click.option('--diff/--no-diff', default=False)
@click.option('--quiet/--no-quiet', default=False)
@click.option('--dry-run/--no-dry-run', default=False)
@click.argument('file_path_str')
def ufmt_wrapper(diff: bool, quiet: bool, dry_run: bool, file_path_str: str):
    """See module docstring
    """
    file_path = Path(file_path_str)
    result = ufmt.ufmt_file(path=file_path, dry_run=dry_run, diff=diff)

    if not quiet:
        click.echo(result)

if __name__ == '__main__':
    ufmt_wrapper() # pylint: disable=no-value-for-parameter
