# coding=utf-8
# author xin.he

import subprocess
import sys
import re

from dynamicPip import MirrorManager, StaticResources

# some packages are internal packages which should be excluded.
# exclude package list
exclude_packages = {
    'pip': 'pip',
    'setuptools': 'setuptools',
    'wheel': 'wheel',
}


class DynamicPip:
    """
    dynamic pip
    """

    def __init__(self):
        """
        init
        """
        self.mirror_manager = MirrorManager()
        # default mirror
        self.fastest_host = StaticResources.DEFAULT_PYPI_HOST

    def set_mirror_list(self, custom_mirror_list=None):
        """
        set custom mirror list and then update the fastest host
        :param custom_mirror_list: mirror list
        """

        # verify
        if custom_mirror_list is not None \
                and isinstance(custom_mirror_list, list) \
                and 0 < len(custom_mirror_list):
            # update mirror list
            self.mirror_manager.mirror_list = custom_mirror_list
            # update fastest host
            self.fastest_host = self.mirror_manager.get_best_mirror()
        else:
            raise ValueError('Please setup a valid mirror list and try again.')

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

    @staticmethod
    def remove_single_package(*args) -> int:
        """
        remove single package
        :param args: package name list and other parameters.
                     refer: https://pip.pypa.io/en/stable/cli/pip_install/
        :return: 0 - success
        """
        # verify
        if args is None:
            raise ValueError('invalid package name')

        rtn = 0

        try:
            rtn = subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', '-y'] + list(args))
        except Exception:
            raise RuntimeError(f'Target package can not be removed. '
                               f'Please either try again later or uninstall it manually')

        return rtn
