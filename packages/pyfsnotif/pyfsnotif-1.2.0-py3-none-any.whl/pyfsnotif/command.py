from os.path import exists
from string import Template
from subprocess import run
from sys import argv

from pyfsnotif import Watcher, MODIFY


def _on_change_run(path, cmd):

    command = Template(cmd.replace('%','$path')).substitute(path=path).split(' ')

    def do_cmd(_evt):
        try:
            run(command)
        except Exception as x:
            print(f' ! {" ".join(command)} ! {x}')

    do_cmd(None)

    with Watcher() as w:
        w.add(path, MODIFY, do_cmd)

def on_change():
    usage = f'''Usage:
        on_change {{path}} {{cmd}}

        Use % in {{cmd}} as a placeholder for {{path}}.

        ex : on_change readme.txt cat %

        Use ^C to stop.
    '''
    path, *cmd = argv[1:]
    cmd = ' '.join(cmd)
    if exists(path):
        _on_change_run(path, cmd)
    else:
        print(usage)


def _on_changes_run(paths, cmd):
    def do_cmd(evt):
        command = Template(cmd.replace('%','$path')).substitute(path=evt.path).split(' ')
        try:
            run(command)
        except Exception as x:
            print(f' ! {" ".join(command)} ! {x}')

    with Watcher() as w:
        for path in paths:
            if exists(path):
                w.add(path, MODIFY, do_cmd)
            else:
                print(f' ! file not found ! {path}')


def on_changes():
    usage = f'''Usage:
        on_changes {{paths}} {{cmd}}

        Use % in {{cmd}} as a placeholder for {{path}}.

        ex : on_changes * cat %

        Use ^C to stop.
    '''
    *paths, cmd = argv[1:]
    try:
        _on_changes_run(paths, cmd)
    except Exception as x:
        print(f' ! {" ".join(command)} ! {x}')
        print(usage)
