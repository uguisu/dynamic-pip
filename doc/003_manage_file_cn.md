# 支持文件列表

## `requirements.txt`文件
`dynamic-Pip`支持文件定义的安装列表。传统的`requirements.txt`文件可直接写到运行时中。
```python
from dynamicPip import DynamicPip

# declare
target_requirements_file_name = './requirements.txt'
dynamic_pip = DynamicPip()

# install
print(f'----- install from requirements file test -----')
rtn = dynamic_pip.install_from_requirements_file(target_requirements_file_name)
print(f'return result code {rtn}\n')
self.assertTrue(0 == rtn)
```

## 案例研究
有地时候，程序需要根据运行状态做出某些决策，从而安装相对应的`package`。这时候，研发工程师就可以把满足不同场景的一系列`package`定义成不同的文件，在程序运行时安装，方便管理。

考虑下面的情况：
- `Project A`是一个人工智能的程序。其运行的场景对硬件有强烈依赖
  - 拥有`Nvidia GPU`
  - 仅`Intel CPU`
  - 其他硬件
- 如果运行环境中包含`Nvidia GPU`, 则工程师可以定义一个`requirement-gpu.txt`的文件，将`pytorch GPU`版本包含其中
- 如果运行环境中仅有`Intel CPU`，则工程师可以定义一个`requirement-cpu.txt`的文件，将`pytorch CPU`版本以及`OpenVINO`包含其中
- 如果运行环境中包含其他硬件，则工程师可以有目的的定义相应的安装列表文件
