Project Manager
===============

The Project Manager provides support for managing application based on Python

    $ vim manage.py
    from pypm import ProjectManager

    pm = ProjectManager()

    @pm.command(messages=dict(type=str, nargs='+', help='echo messages'))
    def echo(messages):
        print messages

    if __name__ == '__main__':
        import sys
        pm.run_command(sys.argv[1:])

    $ python manage.py echo hello world
    ['hello', 'world']


Installing
----------

#### Global Project Setup

Install with pip:

    $ sudo pip install git+https://github.com/myevan/pypm.git

#### Local Project Setup

Setup project directory with pip:

    $ cd ~/Project

    $ mkdir Tools
    $ pip install git+https://github.com/myevan/pypm.git --target Tools

    $ touch Tools/__init__.py

    $ vim manage.py
    from Tools.pypm import ProjectManager
    ... 

#### Developer Setup

    $ git clone https://github.com/myevan/pypm.git
    $ cd pypm
    $ ./setup.py develop
