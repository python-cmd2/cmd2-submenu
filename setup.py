#
# coding=utf-8

import os
import setuptools

#
# get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='cmd2-submenu',
    use_scm_version=True,
    description='A nested submenu system for cmd2',
    long_description=long_description,
    keywords='cmd2 plugin submenu',

    author='python-cmd2',
    author_email='',
    url='https://github.com/python-cmd2/cmd2-submenu',
    license='MIT',

    packages=['cmd2_submenu'],

    python_requires='>=3.4',
    install_requires=['cmd2 >= 0.9.6, <=2'],
    setup_requires=['setuptools_scm'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    # dependencies for development and testing
    # $ pip install -e .[dev]
    extras_require={
        'dev': ['setuptools_scm', 'pytest', 'invoke']
    },
)
