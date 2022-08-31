# coding=utf-8
# author xin.he
from icmplib import multiping


class MirrorManager:
    """
    manage usable PyPI mirrors to improve download speed
    """

    def __init__(self):
        """
        init
        """

        self._mirror_list = [
            'pypi.org',
        ]

    def connection_speed_check(self, time_out_second=4):
        """
        check connect speed
        """

        # declare speed dict
        speed_dic = {}
        # declare the fasted host
        fasted_host = [None, time_out_second * 100]

        _hosts = multiping(self._mirror_list,
                           count=3,
                           interval=0.5,
                           timeout=time_out_second,
                           privileged=False)

        for i in range(len(_hosts)):
            if _hosts[i].is_alive:
                # add to dict
                speed_dic[self._mirror_list[i]] = _hosts[i].avg_rtt
                # check speed
                if _hosts[i].avg_rtt < fasted_host[1]:
                    # find faster mirror
                    fasted_host = [self._mirror_list[i], _hosts[i].avg_rtt]
            else:
                speed_dic[self._mirror_list[i]] = -1

        return speed_dic, fasted_host

    def get_best_mirror(self, time_out_second=4) -> str:
        """
        get the best mirror
        """
        _, fasted_host = self.connection_speed_check(time_out_second=time_out_second)
        return fasted_host[0]

    @property
    def mirror_list(self):
        return self._mirror_list

    @mirror_list.setter
    def mirror_list(self, mirror_list: list):
        self._mirror_list = mirror_list
