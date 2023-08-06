import setuptools

with open('README.md','r',encoding='utf-8') as fh: # 读取 README.md
    long_description = fh.read()

setuptools.setup(
    name = 'zb_test_pkg', # 当前包的名字
    version = '0.1.0',  # 当前版本号
    author = 'Bo Zhang', # 作者
    author_email = 'tianniaozbl@163.com', # 作者邮箱
    description = 'An example for teaching how to publish a Python package',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/pypa/sampleproject',
    packages = setuptools.find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ]

    # classifiers = [
    #     'Programming Language :: Python :: 3',
    #     'License :: OSI Approved :: MITL license',
    #     'Operating System :: OS Independent'
    # ]
)