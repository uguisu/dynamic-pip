# coding=utf-8
# author xin.he

import subprocess
import sys
import re


# class PIP:
#     """
#     Super PIP
#     """
#     @staticmethod
#     def install_single_package(args: str = None) -> int:
#         """
#         install single package
#         :return:
#         """
#         from pip._internal.cli.main import main as _main  # isort:skip # noqa
#
#         # verify
#         if args is None or not isinstance(args, str):
#             raise ValueError('invalid package name')
#
#         # generate command line
#         sys.argv = ["pip", 'install', args]
#         return _main()
#
#     @staticmethod
#     def list_packages():
#         from pip._internal.cli.main import main as _main  # isort:skip # noqa
#         # generate command line
#         sys.argv = ["pip", 'list']
#         return _main()


# exclude package list
exclude_packages = {
    'pip': 'pip',
    'pkg-resources': 'pkg-resources',
    'setuptools': 'setuptools',
    'wheel': 'wheel',
}


class DynamicPip:
    """
    dynamic pip
    """
    @staticmethod
    def list_package() -> dict:
        """
        list packages
        :return: package dict
        """
        _pip_lst = subprocess.check_output([sys.executable, '-m', 'pip', 'list'])
        _pip_lst = str(_pip_lst, 'utf-8')

        # Top two rows are "table header" info which can be ignored.
        _pip_lst = _pip_lst.splitlines()[2:]

        # key: package name, value: version
        rtn = {}

        for _package_info in _pip_lst:
            # remove continuous space
            _package_info = re.sub(r'(\s)+', ' ', _package_info.strip(), count=1)
            # split by SPACE
            _package_info = _package_info.split(' ')
            if exclude_packages.get(_package_info[0]) is None:
                rtn[_package_info[0]] = _package_info[1]

        del _pip_lst

        return rtn

    @staticmethod
    def install_single_package(*args) -> int:
        """
        install single package
        :param args: package name list and other parameters.
                     refer: https://pip.pypa.io/en/stable/cli/pip_install/
        :return: 0 - success
        """
        # verify
        if args is None:
            raise ValueError('invalid package name')

        rtn = 0

        try:
            rtn = subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + list(args))
        except Exception:
            raise RuntimeError(f'Target package can not be installed. '
                               f'Please either try again later or install it manually')

        return rtn
