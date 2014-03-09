import pytest

import os

from pypm import ProjectManager

FILE_PATH = os.path.realpath(__file__)
MODULE_DIR_PATH = os.path.dirname(FILE_PATH)
PROJECT_DIR_PATH = os.path.dirname(MODULE_DIR_PATH)

@pytest.fixture(scope="module")
def __get_project_manager():
    return ProjectManager()

def test_finding_python_in_pypm():
    pm = __get_project_manager()
    with pm.push_directory(PROJECT_DIR_PATH) as parent_dir:
        file_path_prefix = os.path.join(PROJECT_DIR_PATH, 'pypm')
        for file_path in pm.find_file_path_iter(path_patterns=['pypm/....py']):
            assert(file_path.startswith(file_path_prefix))
            assert(file_path.endswith('.py'))

def test_managing_directories_and_files():
    pm = __get_project_manager()
    assert(not os.access('temp', os.R_OK))

    pm.make_directory('temp')
    assert(os.access('temp', os.R_OK))

    pm.touch_file('temp/empty')
    assert(os.access('temp/empty', os.R_OK))

    pm.make_directory('temp/t1')
    assert(os.access('temp/t1', os.R_OK))

    pm.make_directory('temp/t2')
    assert(os.access('temp/t2', os.R_OK))

    pm.make_directory('temp/t3')
    assert(os.access('temp/t2', os.R_OK))

    pm.touch_file('temp/t1/f1')
    assert(os.access('temp/t1/f1', os.R_OK))

    pm.touch_file('temp/t2/f2')
    assert(os.access('temp/t2/f2', os.R_OK))

    pm.touch_file('temp/t3/f3')
    assert(os.access('temp/t3/f3', os.R_OK))

    pm.touch_file('temp/t3/f3-2')
    assert(os.access('temp/t3/f3-2', os.R_OK))

    pm.make_symbolic_link('temp/t3/f3-2', 'temp/t3/f3-2s')
    assert(open('temp/t3/f3-2', 'rb').read() == open('temp/t3/f3-2s', 'rb').read())

    pm.remove_tree('temp/t1', is_testing=False)
    assert(not os.access('temp/t1', os.R_OK))

    pm.remove_trees_by_patterns(['temp/*2'], is_testing=False)
    assert(not os.access('temp/t2', os.R_OK))

    pm.remove_files_by_patterns(['temp/*/*3'], is_testing=False)
    assert(not os.access('temp/t3/f3', os.R_OK))

    pm.remove_symbolic_link('temp/t3/f3-2s', is_testing=False)
    assert(not os.access('temp/t3/f3-2s', os.R_OK))

    pm.remove_file('temp/t3/f3-2', is_testing=False)
    assert(not os.access('temp/t3/f3-2', os.R_OK))

    pm.remove_tree('temp', is_testing=False)
    assert(not os.access('temp', os.R_OK))
