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
rtn = DynamicPip.install_single_package('numpy==1.21.6')
print(rtn)
```

# Related package

`python-pip` 

## TODO
- [x] support uninstall target package
- [ ] support multiple index-url
- [ ] install from the given requirements file
- [ ] export requirements file
- [ ] find package exist
- [ ] auto-detect packages with custom version from github
- [ ] build requires map
- [ ] generate a report about all installed packages
- [ ] verify hash
