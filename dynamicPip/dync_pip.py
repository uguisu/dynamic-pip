# coding=utf-8
# author xin.he
import os.path
import re
import subprocess
import sys
from typing import Union, List

from dynamicPip import MirrorManager, StaticResources
from dynamicPip.utility import get_site_packages_path, is_path_exist

# some packages are internal packages which should be excluded.
# exclude package list
exclude_packages = {
    'pip': 'pip',
    'setuptools': 'setuptools',
    'wheel': 'wheel',
    'pkg-resources': 'pkg-resources',
    'pkg_resources': 'pkg_resources',
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
        # extra index url
        self._extra_index_url = None

    def set_mirror_list(self, custom_mirror_list=None):
        """
        set custom mirror list and then update the fastest host
        :param custom_mirror_list: mirror list
        """
        # update mirror list
        self.mirror_manager.mirror_list = custom_mirror_list
        # update fastest host
        self.fastest_host = self.mirror_manager.get_best_mirror()

    @property
    def extra_index_url(self):
        """
        get "extra-index-url"
        """
        return self._extra_index_url

    @extra_index_url.setter
    def extra_index_url(self, extra_index_url: str = ''):
        """
        set "extra-index-url"
        :param extra_index_url: an url target to extra index
        """
        if extra_index_url is None or '' == extra_index_url.strip():
            # skip blank value
            self._extra_index_url = None
            return
        # TODO URL check
        self._extra_index_url = extra_index_url

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

    def install_package(self, args: Union[str, List]) -> int:
        """
        install package(s)
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

        cli_array = [sys.executable, '-m', 'pip', 'install']
        cli_array.extend(['-i', self.fastest_host])

        # determine extra_index_url
        if self.extra_index_url is not None and '' != self.extra_index_url.strip():
            cli_array.extend(['--extra-index-url', self.extra_index_url])

        if isinstance(args, list):
            cli_array.extend(args)
        else:
            cli_array.append(args)

        try:
            rtn = subprocess.check_call(cli_array)
        except Exception:
            raise RuntimeError(f'Target package can not be installed. '
                               f'Please either try again later or install it manually')

        return rtn

    @staticmethod
    def remove_package(args: Union[str, List]) -> int:
        """
        remove package(s)
        :param args: package name list and other parameters.
                     refer: https://pip.pypa.io/en/stable/cli/pip_install/
        :return: 0 - success
        """
        # verify
        if args is None:
            raise ValueError('invalid package name')

        rtn = 0

        _cli = [sys.executable, '-m', 'pip', 'uninstall', '-y']
        if isinstance(args, list):
            _cli.extend(args)
        else:
            _cli.append(args)

        try:
            rtn = subprocess.check_call(_cli)
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
        export requirement packages into file
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
            out_path = os.path.join('', requirements_file)
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
    def generate_requires_map(output_file='requirement_map.md'):
        """
        generate requires map

        fetch all installed packages of current project, sort out dependencies, and generate a graph

        :param output_file: output result as a markdown file
        """

        from dynamicPip.utility import (
            MetaDataEntity,
            get_meta_data_file_reader,
            beauty_output_doc,
        )

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

        def _generate_graph_body(pgk_entity_dict) -> str:
            """
            generate graph body
            """
            _l = []
            for k, v in pgk_entity_dict.items():
                _l.append(v.format_to_markdown())

            return '\n'.join(_l)

        def _generate_graph_link(pgk_entity_dict) -> str:
            """
            generate graph link
            """
            _l = []
            for k, v in pgk_entity_dict.items():
                # add link with main project
                _l.append(f'MyProject --> {k}')

                for dep_pkg in v.requires_dist.keys():
                    # add all dependency packages
                    _l.append(f'{k} --> {dep_pkg}')

            return '\n'.join(_l)

        # start ==========================

        # get site-package path
        site_pgk_path = get_site_packages_path()

        # load all METADATA file
        all_pkg_meta_data_as_dict = _load_meta_data_file_to_dict(site_pgk_path)

        # fetch all installed packages of current project
        pip_package_dict = DynamicPip.list_package()

        # some packages may do not contain METADATA, so merge direct loaded meta file dict and system pip list
        # key: package name, val = MetaDataEntity
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

        # get back to the packages which managed by pip to make sure all packages will be output
        for _pip_pkg in pip_package_dict.keys():
            pip_ver = pip_package_dict.get(_pip_pkg)

            # generate a dummy entity
            mde = MetaDataEntity()
            mde.name = _pip_pkg
            mde.version = pip_ver

            merged_pgk_entity_dict[_pip_pkg] = mde

            # output warning
            print(f'invite {_pip_pkg} to relationship map')

        # all_pkg_meta_data_as_dict should equal to merged_pgk_entity_dict
        if len(merged_pgk_entity_dict) != len(all_pkg_meta_data_as_dict):
            # some package name might be a little different. 'pkg_resources' and 'pkg-resources' for instance are
            # actually the same package
            print('WARNING!!! Some package names have exceptions.')

        # generate output doc
        body_str = _generate_graph_body(merged_pgk_entity_dict)
        link_str = _generate_graph_link(merged_pgk_entity_dict)

        md_lines = beauty_output_doc(
            StaticResources.DEFAULT_RELATIONSHIP_MAP_TEMPLATE.format(
                body=body_str,
                links=link_str
            )
        )

        try:
            # generate requirement map file
            out_path = os.path.join('', output_file)
            out_path = os.path.abspath(out_path)
            with open(out_path, mode='w', encoding='utf-8') as f:
                f.write('```mermaid\n')
                f.write('\n'.join(md_lines))
                f.write('\n```')

            print(f'Export to {out_path} success.')
        except Exception:
            raise RuntimeError(f'Target requirement map file can not be exported. ')

    def make_sure_packages(self, pkgs: Union[str, List]) -> int:
        """
        make sure all package(s) has been installed.

        :param pkgs: package name(with/without version) list.
        """

        # verify
        if pkgs is None:
            raise ValueError('invalid package name')

        rtn = 0

        pkg_dict: dict = self.list_package()
        missing_list: list = []
        # go through all target package
        for item_pkg in pkgs:
            if pkg_dict.get(item_pkg.split('==')[0]) is None and not item_pkg.endswith('.whl'):
                # find a package that not installed yet
                missing_list.append(item_pkg)
                continue

            if item_pkg.endswith('.whl'):
                # find a 'whl' file
                missing_list.append(item_pkg)
                continue

        if len(missing_list) > 0:
            rtn = self.install_package(missing_list)

        return rtn
