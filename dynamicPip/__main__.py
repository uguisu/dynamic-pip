# coding=utf-8
# author xin.he
import argparse
import sys

from dynamicPip import DynamicPip, StaticResources


def _argparse():
    """
    get input arguments
    :return: argument object
    """
    parser = argparse.ArgumentParser(
        description="Help users to dynamically manage python package resources"
    )

    parser.add_argument('--list-package',
                        action='store_true',
                        dest='list_package',
                        default=False,
                        help='show all packages as list')
    parser.add_argument('--require-map',
                        action='store_true',
                        # dest='require_map',
                        default=False,
                        help='generate a requirement/dependence map for all installed packages')
    parser.add_argument('-f',
                        action='store',
                        dest='file_name',
                        default=None,
                        help='Output file\'s name')

    return parser.parse_args(), parser


def main():
    """
    main method
    """
    args, __p = _argparse()

    dynamic_pip = DynamicPip()

    if args.list_package:
        print(dynamic_pip.list_package())
        sys.exit(StaticResources.SUCCESS_EXIT)

    if args.require_map:
        # verify output file name has been specified
        if args.file_name is not None:
            _f = str(args.file_name)
        else:
            _f = 'requirement_map.md'
        print(dynamic_pip.generate_requires_map(_f))
        sys.exit(StaticResources.SUCCESS_EXIT)

    # if no command is hit, output help info
    __p.print_help()
