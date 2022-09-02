# coding=utf-8
# author xin.he

import unittest

from dynamicPip import MirrorManager, StaticResources

proxy_list = [
    'pypi.org',
    'mirrors.aliyun.com',
    # TODO unknown host
    # 'unknown.host.com',
    'google.com',
]


class Test002(unittest.TestCase):

    def test_ping_all_mirror(self):
        """
        ping all mirrors in the list
        """

        mm = MirrorManager()
        mm.mirror_list = proxy_list

        speed_dic, fastest_host = mm.connection_speed_check()

        print(f'speed_dic:\n{speed_dic}')
        self.assertEqual(len(speed_dic), len(proxy_list))

        print(f'fastest_host:\n{fastest_host}')
        self.assertTrue(fastest_host[0] is not None)

        del mm

    def find_the_fastest_mirror_001(self):
        """
        only use default mirror
        """
        mm = MirrorManager()
        mirror_result = mm.get_best_mirror()
        self.assertEqual(StaticResources.DEFAULT_PYPI_HOST, mirror_result[0])

    def find_the_fastest_mirror_002(self):
        """
        use proxy_list
        """

        local_host = '127.0.0.1'

        mm = MirrorManager()
        mm.mirror_list = proxy_list.append(local_host)
        mirror_result = mm.get_best_mirror()
        self.assertEqual(local_host, mirror_result[0])


if __name__ == '__main__':
    unittest.main()