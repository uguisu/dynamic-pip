# coding=utf-8
# author xin.he

import os
import unittest

from dynamicPip import DynamicPip, StaticResources

# declare target package
target_package = 'numpy==1.21.6'
target_package_list = [
    target_package,
    'importlib-metadata==7.0.2'
]
target_requirements_file_name = './test_req.txt'
target_requirements__map_file_name = './test_req_map.md'


class Test004(unittest.TestCase):

    def test_get_dependency_tree(self):
        """
        get dependency tree
        """

        # generate a test file
        with open(target_requirements_file_name, mode='w', encoding='utf-8') as f:
            f.writelines('\n'.join(target_package_list))

        dynamic_pip = DynamicPip()

        dynamic_pip.set_mirror_list([
            StaticResources.DEFAULT_PYPI_HOST,
            'https://mirrors.aliyun.com/pypi/simple',
        ])

        # install
        print(f'----- install from requirements file test -----')
        rtn = dynamic_pip.install_from_requirements_file(target_requirements_file_name)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # check package list
        rtn = DynamicPip.list_package()
        print(f'return result {rtn}\n')
        self.assertTrue('1.21.6' == rtn.get('numpy'))
        self.assertTrue('7.0.2' == rtn.get('importlib_metadata'))
        # backup a copy for further test
        confirm_package_dict = rtn.copy()

        dynamic_pip.generate_requires_map(target_requirements__map_file_name)

        # uninstall
        print(f'----- uninstall from requirements file test -----')
        rtn = dynamic_pip.remove_from_requirements_file(target_requirements_file_name)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # confirm result
        o_lines = []
        with open(target_requirements__map_file_name, mode='r', encoding='utf-8') as f:
            o_lines = f.readlines()

        for pkg_name in confirm_package_dict.keys():
            for _o_l in o_lines:
                # go through each line to find target package by name
                if _o_l.find(pkg_name) >= 0:
                    # change dict structure
                    confirm_package_dict[pkg_name] = True
                    break
        for k, v in confirm_package_dict.items():
            assert isinstance(v, bool)

        # remove useless file
        os.remove(target_requirements_file_name)
        os.remove(target_requirements__map_file_name)

        del dynamic_pip


if __name__ == '__main__':
    unittest.main()
