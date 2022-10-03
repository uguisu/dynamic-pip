# coding=utf-8
# author xin.he
import os.path
import re
import subprocess
import sys

from dynamicPip import MirrorManager, StaticResources
from dynamicPip.utility import get_site_packages_path, is_path_exist

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
        # update mirror list
        self.mirror_manager.mirror_list = custom_mirror_list
        # update fastest host
        self.fastest_host = self.mirror_manager.get_best_mirror()

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

    def install_single_package(self, *args) -> int:
        """
        install single package
        :param args: package name list and other parameters.
                     refer: https://pip.pypa.io/en/stable/cli/pip_install/
        :return: 0 - success
        """
        # verify
        if args is None:
            raise ValueError('invalid package name')

        # show mirror
        print(f'The mirror site used by the current operation is: {self.fastest_host}')

        rtn = 0

        try:
            rtn = subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install'] +
                ['-i', self.fastest_host] +
                list(args)
            )
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

    def install_from_requirements_file(self, requirements_file):
        """
        install from requirements file
        :param requirements_file: requirements file
        :return: 0 - success
        """

        # TODO multiprocess install

        # verify
        if requirements_file is None:
            raise ValueError('invalid file name')

        # show mirror
        print(f'The mirror site used by the current operation is: {self.fastest_host}')

        rtn = 0

        try:
            rtn = subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install'] +
                ['-i', self.fastest_host] +
                ['-r', requirements_file]
            )
        except Exception:
            raise RuntimeError(f'Target package can not be installed. '
                               f'Please either try again later or install it manually')

        return rtn

    @staticmethod
    def remove_from_requirements_file(requirements_file):
        """
        remove from requirements file
        :param requirements_file: requirements file
        :return: 0 - success
        """

        # verify
        if requirements_file is None:
            raise ValueError('invalid file name')

        rtn = 0

        try:
            rtn = subprocess.check_call(
                [sys.executable, '-m', 'pip', 'uninstall', '-y'] +
                ['-r', requirements_file]
            )
        except Exception:
            raise RuntimeError(f'Target package can not be removed. '
                               f'Please either try again later or uninstall it manually')

        return rtn

    @staticmethod
    def export_requirements_file(requirements_file=StaticResources.DEFAULT_REQUIREMENT_FILE):
        """
        export requirements file
        :param requirements_file: requirements file. default file name is 'requirements.txt'
        :return: 0 - success
        """

        # verify
        if requirements_file is None:
            raise ValueError('invalid file name')

        _pip_lst = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        _pip_lst = str(_pip_lst, 'utf-8')

        try:
            # generate requirement file
            out_path = os.path.join('.', requirements_file)
            out_path = os.path.abspath(out_path)
            with open(out_path, mode='w', encoding='utf-8') as f:
                for _package_info in _pip_lst:
                    f.writelines('\n'.join(_package_info))

            print(f'Export to {out_path} success.')
        except Exception:
            raise RuntimeError(f'Target requirement file can not be exported. '
                               f'Please either try again later or execute \'freeze\' command manually')

        return 0

    @staticmethod
    def generate_requires_map() -> dict:
        """
        generate requires map

        fetch all installed packages of current project, sort out dependencies, and generate a graph
        """

        from dynamicPip.utility import MetaDataEntity
        from dynamicPip.utility import get_meta_data_file_reader

        def _get_sub_folder_list(target_path: str) -> list:
            """
            get sub-folder name as list
            :param target_path: target path
            """
            rtn = []
            for _t_sub in os.listdir(target_path):
                # generate real path
                _t_sub = os.path.join(target_path, _t_sub)
                if os.path.isdir(_t_sub):
                    # only append folder, skip all files
                    rtn.append(_t_sub)

            return rtn

        def _load_meta_data_file_to_dict(site_pp) -> dict:
            """
            load METADATA file info to a dict
            :param site_pp: site-package path
            :return: package - METADATA dict. key: package name; val: METADATA entity
            """
            # get sub-folder list
            sub_folder_list = _get_sub_folder_list(site_pp)
            # declare return dict
            pkg_meta_data_dict = {}

            for _sub_folder in sub_folder_list:
                # go through each sub folder, load METADATA info
                _sub_folder = os.path.join(site_pp, _sub_folder, 'METADATA')

                if is_path_exist(_sub_folder):
                    # find METADATA file
                    entity_temp = get_meta_data_file_reader().read(_sub_folder)

                    if exclude_packages.get(entity_temp.name) is None:
                        # skip packages which in excluded list
                        pkg_meta_data_dict[entity_temp.name] = entity_temp

            return pkg_meta_data_dict

        # start ==========================

        # get site-package path
        site_pgk_path = get_site_packages_path()

        # load all METADATA file
        all_pkg_meta_data_as_dict = _load_meta_data_file_to_dict(site_pgk_path)

        # fetch all installed packages of current project
        pip_package_dict = DynamicPip.list_package()

        # some packages may do not contain METADATA, so merge direct loaded meta file dict and system pip list
        merged_pgk_entity_dict = {}

        for _meta_pkg in all_pkg_meta_data_as_dict.keys():
            # try to fetch data from both dict
            m_pkg_item = all_pkg_meta_data_as_dict.get(_meta_pkg)
            p_pkg_ver = pip_package_dict.pop(_meta_pkg, None)

            if p_pkg_ver is not None:
                # direct loaded METADATA file exist in pip list
                merged_pgk_entity_dict[_meta_pkg] = m_pkg_item
            else:
                # TODO find an package which do not managed by PIP ?
                print(f'Find package {_meta_pkg} do not managed by PIP. Please confirm manually.', file=sys.stderr)

        # all_pkg_meta_data_as_dict should equal to merged_pgk_entity_dict
        assert len(merged_pgk_entity_dict) == len(all_pkg_meta_data_as_dict)

        # get back to the packages which managed by pip to make sure all packages will be output

        # TODO debug
        # print(f'current pip list length = {len(pip_package_dict)}')

        for _pip_pkg in pip_package_dict.keys():
            pip_ver = pip_package_dict.pop(_pip_pkg)

            # generate a dummy entity
            mde = MetaDataEntity()
            mde.name = _pip_pkg
            mde.version = pip_ver

            merged_pgk_entity_dict[_pip_pkg] = mde

            # output warning
            print(f'invite {_pip_pkg} to relationship map')

        return merged_pgk_entity_dict
