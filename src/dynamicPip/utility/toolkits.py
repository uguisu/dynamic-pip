# coding=utf-8
# author xin.he
import sys
import os


def is_under_virtual_environment() -> bool:
    """
    verify if current process is running under a virtual environment
    """
    return sys.prefix != sys.base_prefix


def is_path_exist(path_or_file: str) -> bool:
    """
    verify target path or file exist
    """
    return os.path.exists(path_or_file)


def get_site_packages_path() -> str:
    """
    get site-package path

    support:
    - global environment
    - virtual environment
    - TODO conda
    """

    def _is_a_possible_path(path: str) -> bool:
        """
        use the most common package names to predict target path is a possible site-package path
        """

        if is_path_exist(os.path.join(path, 'pip')):
            return True

        if is_path_exist(os.path.join(path, 'pkg_resources')):
            return True

        if is_path_exist(os.path.join(path, '__pycache__')):
            return True

        # target path do not look like a possible site-package path
        return False

    def _using_global_env() -> str:
        """
        global env
        """
        import site

        # get whole list
        site_list = site.getsitepackages()

        # TODO debug
        print(f'site list:')
        for sl in site_list:
            print(sl, ' --> ', is_path_exist(sl))

        rtn = None
        for sl in site_list:

            if is_path_exist(sl) and _is_a_possible_path(sl):
                # find the first possible path, then return
                rtn = sl
                break

        del site_list

        return rtn

    def _using_virtualenv() -> str:
        """
        with virtualenv getsitepackages is not available, so turn to 'sysconfig' instead
        """
        import sysconfig
        return sysconfig.get_paths()["purelib"]

    rtn_site_path = _using_virtualenv() if is_under_virtual_environment() else _using_global_env()

    return rtn_site_path


def read_meta_data_file(file: str):
    """
    read METADATA file info into entity
    :param file: METADATA file name & path
    :return: TODO entity
    """
    pass
