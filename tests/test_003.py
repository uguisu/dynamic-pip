# coding=utf-8
# author xin.he

import os
import unittest

from dynamicPip import DynamicPip

# declare target package
target_package = 'numpy==1.21.6'
target_package_list = [
    target_package,
    'scikit-learn==1.0.2'
]
target_requirements_file_name = './test_req.txt'


class Test003(unittest.TestCase):

    def test_export_requirements_file_001(self):
        """
        export requirements file
        """

        dynamic_pip = DynamicPip()

        dynamic_pip.export_requirements_file(target_requirements_file_name)

        _confirm_file = os.path.join('.', target_requirements_file_name)

        self.assertTrue(os.path.exists(_confirm_file))

        # remove useless file
        os.remove(_confirm_file)

        del dynamic_pip


if __name__ == '__main__':
    unittest.main()
