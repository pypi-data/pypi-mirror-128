from typing import Optional

from typer import Argument
from typer import Context as TyperContext
from typer import echo

from spinta.cli.helpers.store import prepare_manifest
from spinta.components import Context
from spinta.core.config import RawConfig
from spinta.manifests.tabular.helpers import render_tabular_manifest


def show(
    ctx: TyperContext,
    manifest: Optional[str] = Argument(None),
):
    """Show manifest as ascii table"""

    context: Context = ctx.obj
    context = context.fork('show')

    if manifest is not None:
        config = {
            'keymaps.show': {
                'type': 'sqlalchemy',
                'dsn': 'sqlite://',
            },
            'backends.null': {
                'type': 'memory',
            },
            'manifests.show': {
                'type': 'tabular',
                'backend': 'null',
                'keymap': 'show',
                'mode': 'internal',
                'path': manifest,
            },
            'manifest': 'show',
        }

        # Add given manifest file to configuration
        rc: RawConfig = context.get('rc')
        context.set('rc', rc.fork(config))

    store = prepare_manifest(context, verbose=False)
    manifest = store.manifest
    echo(render_tabular_manifest(manifest))

