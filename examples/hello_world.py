#!/usr/bin/env python
from pypm import ProjectManager

pm = ProjectManager()

@pm.command(messages=dict(type=str, nargs='+', help='echo messages'))
def echo(messages):
 ', hint)   """
    echo messages
    """
    print messages

if __name__ == '__main__':
    import sys
    pm.run_command(sys.argv[1:])
