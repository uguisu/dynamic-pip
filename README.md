# Dynamic Pip

![logo](assets/logo.jpg)

_Photo by David Dibert: https://www.pexels.com/photo/green-and-gray-evergreen-cargo-ship-1117210/_

Help users to dynamically manage python package resources and bid farewell to the constraints of the `requirements.txt` file.

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.7%2F3.8%2F3.9%2F3.10-blue" alt="valid for python3.7/3.8/3.9" />
    <img src="https://img.shields.io/badge/Apache-2.0-blue" alt="license" />
</p>


## Build-in `pip`

Refer: https://pip.pypa.io/en/stable/cli/pip_install/

## Dynamic-Pip

Through `DynamicPip` class object, dynamically manage (install, delete, etc.) python packages during the execution of the program. In addition, compared to build-in `pip`, `dynamic-pip` also supports some extended functions.

Example: Install the `numpy` package at runtime

```py
from dynamicPip import DynamicPip

dynamic_pip = DynamicPip()

# declare target package
target_package = 'numpy==1.21.6'

# install
print(f'----- install {target_package} test -----')
rtn = dynamic_pip.install_package(target_package)
print(f'return result code {rtn}\n')

# check package list
print(f'----- list {target_package} test -----')
rtn = DynamicPip.list_package()
print(f'return result {rtn}\n')

# uninstall single package
print(f'----- uninstall {target_package} test -----')
rtn = DynamicPip.remove_package(target_package)
print(f'return result code {rtn}\n')

del dynamic_pip
```

Example: Build a requirement map
```python
from dynamicPip import DynamicPip

dynamic_pip = DynamicPip()

dynamic_pip.generate_requires_map()
```

Example: List all installed packages. (`pip list`)
```python
# check package as dict. (key = package name, value = version )
rtn = dynamic_pip.list_package()
print(f'return result {rtn}\n')
```

Example: Generate a requirement map
```python
dynamic_pip.generate_requires_map(target_output_requirements__map_file_name)
```

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

## Features :point_left:
- [x] support install / uninstall specific package(s) at runtime
- [x] install / uninstall from the given requirements file
- [x] support python test unit
- [x] support multiple index-url, auto-detect fastest PyPI mirror
- [x] support extra-index-url
- [x] export requirements file
- [x] build requires map
- [x] install from local file
- [x] find package exist

## Limitations :construction:
- [ ] official `inspect` function is still in the experimental stage.
- [ ] official `--dry-run` function is still in the experimental stage.
- [ ] official `--report` function is still in the experimental stage.

## Future version
- [ ] generate a report about all installed packages
- [ ] verify hash
- [ ] dynamic `import`
