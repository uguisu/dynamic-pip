# coding=utf-8
# author xin.he

import unittest

from dynamicPip import DynamicPip

# declare target package
target_package = 'numpy==1.21.6'
requests_package = 'requests-2.31.0-py3-none-any.whl'
target_package_requests = 'requests==2.31.0'
target_package_list = [
    target_package,
    'scikit-learn==1.0.2'
]
target_package_list_with_file = [
    target_package,
    'scikit-learn==1.0.2',
    requests_package,
]


class Test006(unittest.TestCase):

    def test_make_sure_package_001(self):
        """
        make sure all required packages are installed
        - use default mirror
        - install all -> confirm -> make_sure -> confirm again
        """

        dynamic_pip = DynamicPip()

        # pre-install all packages
        print(f'----- make sure { ",".join(target_package_list) } test pre-install -----')
        rtn = dynamic_pip.install_package(target_package_list)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # check package list
        print(f'----- list { ",".join(target_package_list) } test -----')
        rtn = DynamicPip.list_package()
        print(f'return result {rtn}\n')
        self.assertTrue('1.21.6' == rtn.get('numpy'))
        self.assertTrue('1.0.2' == rtn.get('scikit-learn'))

        # call make sure
        print(f'----- call make sure { ",".join(target_package_list) } method -----')
        rtn = dynamic_pip.make_sure_packages(target_package_list)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # check package list
        print(f'----- list { ",".join(target_package_list) } test -----')
        rtn = DynamicPip.list_package()
        print(f'return result {rtn}\n')
        self.assertTrue('1.21.6' == rtn.get('numpy'))
        self.assertTrue('1.0.2' == rtn.get('scikit-learn'))

        del dynamic_pip

    def test_make_sure_package_002(self):
        """
        make sure all required packages are installed
        - use default mirror
        - install all -> delete one -> confirm -> make_sure -> confirm again
        """

        dynamic_pip = DynamicPip()

        # pre-install all packages
        print(f'----- make sure { ",".join(target_package_list) } test pre-install -----')
        rtn = dynamic_pip.install_package(target_package_list)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # uninstall numpy package
        print(f'----- uninstall {target_package} test -----')
        rtn = DynamicPip.remove_package(target_package)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # check package list
        print(f'----- list { ",".join(target_package_list) } test -----')
        rtn = DynamicPip.list_package()
        print(f'return result {rtn}\n')
        self.assertTrue(rtn.get('numpy') is None)
        self.assertTrue('1.0.2' == rtn.get('scikit-learn'))

        # call make sure
        print(f'----- call make sure { ",".join(target_package_list) } method -----')
        rtn = dynamic_pip.make_sure_packages(target_package_list)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # check package list
        print(f'----- list { ",".join(target_package_list) } test -----')
        rtn = DynamicPip.list_package()
        print(f'return result {rtn}\n')
        self.assertTrue('1.21.6' == rtn.get('numpy'))
        self.assertTrue('1.0.2' == rtn.get('scikit-learn'))

        del dynamic_pip

    def test_make_sure_package_003(self):
        """
        make sure all required packages are installed
        - use default mirror
        - install all -> delete one with whl -> confirm -> make_sure -> confirm again
        """

        dynamic_pip = DynamicPip()

        # pre-install all packages
        print(f'----- make sure { ",".join(target_package_list_with_file) } test pre-install -----')
        rtn = dynamic_pip.install_package(target_package_list)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # uninstall requests package
        print(f'----- uninstall {target_package_requests}, {target_package} test -----')
        rtn = DynamicPip.remove_package(target_package_requests)
        rtn = DynamicPip.remove_package(target_package)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # check package list
        print(f'----- list { ",".join(target_package_list) } test -----')
        rtn = DynamicPip.list_package()
        print(f'return result {rtn}\n')
        self.assertTrue(rtn.get('numpy') is None)
        self.assertTrue(rtn.get('requests') is None)
        self.assertTrue('1.0.2' == rtn.get('scikit-learn'))

        # call make sure
        print(f'----- call make sure { ",".join(target_package_list_with_file) } method -----')
        rtn = dynamic_pip.make_sure_packages(target_package_list_with_file)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # check package list
        print(f'----- list { ",".join(target_package_list_with_file) } test -----')
        rtn = DynamicPip.list_package()
        print(f'return result {rtn}\n')
        self.assertTrue('1.21.6' == rtn.get('numpy'))
        self.assertTrue('1.0.2' == rtn.get('scikit-learn'))
        self.assertTrue('2.31.0' == rtn.get('requests'))

        del dynamic_pip


if __name__ == '__main__':
    unittest.main()
