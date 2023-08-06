import os
import pathlib
import json
from datetime import datetime
from shutil import copyfile
import click

from .globaldeps import GlobalDeps
from .pages import Pages
from .snippets import Snippets

from elementalcms import ElementalContext
from elementalcms.persistence import MongoDbConnectionManager
from elementalcms.services.sessions import CreateExpirationIndex


@click.command('init')
@click.pass_context
def init(ctx):

    if os.path.exists('.elemental'):
        click.echo('Elemental CMS has been already initialized.')
        return

    context: ElementalContext = ctx.obj['elemental_context']
    db_name = MongoDbConnectionManager.get_db_name(context.cms_db_context)
    if db_name is None:
        click.echo('The database context has something wrong.')
        return

    click.echo(f'Initializing elemental CMS for db {db_name}...')

    CreateExpirationIndex(context.cms_db_context).execute()

    for path in ['media',
                 'static',
                 f'static/{context.cms_core_context.APP_NAME}',
                 'templates',
                 'translations',
                 'workspace',
                 'workspace/global_deps',
                 'workspace/snippets',
                 'workspace/pages']:
        create_folder(path)

    lib_root_path = pathlib.Path(__file__).resolve().parent
    path_parts = str(lib_root_path).split(os.sep)
    lib_path = os.sep.join(path_parts[1:-1])
    if not os.path.exists('templates/base.html'):
        copyfile(f'/{lib_path}/templates/base.html', 'templates/base.html')
    init_file = open('.elemental', mode="w", encoding="utf-8")
    init_file.write(json.dumps({
        'time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }, indent=4))
    init_file.close()
    click.echo('Initializing completed...')


def create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)
