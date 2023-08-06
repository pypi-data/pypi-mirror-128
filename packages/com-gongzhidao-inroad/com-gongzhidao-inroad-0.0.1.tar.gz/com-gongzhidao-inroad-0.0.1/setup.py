from setuptools import setup

setup(name='com-gongzhidao-inroad',             # 这个是显示在PYPI中的名称，使用pip安装时也是这个名称
      version='0.0.1',                          # 版本号，做pip install --upgrade的时候有用
      description='工智道公共方法',                # 描述
      packages= ['inroad'],
      # # 以下均为可选参数
      # long_description="",# 长描述
      # url='https://github.com/pypa/sampleproject', # 主页链接
      # author='The Python Packaging Authority', # 作者名
      # author_email='pypa-dev@googlegroups.com', # 作者邮箱
      # classifiers=[
      #       'Development Status :: 3 - Alpha',  # 当前开发进度等级（测试版，正式版等）
      #
      #       'Intended Audience :: Developers', # 模块适用人群
      #       'Topic :: Software Development :: Build Tools', # 给模块加话题标签
      #
      #       'License :: OSI Approved :: MIT License', # 模块的license
      #
      #       'Programming Language :: Python :: 2', # 模块支持的Python版本
      #       'Programming Language :: Python :: 2.7',
      #       'Programming Language :: Python :: 3',
      #       'Programming Language :: Python :: 3.4',
      #       'Programming Language :: Python :: 3.5',
      #       'Programming Language :: Python :: 3.6',
      # ],
      # keywords='sample setuptools development',  # 模块的关键词，使用空格分割
      # install_requires=['peppercorn'], # 依赖模块
      # extras_require={  # 分组依赖模块，可使用pip install sampleproject[dev] 安装分组内的依赖
      #       'dev': ['check-manifest'],
      #       'test': ['coverage'],
      # },
      # package_data={  # 模块所需的额外文件
      #       'sample': ['package_data.dat'],
      # },
      # data_files=[('my_data', ['data/data_file'])], # 类似package_data, 但指定不在当前包目录下的文件
      # entry_points={  # 新建终端命令并链接到模块函数
      #       'console_scripts': [
      #             'sample=sample:main',
      #       ],
      # },
      # project_urls={  # 项目相关的额外链接
      #       'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
      #       'Funding': 'https://donate.pypi.org',
      #       'Say Thanks!': 'http://saythanks.io/to/example',
      #       'Source': 'https://github.com/pypa/sampleproject/',
      # },
      )
