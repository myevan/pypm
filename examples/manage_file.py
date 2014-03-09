#!/usr/bin/env python
from pypm import ProjectManager

pm = ProjectManager()

@pm.command(hint=dict(type=str, nargs=1, help='file path or name hint'))
def find(hint):
    print 'FOUND_FILE_PATH:', pm.smart_find_file_path(hint)

if __name__ == '__main__':
    import sys
    pm.run_command(sys.argv[1:])
