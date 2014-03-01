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
Install with pip:

    $ pip install git+https://github.com/myevan/pypm.git

or download the lastest version from version control

    $ git clone https://github.com/myevan/pypm.git
    $ cd pypm
    $ ./setup.py develop


