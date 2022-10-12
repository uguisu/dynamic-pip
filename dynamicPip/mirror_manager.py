# coding=utf-8
# author xin.he
import re

from icmplib import multiping

from dynamicPip import StaticResources


class MirrorManager:
    """
    manage usable PyPI mirrors to improve download speed
    """

    def __init__(self):
        """
        init
        """
        # declare a default mirror list
        self._mirror_list = [
            StaticResources.DEFAULT_PYPI_HOST,
        ]

    def connection_speed_check(self, time_out_second=4):
        """
        check connect speed
        :param time_out_second: time out in second, default is 4 second
        :return: speed_dic - each mirror is speed, stored as dist.<br />
                     key:str -> mirror name;<br />
                     val:float -> average response time<br />
                 fastest_host - the fastest host as list.
        """

        def _get_mirror_original_uri(mirror_dict: dict):
            """
            get mirror original URI
            """
            return list(mirror_dict.keys())

        # declare speed dict
        speed_dic = {}
        # declare the fasted host
        fastest_host = [None, time_out_second * 100]

        # clean mirror list to URI
        mirror_list_as_host = self._clean_mirror_uri(_get_mirror_original_uri, self._mirror_list)

        _hosts = multiping(mirror_list_as_host,
                           count=3,
                           interval=0.5,
                           timeout=time_out_second,
                           privileged=False)

        for i in range(len(_hosts)):
            if _hosts[i].is_alive:
                # add to dict
                speed_dic[self._mirror_list[i]] = _hosts[i].avg_rtt
                # check speed
                if _hosts[i].avg_rtt < fastest_host[1]:
                    # find faster mirror
                    fastest_host = [self._mirror_list[i], _hosts[i].avg_rtt]
            else:
                speed_dic[self._mirror_list[i]] = -1

        return speed_dic, fastest_host

    def get_best_mirror(self, time_out_second=4) -> str:
        """
        get the best mirror
        :param time_out_second: time out in second, default is 4 second
        :return: the fastest host name
        """
        _, fastest_host = self.connection_speed_check(time_out_second=time_out_second)
        return fastest_host[0]

    @property
    def mirror_list(self):
        """
        get mirror list
        """
        return self._mirror_list

    @mirror_list.setter
    def mirror_list(self, mirror_list: list):
        """
        set mirror list
        """

        def _is_valid_parameter(_m_list) -> bool:
            """
            verify mirror list is valid
            """
            return _m_list is not None\
                and isinstance(_m_list, list)\
                and 0 < len(_m_list)

        def _get_mirror_uri(mirror_dict: dict):
            # update mirror list
            self._mirror_list = list(mirror_dict.values())

        # verify
        if _is_valid_parameter(mirror_list):
            # append default PyPi mirror
            mirror_list.append(StaticResources.DEFAULT_PYPI_HOST)
            # update mirror list
            self._clean_mirror_uri(_get_mirror_uri, mirror_list)
        else:
            raise ValueError('Please setup a valid mirror list and try again.')

    @staticmethod
    def _clean_mirror_uri(fn, mirror_list=None):
        """
        clean mirror list URI to a hostname or IP.
        only the http/https mirror will be replaced into mirror list
        :param fn: function
        :param mirror_list: mirror list
        """

        # key: mirror name; val: original URI
        # example:
        #   'pypi.org' : 'https://pypi.org/simple'
        valid_mirror_dict = {}

        for i in range(len(mirror_list)):
            # to lower case
            _mr = mirror_list[i].lower()

            if _mr.startswith('http://') or _mr.startswith('https://'):
                # separate host name
                match_prefix = re.match(r'(^((http)s?://)[\w.-]+(/))', _mr)
                _mr = match_prefix.group(1).replace('http://', '').replace('https://', '').replace('/', '')

                # key: mirror name; val: original URI
                valid_mirror_dict[_mr] = mirror_list[i]

        assert 0 < len(valid_mirror_dict)

        return fn(valid_mirror_dict)
