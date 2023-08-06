import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='liungfu',
    version='0.2.0',
    packages=find_packages(),
    include_package_data=True,
    description='permainan liungfu sederhana',
    long_description_content_type='text/markdown',
    long_description=README,
    author='Exso Kamabay',
    url='https://github.com/ExsoKamabay/ipwhois',
    license='Apache License 2.0',
    # install_requires=['requests'],
    keywords=['kamabay', 'liungfu', 'judi', 'permainan', 'game'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    entry_points={
        "console_scripts": [
            "liungfu = liungfu.server:main"
        ]
    }
)
