# Dependency tree

Dependencies between `packages` are a challenge in `python`. `dynamic-Pip` can automatically mine the interdependencies between `packages` and visualize them in a `tree` way.

The following example will generate a `Markdown` file named `test_req_map.md`, which contains the dependencies of all installed `packages`.
```python
target_requirements_file_name = './test_req.txt'
target_requirements__map_file_name = './test_req_map.md'

from dynamicPip import DynamicPip

dynamic_pip = DynamicPip()

# install
print(f'----- install from requirements file test -----')
rtn = dynamic_pip.install_from_requirements_file(target_requirements_file_name)
print(f'return result code {rtn}\n')
self.assertTrue(0 == rtn)

dynamic_pip.generate_requires_map(target_requirements__map_file_name)
```

The visualization of `test_req_map.md` is as follow
```mermaid
%%{ init: { 'flowchart': { 'curve': 'monotoneX' } } }%%
graph LR
MyProject([MyProject]):::header
%% ---- BODY
pkg_resources[name: pkg_resources<br/>version: 0.0.0<br/>summary: UNKNOWN<br/>license: UNKNOWN<br/>]:::mynode
joblib[name: joblib<br/>version: 1.1.0<br/>summary: Lightweight pipelining with Python functions<br/>license: BSD<br/>]:::mynode
threadpoolctl[name: threadpoolctl<br/>version: 3.1.0<br/>summary: threadpoolctl<br/>license: BSD-3-Clause<br/>]:::mynode
icmplib[name: icmplib<br/>version: 3.0.3<br/>summary: The power to forge ICMP packets and do ping and traceroute.<br/>license: GNU Lesser General Public License v3.0<br/>]:::mynode
python-dateutil{{name: python-dateutil<br/>version: 2.8.2<br/>summary: Extensions to the standard Python datetime module<br/>license: Dual License<br/>+six}}:::mynode
numpy[name: numpy<br/>version: 1.21.6<br/>summary: NumPy is the fundamental package for array computing with Python.<br/>license: BSD<br/>]:::mynode
pandas{{name: pandas<br/>version: 1.3.5<br/>summary: Powerful data structures for data analysis, time series, and statistics<br/>license: BSD-3-Clause<br/>+python-dateutil<br>+pytz<br>+numpy}}:::mynode
scipy{{name: scipy<br/>version: 1.7.3<br/>summary: SciPy: Scientific Library for Python<br/>license: BSD<br/>+numpy}}:::mynode
six[name: six<br/>version: 1.16.0<br/>summary: Python 2 and 3 compatibility utilities<br/>license: MIT<br/>]:::mynode
pytz[name: pytz<br/>version: 2022.2.1<br/>summary: World timezone definitions, modern and historical<br/>license: MIT<br/>]:::mynode
%% ---- LINK
MyProject --> pkg_resources
MyProject --> joblib
MyProject --> threadpoolctl
MyProject --> icmplib
MyProject --> python-dateutil
python-dateutil --> six
MyProject --> numpy
MyProject --> pandas
pandas --> python-dateutil
pandas --> pytz
pandas --> numpy
MyProject --> scipy
scipy --> numpy
MyProject --> six
MyProject --> pytz
%% ---- STYLE
classDef header fill:#FFCC99;
classDef mynode text-align:left;
```
Notice: The visualization function uses the `Mermaid` plug-in of `Markdown`. Please make sure your system supports [`Mermaid` :link: ](https://mermaid.js.org/intro/) when using it.
