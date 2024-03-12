# coding=utf-8
# author xin.he
import sys
import os

from dynamicPip.utility import MetaDataFileReader


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


def get_meta_data_file_reader() -> MetaDataFileReader:
    """
    get read METADATA file reader
    :return: MetaDataFileReader instance
    """

    # if is_current_python_version_less_than_or_equal((3, 7, 9999)):
    #     # py version 3.7 ~
    #     from dynamicPip.utility import MetaDataFileReader37
    #     meta_reader = MetaDataFileReader37()
    # else:
    #     # py version 3.8 ~
    #     from dynamicPip.utility import MetaDataFileReader38
    #     meta_reader = MetaDataFileReader38()

    # TODO importlib.metadata is new function from python 3.8
    from dynamicPip.utility import MetaDataFileReader37
    meta_reader = MetaDataFileReader37()

    # verify type
    assert isinstance(meta_reader, MetaDataFileReader)

    return meta_reader


def is_current_python_version_less_than_or_equal(expected_version_tuple: tuple) -> bool:
    """
    verify whether current python version is less than or equal to expected value
    :param expected_version_tuple: expected python version.
        Python version as tuple (major, minor, patchlevel) of strings.
    :return: true / false
    """

    if len(expected_version_tuple) < 2:
        raise ValueError('Python version as tuple (major, minor, patchlevel)')

    import platform

    current_py_ver = platform.python_version_tuple()

    # get minimum length
    loop_amount = min(len(expected_version_tuple), len(current_py_ver))

    rtn = True
    for i in range(loop_amount):
        rtn = rtn and (int(current_py_ver[i]) <= int(expected_version_tuple[i]))

    return rtn


def beauty_output_doc(doc_lines) -> list:
    """
    format each line to a more understandable format
    :param doc_lines: line list, a string or a list
    :return: formatted line list
    """

    if isinstance(doc_lines, str):
        wrk_doc_lines = doc_lines.splitlines()
    elif isinstance(doc_lines, list):
        wrk_doc_lines = doc_lines.copy()
    else:
        raise ValueError('Only string or list type can be formatted')

    rtn = []

    for original_line in wrk_doc_lines:
        _l = original_line.strip()
        if len(_l) > 0:
            rtn.append(_l)

    return rtn
