# 运行时安装`package`

## 获取列表
在程序运行期间，可获取当前运行时已经加载的所有`package`的列表和版本信息。所有信息以`dict`类型返回。
```python
from dynamicPip import DynamicPip

rtn = DynamicPip.list_package()
print(f'return result {rtn}\n')
```

## 添加
在程序运行期间，通过给定目标`package`名称和版本号的方式，完成动态添加
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

## 批量添加
如果需要安装的`package`比较多，则可以将所有的`package`写到一个`list`中，进行批量安装
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

## 从安装包添加
对于某些受到限制，不能访问公共网络，或者没有网络连接的场景，`dynamic-Pip`能够从用户指定的静态文件(如: `whl`文件, 私有`http`服务器)进行安装。使用方法与前面的介绍相同，`dynamic-Pip`甚至支持混合使用本地文件和`PyPI`镜像

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

## 温和的添加方式
有的时候，工程师可能不太确定运行环境中是否已经安装了全部依赖的`package`。为了兼顾性能，`dynamic-Pip`推荐使用更为温和的`make_sure_packages()`方法，代替`install_package()`方法。

`make_sure_packages()`方法将会:
- 检查目标安装清单中的`package`和`version`是否符合需要
- 仅安装(或覆盖)不符合要求的`package`

## 删除
在程序运行期间，通过给定目标`package`名称和版本号的方式，完成动态删除。
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

## 批量删除
如果需要删除的`package`比较多，则可以将所有的`package`写到一个`list`中，进行批量删除
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

## 案例研究
在处理一些特殊情况的任务时，动态管理`package`版本可能会起到关键作用。
考虑下面的情况：
- `Project A`依赖了某个`Package B`。由于`Package B`升级，造成了旧版本中的某些功能被删除。
- `Project A`即需要调用`Package B`旧版本中的某些方法，还需要使用最新版本的另一些方法。
- 这种情况下，就可以使用`dynamic-Pip`中途对`Package B`进行版本替换
