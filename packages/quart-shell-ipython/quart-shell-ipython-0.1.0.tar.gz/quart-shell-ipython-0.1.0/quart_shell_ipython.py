import sys
import asyncio

import IPython
import click
from quart import current_app
from quart.cli import with_appcontext
from IPython.terminal.ipapp import load_default_config


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('ipython_args', nargs=-1, type=click.UNPROCESSED)
@with_appcontext
def shell(ipython_args):
    config = load_default_config()

    asyncio.run(current_app.startup())

    context = current_app.make_shell_context()

    config.TerminalInteractiveShell.banner1 = """Python %s on %s
IPython: %s
App: %s [%s]
""" % (
        sys.version,
        sys.platform,
        IPython.__version__,
        current_app.import_name,
        current_app.env,
    )

    IPython.start_ipython(
        argv=ipython_args,
        user_ns=context,
        config=config,
    )
