from setuptools import setup, find_packages

# 寻找唯一的项目名称，做为库及项目名
packages = find_packages()
if len(packages) != 1:
    print("项目根文件夹必需有且仅有一个，但当前项目根文件夹有", len(packages), "个")
    exit()
project_name = packages[0]

# 从requirements.txt读取所有依赖包并排除aiohttp,避免和插件平台冲突
requirements = open('requirements.txt').read().strip().split('\n')
requires = []
for pkg in requirements:
    if len(pkg) == 0:
        continue
    if not pkg.startswith('aiohttp'):
        # 移除掉本地地址
        _index = pkg.rfind("/")
        if _index == -1:
            requires.append(pkg)

# setup
setup(
    name=project_name,
    version='1.0.5',
    description='大众云学工具箱',
    author='Jem',
    author_email='tank94@163.com',
    url='',
    packages=packages,
    include_package_data=True,
    install_requires=requires
)
