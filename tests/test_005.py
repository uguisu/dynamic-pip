# coding=utf-8
# author xin.he

import unittest

from dynamicPip import DynamicPip
from test_helper import download_file

# declare target package
numpy_package = 'numpy-1.26.4-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl'
numpy_package_url = ('https://mirrors.aliyun.com/pypi/packages/54/30/'
                     'c2a907b9443cf42b90c17ad10c1e8fa801975f01cb9764f3f8eb8aea638b/'
                     'numpy-1.26.4-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl')
target_package_numpy = 'numpy==1.26.4'

pandas_package = 'pandas-2.2.1-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl'
pandas_package_url = ('https://mirrors.aliyun.com/pypi/packages/1a/5e/'
                      '71bb0eef0dc543f7516d9ddeca9ee8dc98207043784e3f7e6c08b4a6b3d9/'
                      'pandas-2.2.1-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl')
target_package_pandas = 'pandas==2.2.1'

requests_package = 'requests-2.31.0-py3-none-any.whl'
requests_package_url = ('https://mirrors.aliyun.com/pypi/packages/70/8e/'
                        '0e2d847013cb52cd35b38c009bb167a1a26b2ce6cd6965bf26b47bc0bf44/'
                        'requests-2.31.0-py3-none-any.whl')
target_package_requests = 'requests==2.31.0'


target_package_list = [
    requests_package,
    pandas_package
]


class Test005(unittest.TestCase):

    def test_install_single_package_from_file_001(self):
        """
        install single package from file
        - use default mirror
        """

        download_file(url=numpy_package_url, filename=numpy_package)

        dynamic_pip = DynamicPip()

        # install
        print(f'----- install {target_package_numpy} from file test -----')
        rtn = dynamic_pip.install_single_package(numpy_package)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # check package list
        print(f'----- list {target_package_numpy} test -----')
        rtn = DynamicPip.list_package()
        print(f'return result {rtn}\n')
        self.assertTrue('1.26.4' == rtn.get('numpy'))

        # uninstall single package
        print(f'----- uninstall {target_package_numpy} from file test -----')
        rtn = DynamicPip.remove_single_package(target_package_numpy)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        del dynamic_pip

    def test_install_multiple_packages_from_file_002(self):
        """
        install multiple packages from file
        - use default mirror
        """

        download_file(url=requests_package_url, filename=requests_package)
        download_file(url=pandas_package_url, filename=pandas_package)

        dynamic_pip = DynamicPip()

        # install
        print(f'----- install {target_package_numpy} from multiple file test -----')
        rtn = dynamic_pip.install_single_package(target_package_list)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # check package list
        print(f'----- list {target_package_numpy} from multiple file test -----')
        rtn = DynamicPip.list_package()
        print(f'return result {rtn}\n')
        self.assertTrue('2.31.0' == rtn.get('requests'))
        self.assertTrue('2.2.1' == rtn.get('pandas'))

        # uninstall package
        print(f'----- uninstall {target_package_numpy} from multiple file test -----')
        rtn = DynamicPip.remove_single_package(target_package_list)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        del dynamic_pip


if __name__ == '__main__':
    unittest.main()
