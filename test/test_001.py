# coding=utf-8
# author xin.he

from dynamicPip import DynamicPip
import unittest

# declare target package
target_package = 'numpy==1.21.6'


class Test001(unittest.TestCase):

    def test_install_single_package(self):
        """
        install single package
        """
        # install
        print(f'----- install {target_package} test -----')
        rtn = DynamicPip.install_single_package(target_package)
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


if __name__ == '__main__':
    unittest.main()
