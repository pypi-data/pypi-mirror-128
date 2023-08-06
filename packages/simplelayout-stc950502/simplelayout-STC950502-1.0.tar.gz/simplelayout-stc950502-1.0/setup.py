
import setuptools

setuptools.setup(
      name='simplelayout-stc950502',  # 程序名称
      version='1.0',  # 程序版本号
      author='stc',  # 程序作者
      description='generator',  # 程序描述
      packages= setuptools.find_namespace_packages(),
      install_requires=[
      'simplelayout'],
      entry_points = {
        'console_scripts': [
            'simplelayout = src.simplelayout:main',
        ]}
      )
