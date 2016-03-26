'''
    setupext.py: A python module with utility functions to ease creation
    of python setup (installation) scripts

    Copyright (C) 2016 Sundar Nagarajan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    For details of the GNU General Pulic License version 3, see the
    LICENSE.txt file that accompanied this program
'''
import sys
import os
from setuptools import setup, find_packages, Extension
# import setupext ONLY if you need triggers for installation steps
import setupext


'''
This will not _JUST_ work for your package - it is provided as a TEMPLATE
to create a setup.py file that uses setupext

See Readme.txt for more details
'''

os.chdir(os.path.dirname(sys.argv[0]) or ".")

# See README.txt for detailed help on different sections
'''
==============================================================================
PACKAGE DATA
==============================================================================
'''
# You _SHOULD_ set these
name = 'dummy_package'
version = '0.1'
description = name
install_requires = [
    'cffi>=1.0.0',
    'six>=1.9.0'
]
packages = find_packages()
license = 'License :: OSI Approved :: MIT License'

# The following are optional
url = ''
download_url = ''
author = 'Sundar Nagarajan'
# author_email = ''
maintainer = author
# maintainer_email = author_email
classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: Implementation :: PyPy',
    'License :: OSI Approved :: MIT License',
]
zip_safe = True


'''
==============================================================================
C EXTENSION DETAILS

Put the C files in a dir under name so that the C files can also be
installed using data_dirs (see ADDITIONAL DATA FILES)
==============================================================================
'''
c_dir = 'c_files'
libname = 'libdummy'
c_src_files = [
    'dummy.c',
]
libpath = os.path.join(name, libname)
c_src_list = [os.path.join(name, c_dir, x) for x in c_src_files]
ext_modules = [
    Extension(
        name=libpath,
        sources=c_src_list,
        include_dirs=[c_dir],
    )
]


'''
==============================================================================
ADDITIONAL DATA FILES
---------------------

- set data_dirs to LIST of directories under name that
    you want to include

see README.txt for more details
==============================================================================
'''

data_dirs = [
    'doc',
    'c_files'
]


'''
==============================================================================
CUSTOM STEPS

see README.txt for more details
==============================================================================
'''


'''
==============================================================================
ADDITIONAL keyword args to setup() - shouldn't be required, normally
==============================================================================
'''
ADDL_KWARGS = dict(
    # To support custom step triggers
    cmdclass=setupext.get_cmdclass()
)


'''
==============================================================================
           DO NOT CHANGE ANYTHING BELOW THIS
==============================================================================
'''


def get_longdesc(default=''):
    '''
    Returns-->str
    '''
    files = ['README.rst', 'README.md', 'README.txt', 'README']
    for f in files:
        try:
            return open(f, 'r').read()
        except:
            continue
    return default


def get_dirtree(topdir, dirlist=[]):
    '''
    topdir-->str: must be name of a dir under current working dir
    dirlist-->list of str: must all be names of dirs under topdir
    '''
    ret = []
    curdir = os.getcwd()
    if not os.path.isdir(topdir):
        return ret
    os.chdir(topdir)
    try:
        for dirname in dirlist:
            if not os.path.isdir(dirname):
                continue
            for (d, ds, fs) in os.walk(dirname):
                for f in fs:
                    ret += [os.path.join(d, f)]
        return ret
    except:
        return ret
    finally:
        os.chdir(curdir)

# Make some keywords MANDATORY
for k in [
    'name', 'version', 'description', 'license',
]:
    if k not in locals():
        raise Exception('Missing mandatory keyword: ' + k)

# keywords that are computed from variables
dirlist = locals().get('data_dirs', None)
if isinstance(dirlist, list):
    package_dir = {name: name}
    package_data = {name: get_dirtree(topdir=name, dirlist=dirlist)}

long_description = get_longdesc(description)

known_keywords = [
    'name', 'version', 'packages', 'description', 'license',
    'install_requires', 'requires', 'setup_requires',
    'ext_modules', 'package_dir', 'package_data',
    'zip_safe', 'classifiers', 'keywords',
    'long_description', 'url', 'download_url',
    'author', 'author_email', 'maintainer', 'maintainer_email',
]

kwdict = {}
for k in known_keywords:
    if k in locals():
        kwdict[k] = locals()[k]

# Additional keywords specified by user - shouldn't be required, normally
kwdict.update(ADDL_KWARGS)


setup(**kwdict)
