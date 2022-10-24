# coding=utf-8
# author xin.he
import re


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
        self._requires_dist = {}

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
    def license(self, licenses):
        self._license = licenses

    @property
    def requires_dist(self):
        return self._requires_dist

    @requires_dist.setter
    def requires_dist(self, requires_dist):
        self._requires_dist = requires_dist

    def __str__(self):
        return f'''
        {{
            name: {self._name},
            version: {self._version},
            summary: {self._summary},
            license: {self._license},
            requires_dist: {'; '.join(self._requires_dist.keys())}
        }}
        '''

    def format_to_markdown(self):
        """
        format values as markdown doc

        refer doc: https://mermaid-js.github.io/mermaid/#/
        """

        def _generate_dependence_list():
            """
            generate child list and info separator( [] - for no child, {{}} - hexagon node for list)
            """

            child_list = []
            for _c in self._requires_dist:
                child_list.append(f'+{_c}')

            child_str = '<br>'.join(child_list)

            if 0 == len(child_str):
                # no child
                l_separator = '['
                r_separator = ']'
            else:
                l_separator = '{{'
                r_separator = '}}'

            return child_str, l_separator, r_separator

        c_str, l_s, r_s = _generate_dependence_list()

        return f'''
        {self._name}{l_s}name: {self._name}<br/>version: {self._version}<br/>summary: {self._summary}<br/>license: {self._license}<br/>{c_str}{r_s}:::mynode
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


class MetaDataFileReader:
    """
    METADATA file reader. super class
    """

    def __init__(self, cls_name: str):
        """
        init
        :param cls_name: instance's class name
        """
        self._class_name = cls_name

    def read(self, file: str) -> MetaDataEntity:
        """
        read METADATA file info into entity
        :param file: METADATA file name & path
        :return: MetaDataEntity entity
        """
        raise AttributeError('This method is not overridden')


class MetaDataFileReader37(MetaDataFileReader):
    """
    METADATA file reader. (for python version < 3.8)
    """

    def __init__(self):
        """
        init
        """
        super().__init__(self.__class__.__name__)

    def read(self, file: str) -> MetaDataEntity:
        """
        read METADATA file info into entity
        :param file: METADATA file name & path
        :return: MetaDataEntity entity
        """
        def _matcher(rule: str, target_text: str, grp=2):
            _match_obj = re.match(rule, target_text)
            if _match_obj is not None:
                return _match_obj.group(grp)
            else:
                return None

        # TODO debug
        # print(f'working with {self._class_name}')

        with open(file, mode='r', encoding='utf-8') as f:
            meta_lines = f.readlines()

        rtn = MetaDataEntity()

        for m_l in meta_lines:
            # Name
            _m = _matcher(r'^(Name:)(.*)', m_l)
            if _m is not None:
                rtn.name = _m.strip()

            # Version
            _m = _matcher(r'^(Version:)(.*)', m_l)
            if _m is not None:
                rtn.version = _m.strip()

            # Summary
            _m = _matcher(r'^(Summary:)(.*)', m_l)
            if _m is not None:
                rtn.summary = _m.strip()

            # License
            _m = _matcher(r'^(License:)(.*)', m_l)
            if _m is not None:
                rtn.license = _m.strip()

            # Requires-Dist
            # Example:
            # input:
            #   Requires-Dist: numpy (>=1.17.3) ; platform_machine != "aarch64" and platform_machine != "arm64" and python_version < "3.10"
            # match:
            #   [1]: Requires-Dist: numpy (>=1.17.3) ; platform_machine != "aarch64" and platform_machine != "arm64" and python_version < "3.10"
            # group:
            #   [1]: Requires-Dist:
            #   [2]:  numpy (>=1.17.3) ; platform_machine != "aarch64" and platform_machine != "arm64" and python_version < "3.10"
            # AVOID EXAMPLE:
            #     Requires-Dist: pytest (>=6.0) ; extra == 'test'
            _m = _matcher(r'^(Requires-Dist:)(?!.*extra)(.*)', m_l)
            if _m is not None:
                _m_pkg_name = _matcher(r'(^\S*)', _m.strip(), grp=1)
                if _m_pkg_name is not None:
                    rtn.requires_dist[_m_pkg_name.strip()] = _m_pkg_name.strip()

        return rtn


class MetaDataFileReader38(MetaDataFileReader):
    """
    METADATA file reader. (for python version >= 3.8)
    """

    def __init__(self):
        """
        init
        """
        super().__init__(self.__class__.__name__)

    def read(self, file: str) -> MetaDataEntity:
        """
        read METADATA file info into entity
        :param file: METADATA file name & path
        :return: MetaDataEntity entity
        """

        print(f'working with {self._class_name}')

        # TODO importlib.metadata is new function from python 3.8
        from importlib.metadata import version
        print(version('numpy'))

        return None
