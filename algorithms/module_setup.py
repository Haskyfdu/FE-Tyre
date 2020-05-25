#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import copy
import sys
import glob

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize


COMPILE_LIST = [
    'src/*.py',
    'src/basic/*.py',
    'src/core/*.py',
    'src/core/FE_TSP/*.py',
    'src/core/FE_Pick_Storage/*.py',
    '!src/__init__.py',
    '!src/basic/__init__.py',
    '!src/core/__init__.py'
]


class Compile(object):
    #
    @staticmethod
    def file_compile():
        inclusion_list, exclusion_list = [], []
        for file in COMPILE_LIST:
            realpath = os.path.join(os.path.realpath('./'), file)
            if '!' not in file:
                inclusion_list += glob.glob(realpath, recursive=False)
            else:
                exclusion_list += glob.glob(realpath.replace('!', ''), recursive=False)
        compile_file_list = list(set(inclusion_list) - set(exclusion_list))

        c_extension_list = cythonize(compile_file_list, language_level=3)
        sys.argv[1] = 'build_ext'
        setup(
            ext_modules=c_extension_list,
            cmdclass={'build_ext': build_ext},
        )

        os.system('cp -rfv ./build/lib*/* ../../')

    #
    @classmethod
    def run(cls):
        assert len(sys.argv) == 2, '\nUsage: python module_setup.py [option: install | clean | clear]'
        flag = copy.deepcopy(sys.argv[1])
        if flag == 'install':
            os.system(
                'rm -rfv ./lib/* && touch ./lib/__init__.py && find ./src -name "*.c" -o -name "*.so" | xargs rm -rfv')
            cls.file_compile()
            os.system('cp -rfv ./src/* ./lib/')
            os.system('find ./src -name "*.c" -o -name "*.so" | xargs rm -rfv')
            os.system('find ./lib -name "*.c" -o -name "*.py" | grep -v __init__.py | xargs rm -rfv')
        elif flag == 'clean':
            os.system(
                'rm -rfv ./lib/* && touch ./lib/__init__.py && find ./src -name "*.c" -o -name "*.so" | xargs rm -rfv')
        elif flag == 'clear':
            yes_no = input(
                '\033[1;31mThis command is DANGEROUS! All your source codes will be removed. [Yes(Y) | No(N)]: \033[0m')
            os.system('rm -rfv ../.git ./src/* && touch ./src/__init__.py') \
                if yes_no in ['y', 'Y', 'yes', 'Yes', 'YES'] else None
        else:
            assert 0, '\nUsage: python module_setup.py [option: install | clean | clear]'
        os.system('rm -rfv ./build ./__pycache__ ./dist ./UNKNOWN.egg-info && echo Operation Complete!"\n"')


if __name__ == '__main__':
    Compile.run()
