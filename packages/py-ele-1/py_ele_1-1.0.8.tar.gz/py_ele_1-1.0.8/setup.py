# try:
#     from setuptools import setup
# except:
#     from distutils.core import setup
# -*- coding: utf-8 -*-

import setuptools

install_requires = [
    # 'numpy>=1.11.1',
    # 'pandas>=0.19.0'
    'requests'
]
platforms = ['linux/Windows']
# 模块相关的元数据
classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
setuptools.setup(
    name='py_ele_1',  # 对外我们模块的名字
    version='1.0.8',  # 版本号
    description='测试本地发布模块py_ele_1',  # 描述
    author='peter.peng',  # 作者
    author_email='peng.peter@qq.com',
    py_modules=['py_ele_1.Person'],  # 要发布的模块
    url="https://gitee.com/xx/xxx.git",
    license="MIT",
    platforms=platforms,
    classifiers=classifiers,
    include_package_data=True,
    install_requires=install_requires,
    packages=setuptools.find_packages()
)
