# coding=utf-8
# author xin.he

import unittest

from dynamicPip import DynamicPip
from test_helper import download_file

# declare target package
importlib_metadata_package = 'importlib_metadata-7.0.2-py3-none-any.whl'
importlib_metadata_package_url = ('https://mirrors.aliyun.com/pypi/packages/db/62/'
                                  '6879ab53ad4997b627fc67241a41eabf7163299c59580c6ca4aa5ae6b677/'
                                  'importlib_metadata-7.0.2-py3-none-any.whl#'
                                  'sha256=f4bc4c0c070c490abf4ce96d715f68e95923320370efb66143df00199bb6c100')
target_package_importlib_metadata = 'importlib-metadata==7.0.2'

requests_package = 'requests-2.31.0-py3-none-any.whl'
requests_package_url = ('https://mirrors.aliyun.com/pypi/packages/70/8e/'
                        '0e2d847013cb52cd35b38c009bb167a1a26b2ce6cd6965bf26b47bc0bf44/'
                        'requests-2.31.0-py3-none-any.whl')
target_package_requests = 'requests==2.31.0'

target_package_list = [
    importlib_metadata_package,
    requests_package,
]


class Test005(unittest.TestCase):

    def test_install_single_package_from_file_001(self):
        """
        install single package from file
        - use default mirror
        """

        download_file(url=importlib_metadata_package_url, filename=importlib_metadata_package)

        dynamic_pip = DynamicPip()

        # install
        print(f'----- install {target_package_list} from file test -----')
        rtn = dynamic_pip.install_package(importlib_metadata_package)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # check package list
        print(f'----- list {importlib_metadata_package} test -----')
        rtn = DynamicPip.list_package()
        print(f'return result {rtn}\n')
        self.assertTrue('7.0.2' == rtn.get('importlib_metadata'))

        # uninstall single package
        print(f'----- uninstall {target_package_importlib_metadata} from file test -----')
        rtn = DynamicPip.remove_package(target_package_importlib_metadata)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        del dynamic_pip

    def test_install_multiple_packages_from_file_002(self):
        """
        install multiple packages from file
        - use default mirror
        """

        download_file(url=requests_package_url, filename=requests_package)
        download_file(url=importlib_metadata_package_url, filename=importlib_metadata_package)

        dynamic_pip = DynamicPip()

        # install
        print(f'----- install { ",".join(target_package_list) } from multiple file test -----')
        rtn = dynamic_pip.install_package(target_package_list)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        # check package list
        print(f'----- list { ",".join(target_package_list) } from multiple file test -----')
        rtn = DynamicPip.list_package()
        print(f'return result {rtn}\n')
        self.assertTrue('2.31.0' == rtn.get('requests'))
        self.assertTrue('7.0.2' == rtn.get('importlib_metadata'))

        # uninstall package
        print(f'----- uninstall { ",".join(target_package_list) } from multiple file test -----')
        rtn = DynamicPip.remove_package(target_package_list)
        print(f'return result code {rtn}\n')
        self.assertTrue(0 == rtn)

        del dynamic_pip


if __name__ == '__main__':
    unittest.main()
