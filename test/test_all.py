# coding=utf-8
# author xin.he

import unittest


if __name__ == '__main__':
    # declare test suite
    test_unit = unittest.defaultTestLoader.discover('.', 'test_*.py')

    test_executor = unittest.TextTestRunner()

    test_executor.run(test_unit)
