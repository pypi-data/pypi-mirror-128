from distutils.core import setup
from setuptools import find_packages

setup(name='dtanys',  # 包名
      version='1.0.7',  # 版本号
      description='A python dictionary parser',
      long_description='https://github.com/luxuncang/dtanys',
      author='ShengXin Lu',
      author_email='luxuncang@qq.com',
      url='https://github.com/luxuncang/dtanys',
      install_requires=[],
      license='MIT',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development :: Libraries'
      ],
      )