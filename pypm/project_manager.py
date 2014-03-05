# -*- coding:utf8 -*-
import os
import re
import code
import shutil
import argparse
import functools

from fnmatch import fnmatch

from codecs import BOM_UTF8

class PushDirectoryContext(object):
    def __init__(self, dir_name):
        self.target_dir_path = os.path.realpath(dir_name)
        self.prev_dir_path = None
 
    def __enter__(self):
        self.prev_dir_path = os.getcwd()
        os.chdir(self.target_dir_path)
        return self
 
    def __exit__(self, type, value, tb):
        os.chdir(self.prev_dir_path)

class FilterPathPattern(object):
    RECURSIVE_DIR_PATTERN = '...'

    def __init__(self, patterns):
        self.patterns = [
                re.compile(pattern.replace('...', '[\w\/]+')) 
                if '...' in pattern else pattern 
                for pattern in patterns]

    def __call__(self, path):
        for pattern in self.patterns:
            if isinstance(pattern, str):
                return fnmatch(path, pattern)
            else:
                return pattern.match(path)

class ProjectManager(object):
    class ExitCode(object):
        EMPTY_ARGUMENTS = -1
        WRONG_PROCESS = -2

    class Error(Exception):
        pass

    class ArgumentError(Error):
        pass

    def __init__(self):
        self.main_parser = argparse.ArgumentParser()
        self.sub_parsers = self.main_parser.add_subparsers()

    def command(self, **option_table):
        def handler(func):
            option_names = func.func_code\
                               .co_varnames[:func.func_code.co_argcount]

            @functools.wraps(func)
            def wrapper(ns):
                kwargs = dict()
                for option_name in option_names:
                    option_info_dict = option_table[option_name]
                    option_nargs = option_info_dict.get('nargs', None)
                    if option_nargs == 1:
                        kwargs[option_name] = getattr(ns, option_name)[0]
                    else:
                        kwargs[option_name] = getattr(ns, option_name)

                return func(**kwargs)

            def create_sub_parser(func_name, func_doc):
                new_sub_parser = self.sub_parsers.add_parser(
                    func_name, help=func_doc)

                for option_name in option_names:
                    option_info_dict = option_table[option_name]
                    option_flag = option_info_dict.get('flag', None)
                    if option_flag:
                        del option_info_dict['flag']
                        new_sub_parser.add_argument(
                            option_flag, '--' + option_name, **option_info_dict)
                    else:
                        new_sub_parser.add_argument(
                            option_name, **option_info_dict)

                return new_sub_parser

            sub_parser = create_sub_parser(func.func_name, func.func_doc)
            sub_parser.set_defaults(func=wrapper)
        return handler

    def add_common_argument(self, *args, **kwargs):
        self.main_parser.add_argument(*args, **kwargs) 
    
    def run_command(self, cmd_args):
        if cmd_args is None or len(cmd_args) == 0:
            self.main_parser.print_help()
            return self.ExitCode.EMPTY_ARGUMENTS

        ns = self.main_parser.parse_args(cmd_args)
        try:
            return ns.func(ns)
        except self.Error:
            return self.ExitCode.WRONG_PROCESS

    @staticmethod
    def run_program(exec_path, exec_args):
        cmd_line = '%s %s' % (exec_path, ' '.join(exec_args))
        print(cmd_line)
        return os.system(cmd_line)

    @staticmethod
    def run_python_shell(title, local_dict):
        code.interact(title, local=local_dict)

    @staticmethod
    def push_directory(dir_name):
        return PushDirectoryContext(dir_name)

    @staticmethod
    def find_dir_path_iter(
            base_dir_path,
            path_patterns=None,
            filter_dir_name=None,
            is_all_dirs=False):

        filter_path_pattern = FilterPathPattern(path_patterns) if path_patterns else None

        for parent_dir_path, dir_names, file_names in os.walk(base_dir_path):
            if filter_path_pattern is None or filter_path_pattern(parent_dir_path[len(base_dir_path) + 1:]):
                yield parent_dir_path

            if not is_all_dirs:
                for dir_name in list(dir_names):
                    if dir_name[0] == '.':
                        dir_names.remove(dir_name)

            if filter_dir_name:
                for dir_name in list(dir_names):
                    if not filter_dir_name(dir_name):
                        dir_names.remove(dir_name)

    @staticmethod
    def find_file_path_iter(
            base_dir_path,
            path_patterns=None,
            filter_dir_name=None,
            filter_file_name=None,
            filter_file_ext=None,
            filter_file_path=None,
            is_all_files=False):

        filter_path_pattern = FilterPathPattern(path_patterns) if path_patterns else None

        for parent_dir_path, dir_names, file_names in os.walk(base_dir_path):
            if not is_all_files:
                for dir_name in list(dir_names):
                    if dir_name[0] == '.':
                        dir_names.remove(dir_name)

            if filter_dir_name:
                for dir_name in list(dir_names):
                    if not filter_dir_name(dir_name):
                        dir_names.remove(dir_name)
            
            for file_name in file_names:
                if not is_all_files:
                    if file_name[0] == '.':
                        continue

                if filter_file_name is None or filter_file_name(file_name):
                    file_ext = os.path.splitext(file_name)[1].lower()
                    if filter_file_ext is None or filter_file_ext(file_ext):
                        file_path = os.path.join(parent_dir_path, file_name)
                        if filter_file_path is None or filter_file_path(file_path):
                            if filter_path_pattern is None or filter_path_pattern(file_path[len(base_dir_path) + 1:]):
                                yield file_path

    @staticmethod
    def add_utf8_bom(file_path):
        file_bom = open(file_path, 'rb').read(len(BOM_UTF8))
        if file_bom != BOM_UTF8:
            file_data = open(file_path, 'rb').read()
            open(file_path, 'wb').write(BOM_UTF8 + file_data)

    @staticmethod
    def remove_utf8_bom(file_path):
        file_bom = open(file_path, 'rb').read(len(BOM_UTF8))
        if file_bom == BOM_UTF8:
            file_data = open(file_path, 'rb').read()
            open(file_path, 'wb').write(file_data[len(BOM_UTF8):])

    @classmethod
    def remove_trees_by_patterns(cls, base_dir_path, path_patterns):
        dir_paths = [dir_path 
                for dir_path in cls.find_dir_path_iter(
                    base_dir_path, path_patterns, is_all_dirs=True)]
        
        for dir_path in reversed(dir_paths):
            shutil.rmtree(dir_path)

if __name__ == '__main__':
    pm = ProjectManager()

    @pm.command(msg=dict(type=str, nargs='+'))
    def test(msg):
        print os.getcwd()
        with pm.push_directory('..'):
            print os.getcwd()
            for file_path in pm.find_file_path_iter('.', path_patterns=['pypm/....py']):
                print file_path

    pm.run_command(['test', 'haha'])
