# coding=utf-8
# author xin.he

class StaticResources:
    """
    static resources
    """

    # default PyPI mirror
    DEFAULT_PYPI_HOST: str = 'https://pypi.org/simple'

    DEFAULT_REQUIREMENT_FILE: str = 'requirements.txt'

    DEFAULT_RELATIONSHIP_MAP_TEMPLATE: str = '''
    %%{{ init: {{ 'flowchart': {{ 'curve': 'monotoneX' }} }} }}%%
    graph LR
    MyProject([MyProject]):::header
    %% ---- BODY
    {body}
    %% ---- LINK
    {links}
    %% ---- STYLE
    classDef header fill:#FFCC99;
    classDef mynode text-align:left;
    '''

    SUCCESS_EXIT: int = 0
