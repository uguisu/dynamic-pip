# 镜像服务

## 镜像服务器列表
`PyPI`默认的仓库地址:`https://pypi.org/simple`可能会因为各种原因，导致速度不佳。因此通过镜像服务器安装`package`是一个很好的解决方案。

`dynamic-Pip`通过`StaticResources.DEFAULT_PYPI_HOST`属性，内置了`PyPI`默认的仓库，同时也支持自定义的镜像服务器列表功能。

当工程师设置了一个镜像服务器列表时，`dynamic-Pip`会自动根据网络链接的速度，选择一个最快的站点进行连接。

下面，以`mirrors.aliyun.com`提供的镜像服务为例
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

注意：
- 使用镜像列表的时候，系统级别的镜像服务器设置(如`～/.pip/pip.conf`)将会被忽略
- `set_mirror_list()`方法一定要在安装方法之前被调用才会生效

## 额外索引支持(extra-index-url)

某些特殊的`package`需要从其提供商所建立的网站上进行下载和安装。这就是用到了`额外索引(extra-index)`的概念。`dynamic-Pip`同样支持这种安装方式。

下面以`pytorch`为例:
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

注意：
- 使用`额外索引`时，`镜像服务器列表`功能是可选的，二者没有相互依赖关系
