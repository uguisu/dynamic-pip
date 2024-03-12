# coding=utf-8
# author xin.he

import os
import unittest

from dynamicPip import DynamicPip, StaticResources

# declare target package
target_package = 'numpy==1.21.6'
target_package_list = [
    target_package,
    'scikit-learn==1.0.2'
]
target_requirements_file_name = './test_req.txt'


class Test001(unittest.TestCase):

    def test_install_single_package_001(self):
        """
        install single package
        - use default mirror
        """

        dynamic_pip = DynamicPip()

        # install
        print(f'----- install {target_package} test -----')
        rtn = dynamic_pip.install_package(target_package)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # check package list
        print(f'----- list {target_package} test -----')
        rtn = DynamicPip.list_package()
        print(f'return result {rtn}\n')
        self.assertTrue('1.21.6' == rtn.get('numpy'))

        # uninstall single package
        print(f'----- uninstall {target_package} test -----')
        rtn = DynamicPip.remove_package(target_package)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        del dynamic_pip

    def test_install_single_package_002(self):
        """
        install single package
        - use faster mirror
        """

        dynamic_pip = DynamicPip()

        dynamic_pip.set_mirror_list([
            StaticResources.DEFAULT_PYPI_HOST,
            'https://mirrors.aliyun.com/pypi/simple',
        ])

        # install
        print(f'----- install {target_package} test -----')
        rtn = dynamic_pip.install_package(target_package)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # check package list
        print(f'----- list {target_package} test -----')
        rtn = DynamicPip.list_package()
        print(f'return result {rtn}\n')
        self.assertTrue('1.21.6' == rtn.get('numpy'))

        # uninstall single package
        print(f'----- uninstall {target_package} test -----')
        rtn = DynamicPip.remove_package(target_package)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        del dynamic_pip

    def test_install_from_requirements_file_001(self):
        """
        install from requirements file
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
        self.assertTrue('1.0.2' == rtn.get('scikit-learn'))

        # uninstall
        print(f'----- uninstall from requirements file test -----')
        rtn = dynamic_pip.remove_from_requirements_file(target_requirements_file_name)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # remove useless file
        os.remove(target_requirements_file_name)

        del dynamic_pip


if __name__ == '__main__':
    unittest.main()
