# -*- coding:utf8 -*-
import os
import code
import argparse
import functools


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

if __name__ == '__main__':
    pm = ProjectManager()

    @pm.command(msg=dict(type=str, nargs='+'))
    def test(msg):
        print msg

    pm.run_command(['test', 'haha'])
