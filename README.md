# Dynamic Pip

![logo](assets/logo.jpg)

_Photo by David Dibert: https://www.pexels.com/photo/green-and-gray-evergreen-cargo-ship-1117210/_

Help users to dynamically manage python package resources and bid farewell to the constraints of the `requirements.txt` file.

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
rtn = dynamic_pip.install_single_package(target_package)
print(f'return result code {rtn}\n')

# check package list
print(f'----- list {target_package} test -----')
rtn = DynamicPip.list_package()
print(f'return result {rtn}\n')

# uninstall single package
print(f'----- uninstall {target_package} test -----')
rtn = DynamicPip.remove_single_package(target_package)
print(f'return result code {rtn}\n')

del dynamic_pip
```

# Related package

`python-pip` 

## TODO
- [x] support uninstall target package
- [x] support python test unit
- [x] support multiple index-url
- [ ] install from the given requirements file
- [ ] export requirements file
- [ ] find package exist
- [ ] auto-detect packages with custom version from github
- [ ] build requires map
- [ ] generate a report about all installed packages
- [ ] verify hash
- [ ] install from local file
- [ ] install from compressed file
- [ ] install from FTP
- [ ] dynamic `import`