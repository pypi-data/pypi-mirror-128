"""
des: 打包的用的setup必须引入
author: mr52hz
date: 2021-11-24
"""
from setuptools import setup, find_packages


VERSION = '0.0.1'

setup(name='vr.xy',
      version=VERSION,
      description="(x, y) for pr to make vr video based on Python3",
      long_description='just enjoy',
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python3 vr xy terminal',
      author='mr52hz',
      author_email='mr52hz@qq.com',
      url='https://gitee.com/Mr_52Hz/vxy.git',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[],
      entry_points={
        'console_scripts': [
            'vr = xy:v_h_xy'
        ]
      },
)