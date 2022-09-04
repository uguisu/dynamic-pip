# coding=utf-8
# author xin.he

import unittest

from dynamicPip import DynamicPip, StaticResources

# declare target package
target_package = 'numpy==1.21.6'


class Test001(unittest.TestCase):

    def test_install_single_package_001(self):
        """
        install single package
        - use default mirror
        """

        dynamic_pip = DynamicPip()

        # install
        print(f'----- install {target_package} test -----')
        rtn = dynamic_pip.install_single_package(target_package)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # check package list
        print(f'----- list {target_package} test -----')
        rtn = DynamicPip.list_package()
        print(f'return result {rtn}\n')
        self.assertTrue('1.21.6' == rtn.get('numpy'))

        # uninstall single package
        print(f'----- uninstall {target_package} test -----')
        rtn = DynamicPip.remove_single_package(target_package)
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
        rtn = dynamic_pip.install_single_package(target_package)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # check package list
        print(f'----- list {target_package} test -----')
        rtn = DynamicPip.list_package()
        print(f'return result {rtn}\n')
        self.assertTrue('1.21.6' == rtn.get('numpy'))

        # uninstall single package
        print(f'----- uninstall {target_package} test -----')
        rtn = DynamicPip.remove_single_package(target_package)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        del dynamic_pip


if __name__ == '__main__':
    unittest.main()
