import click
from bin.ai_init import ai_init1
from bin.ai_check import ai_check1
from bin.ai_env import ai_env1
from bin.ai_pkg import ai_pkg1
from bin.be_init import be_init1
from bin.be_pkg import be_pkg1
from bin.generate_activate_code import generate_code1


@click.version_option(version='0.1.0')
@click.group()
def cli():
    '''This is an automated Scaffolding, see the following for specific usage'''
    pass


@cli.command(help='init an ai project')
@click.option('--n', prompt='project name', help='define project name')
def ai_init(n):
    ai_init1(n)


@cli.command(help='check ai_env info')
def ai_check():
    ai_check1()


@cli.command(help='install ai_env')
def ai_env():
    ai_env1()


@cli.command(help='install ai_packages')
def ai_pkg():
    ai_pkg1()


@cli.command(help='init a drf project')
@click.option('--n', prompt='project name', help='define project name')
@click.option('--e', default='dev',
              help='define project env,default:dev,you can choose from the following options:local,dev,production')
def be_init(n, e):
    be_init1(n, e)


@cli.command(help='download drf sitepackages')
def be_pkg():
    be_pkg1()


@cli.command(help='generate pycharm activate code')
def generate_code():
    generate_code1()


if __name__ == '__main__':
    cli()
