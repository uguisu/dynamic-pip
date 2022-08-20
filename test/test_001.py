# coding=utf-8
# author xin.he

from dynamicPip import DynamicPip


# install single package
# rtn = PIP.install_single_package('numpy==1.21.6')
# rtn = DynamicPip.install_single_package('numpy==1.21.6', '--force-reinstall')
rtn = DynamicPip.install_single_package('numpy==1.21.6')
print(rtn)

# rtn = PIP.list_packages()
# print(rtn)

rtn = DynamicPip.list_package()
print(rtn)
