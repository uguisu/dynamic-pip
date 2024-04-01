# Classic requirements file

## `requirements.txt` file
`dynamic-Pip` supports file-defined installation lists. The traditional `requirements.txt` file can be written directly to the runtime.
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

## Case study
Sometimes, the program needs to make certain decisions based on the running status to install the corresponding `package`. At this time, R&D engineers can define a series of packages that meet different scenarios into different files, and install them when the program is running.

Consider the following situation:
- `Project A` is an artificial intelligence program. The scenarios it runs in are strongly dependent on hardware
  - Have `Nvidia GPU`
  - Only `Intel CPU`
  - Other accelerator
- If the running environment contains `Nvidia GPU`, engineers can define a `requirement-gpu.txt` file to include the `pytorch GPU` version
- If there is only `Intel CPU` in the running environment, engineers can define a `requirement-cpu.txt` file to include the `pytorch CPU` version and `OpenVINO`
- If detect other accelerator, engineers can purposefully define the corresponding installation list file.
