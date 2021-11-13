# -*- encoding: utf-8 -*-

import click
import os
"""git quick tools"""

_help = """
    GIT command quick tools: 

    push: Only commit changes to remote branches
    
        git commit -a -m [msg]
        git push

    push: Add * and commit changes to remote branches
    
        git add *
        git commit -a -m [msg]
        git push
"""


@click.option('--repo',
              '-r',
              default="origin",
              help='repository, default is origin')
@click.option('--branch',
              '-b',
              default="master",
              help='branch, default is master')
@click.option('--msg', '-m', default=":heart:update", help='commit message')
@click.command(context_settings=dict(
    allow_extra_args=True,
    ignore_unknown_options=True,
),
               help=_help)
@click.argument('command', required=False)
def git(command, repo, branch, msg):
    click.secho("Pull from git repository, default is origin master",
                fg='green')
    os.system("git pull {} {}".format(repo, branch))
    if 'push' in command:
        click.secho("Commit with message: {}".format(msg), fg='green')
        os.system("git commit -a -m \"{}\"".format(msg))
        os.system("git push")
    if 'pushall' in command:
        click.secho("Add * and commit with message: {}".format(msg), fg='green')
        os.system("git add *")
        os.system("git commit -a -m \"{}\"".format(msg))
        os.system("git push")
