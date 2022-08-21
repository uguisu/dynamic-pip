# coding=utf-8
# author xin.he

from dynamicPip import DynamicPip

# declare target package
target_package = 'numpy==1.21.6'

# install single package
print(f'----- install {target_package} test -----')
rtn = DynamicPip.install_single_package(target_package)
print(f'return result code {rtn}\n')

# check package list
print(f'----- list {target_package} test -----')
rtn = DynamicPip.list_package()
print(f'return result {rtn}\n')

# uninstall single package
print(f'----- uninstall {target_package} test -----')
rtn = DynamicPip.remove_single_package(target_package)
print(f'return result code {rtn}\n')
