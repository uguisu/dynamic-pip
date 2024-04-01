# Mirror service

## Mirror service list
The default warehouse address of `PyPI`: `https://pypi.org/simple` may cause poor speed due to various reasons. Therefore installing the `package` through a mirror server is a good solution.

`dynamic-Pip` has a built-in `PyPI` default warehouse through the `StaticResources.DEFAULT_PYPI_HOST` property, and also supports a custom mirror server list function.

`dynamic-Pip` will automatically select the fastest site to connect according to the speed of the network link when engineers set up a list of mirror servers.

Here, take the mirroring service provided by `mirrors.aliyun.com` as an example
```python
from dynamicPip import DynamicPip, StaticResources

# declare
target_package = 'numpy==1.21.6'

dynamic_pip = DynamicPip()

dynamic_pip.set_mirror_list([
    StaticResources.DEFAULT_PYPI_HOST,
    'https://mirrors.aliyun.com/pypi/simple',
])

# install
print(f'----- install {target_package} test -----')
rtn = dynamic_pip.install_package(target_package)
print(f'return result code {rtn}\n')
self.assertTrue(0 == rtn)
```

Notice：
- When using a mirror list, system-level mirror server settings (such as `~/.pip/pip.conf`) will be ignored
- The `set_mirror_list()` method must be called before the installation method.

## Eextra index url

Some special packages need to be downloaded and installed from the website established by their provider. This is where the concept of `extra-index' is used. `dynamic-Pip` also supports this installation method.

Take `pytorch` as an example:
```python
extra_index_url = 'https://download.pytorch.org/whl/cpu'
target_package = 'torch==1.13.0'

from dynamicPip import DynamicPip

dynamic_pip = DynamicPip()
# setup extra index here
dynamic_pip.extra_index_url = extra_index_url
# optional
dynamic_pip.set_mirror_list(proxy_list)

# install
print(f'----- install {target_package} test -----')
rtn = dynamic_pip.install_package(target_package)
print(f'return result code {rtn}\n')
self.assertTrue(0 == rtn)

# check package list
print(f'----- list {target_package} test -----')
rtn = DynamicPip.list_package()
print(f'return result {rtn}\n')
self.assertTrue('1.13.0+cpu' == rtn.get('torch'))

# uninstall single package
print(f'----- uninstall {target_package} test -----')
rtn = DynamicPip.remove_package(target_package)
print(f'return result code {rtn}\n')
self.assertTrue(0 == rtn)

del dynamic_pip
```

Notice：
- When using `extra index url`, the `mirror server list` function is optional and there is no interdependence between them.
