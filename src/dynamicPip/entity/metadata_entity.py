# coding=utf-8
# author xin.he


class MetaDataEntity:
    """
    METADATA info Entity

    follow attributes will be fetched:
    - package name
    - version
    - summary
    - license
    - requires-dist (as list, no duplication)
    """

    def __init__(self):
        """
        init
        """
        self._name = None
        self._version = None
        self._summary = None
        self._license = None
        self._requires_dist = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, summary):
        self._summary = summary

    @property
    def license(self):
        return self._license

    @license.setter
    def license(self, license):
        self._license = license

    @property
    def requires_dist(self):
        return self._requires_dist

    @requires_dist.setter
    def requires_dist(self, requires_dist):
        self._requires_dist = requires_dist

    def __str__(self):
        # self._name = None
        # self._version = None
        # self._summary = None
        # self._license = None
        # self._requires_dist = None
        return f'''
            {{
                name: {self._name},
                version: {self._version},
                summary: {self._summary},
                license: {self._license},
                requires_dist: {self._requires_dist}
            }}
        '''

    def __eq__(self, other):
        """
        equal
        :param other: other object
        :return: is equal
        """
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __hash__(self):
        """
        hash
        :return: hash code
        """
        return hash(self.__str__())