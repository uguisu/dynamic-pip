# Runtime management `package`

## Get installed package list
Get all installed `package`'s name and version as `dict` type at runtime.
```python
from dynamicPip import DynamicPip

rtn = DynamicPip.list_package()
print(f'return result {rtn}\n')
```

## Add package
Dynamically install target `package` by it's name and version number at runtime.
```python
from dynamicPip import DynamicPip

# declare
target_package = 'numpy==1.21.6'
dynamic_pip = DynamicPip()

# install
print(f'----- install {target_package} test -----')
rtn = dynamic_pip.install_package(target_package)
print(f'return result code {rtn}\n')
self.assertTrue(0 == rtn)
```

## Batch add package
Tie up all required packages into a `list` object, `dynamic-Pip` will commit a batch install automatically, if you want to install more packages.
```python
from dynamicPip import DynamicPip

# declare
target_package = 'numpy==1.21.6'
target_package_list = [
    target_package,
    'scikit-learn==1.0.2'
]
dynamic_pip = DynamicPip()

# install
print(f'----- install {target_package_list} test -----')
rtn = dynamic_pip.install_package(target_package_list)
print(f'return result code {rtn}\n')
self.assertTrue(0 == rtn)
```

## Add from install file
For some scenarios that are restricted, cannot access public networks, or even do not have network connection, `dynamic-Pip` can install `package` from user-specified static files (eg: `whl` files, private `http` servers). The step is the same as the previous introduction. `dynamic-Pip` even supports the mixed use of local files and `PyPI` images

```python
from dynamicPip import DynamicPip

# declare target package
importlib_metadata_package = 'importlib_metadata-7.0.2-py3-none-any.whl'
importlib_metadata_package_url = ('https://mirrors.aliyun.com/pypi/packages/db/62/'
                                  '6879ab53ad4997b627fc67241a41eabf7163299c59580c6ca4aa5ae6b677/'
                                  'importlib_metadata-7.0.2-py3-none-any.whl#'
                                  'sha256=f4bc4c0c070c490abf4ce96d715f68e95923320370efb66143df00199bb6c100')
target_package_importlib_metadata = 'importlib-metadata==7.0.2'

requests_package = 'requests-2.31.0-py3-none-any.whl'
requests_package_url = ('https://mirrors.aliyun.com/pypi/packages/70/8e/'
                        '0e2d847013cb52cd35b38c009bb167a1a26b2ce6cd6965bf26b47bc0bf44/'
                        'requests-2.31.0-py3-none-any.whl')
target_package_requests = 'requests==2.31.0'

target_package_list = [
    importlib_metadata_package,
    requests_package,
]

dynamic_pip = DynamicPip()

# install
print(f'----- install {target_package_list} test -----')
rtn = dynamic_pip.install_package(target_package_list)
print(f'return result code {rtn}\n')
self.assertTrue(0 == rtn)

# check package list
print(f'----- list { ",".join(target_package_list) } from multiple file test -----')
rtn = DynamicPip.list_package()
print(f'return result {rtn}\n')
self.assertTrue('2.31.0' == rtn.get('requests'))
self.assertTrue('7.0.2' == rtn.get('importlib_metadata'))

# uninstall package
print(f'----- uninstall { ",".join(target_package_list) } from multiple file test -----')
rtn = DynamicPip.remove_package(target_package_list)
print(f'return result code {rtn}\n')
self.assertTrue(0 == rtn)

del dynamic_pip
```

## Gentle addition
Sometimes, engineers may not be sure whether all dependent packages have been installed in the running environment. In order to take into account performance, `dynamic-Pip` recommends using the more gentle `make_sure_packages()` method instead of the `install_package()` method.

`make_sure_packages()` method will:
- Check whether the `package` and `version` in the target installation list meet the requirements
- Only install (or overwrite) `packages` that do not meet the requirements

## Remove
Dynamically remove target `package` by it's name and version number at runtime.
```python
from dynamicPip import DynamicPip

# declare
target_package = 'numpy==1.21.6'
dynamic_pip = DynamicPip()

# uninstall single package
print(f'----- uninstall {target_package} test -----')
rtn = DynamicPip.remove_package(target_package)
print(f'return result code {rtn}\n')
self.assertTrue(0 == rtn)
```

## Batch remove
Tie up all packages which will be removed into a `list` object, `dynamic-Pip` will commit a batch remove automatically, if you want to delete more packages.
```python
from dynamicPip import DynamicPip

# declare
target_package = 'numpy==1.21.6'
target_package_list = [
    target_package,
    'scikit-learn==1.0.2'
]
dynamic_pip = DynamicPip()

# uninstall single package
print(f'----- uninstall {target_package_list} test -----')
rtn = DynamicPip.remove_package(target_package_list)
print(f'return result code {rtn}\n')
self.assertTrue(0 == rtn)
```

## Case study
Dynamically managing `package` versions may play a key role when dealing with some special-case tasks.
Consider the following situation:
- `Project A` depends on `Package B`. Due to the upgrade of `Package B`, some functions in the old version have been deleted.
- `Project A` needs to call some methods in the old version of `Package B`, and also needs to use other methods in the latest version.
- In this case, you can use `dynamic-Pip` to replace the version of `Package B` during runtime.
