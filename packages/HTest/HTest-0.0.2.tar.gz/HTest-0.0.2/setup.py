#!/usr/bin/env python3.7
# _*_ coding:utf-8 _*_

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='HTest',
    version='0.0.2',
    url='https://https://github.com/Tao99/ui-autotest/HTest',
    license='BSD',
    author='Tao lei',
    author_email='1285642171@qq.com',
    description='Automated testing framework based on unittest.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'ddt==1.4.2',
        'PyYAML==5.4.1',
        'openpyxl==3.0.9',
        'pytesseract==0.3.8',
        'Pillow==5.4.1',
        'PyAutoGUI==0.9.53',
        'opencv-python==4.5.4.58',
        'numpy==1.21.3',
        'Faker==9.8.2',
        'setuptools==40.8.0'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        "Topic :: Software Development :: Testing",
    ],
    entry_points={
        'console_scripts': [
            'hs=HTest.cli:main_HTest',
            'HTest=HTest.cli:main_HTest',
            'htest=HTest.cli:main_HTest'
        ]
    }

)
