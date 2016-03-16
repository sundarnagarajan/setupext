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
toplevel = 'dummy_package'
version = '0.1'
description = toplevel
install_requires = [
    'cffi>=1.0.0',
    'six>=1.9.0'
]
packages = find_packages()
license = 'License :: OSI Approved :: MIT License'

# The following are optional
long_description = open('README.rst').read()
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

Put the C files in a dir under toplevel so that the C files can also be
installed using data_dirs (see ADDITIONAL DATA FILES)
==============================================================================
'''
c_dir = 'c_files'
libname = 'libdummy'
c_src_files = [
    'dummy.c',
]
libpath = os.path.join(toplevel, libname)
c_src_list = [os.path.join(toplevel, c_dir, x) for x in c_src_files]
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

- set data_dirs to LIST of directories under toplevel that
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
ADDITIONAL keyword args to setup()
==============================================================================
'''
ADDL_KWARGS = dict(
)


'''
==============================================================================
           DO NOT CHANGE ANYTHING BELOW THIS
==============================================================================
'''

# Required keywords
kwdict = dict(
    name=toplevel,
    version=version,
    install_requires=install_requires,
    packages=packages,
    description=description,
    license=license,
)

# Optional keywords
kwdict.update(dict(
    long_description=globals().get('long_description', ''),
    url=globals().get('url', ''),
    download_url=globals().get('download_url', ''),
    author=globals().get('author', ''),
    author_email=globals().get('author_email', ''),
    maintainer=globals().get('maintainer', ''),
    maintainer_email=globals().get('maintainer_email', ''),
    classifiers=globals().get('classifiers', []),
    keywords=globals().get('keywords', []),
    zip_safe=globals().get('zip_safe', False),
))
kwdict.update(globals().get('ADDL_KWARGS', {}))

# To support custom step triggers
kwdict['cmdclass'] = setupext.get_cmdclass()

# More optional keywords, but which are added conditionally
ext_modules = globals().get('ext_modules', [])
if ext_modules:
    kwdict['ext_modules'] = ext_modules

dirlist = globals().get('data_dirs', None)
if isinstance(dirlist, list):
    kwdict['package_dir'] = {toplevel: toplevel}
    kwdict['package_data'] = {toplevel:
                              setupext.get_dirtree(toplevel, dirlist)}


setup(**kwdict)
