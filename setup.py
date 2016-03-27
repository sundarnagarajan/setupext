import sys
import os
from setuptools import setup, find_packages, Extension
# Import setupext ONLY if you want custom triggers
# If you only use prep_cmd, you only need to include setupext in the package
# import setupext


os.chdir(os.path.dirname(sys.argv[0]) or ".")

'''
==============================================================================
PACKAGE DATA
==============================================================================
'''
# You _SHOULD_ set these
name = 'setupext'
version = '0.24.8'   # oldver: '0.24.7'
description = 'Utility classes and methods for using setuptools'
install_requires = [
]
packages = find_packages()
license = (
    'License :: OSI Approved :: '
    'GNU Lesser General Public License v3 or later (LGPLv3+)'
)

# The following are optional
url = 'https://github.com/sundarnagarajan/setupext'
download_url = 'https://github.com/sundarnagarajan/setupext.git'
author = 'Sundar Nagarajan'
author_email = 'sun.nagarajan@gmail.com'
maintainer = author
# maintainer_email = author_email
classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: Implementation :: PyPy',
    ('License :: OSI Approved :: '
     'GNU Lesser General Public License v3 or later (LGPLv3+)'),
]
zip_safe = False


'''
==============================================================================
ADDITIONAL DATA FILES
==============================================================================
'''

data_dirs = [
    'doc',
]


'''
==============================================================================
CUSTOM STEPS
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


def prepare_c_source(cmd):
    '''
    cmd-->str: command with arguments
    '''
    import setupext
    setupext.config['build_ext']['pre']['cmdlist'] = [cmd]
    return setupext.get_cmdclass()


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
    'package_dir', 'package_data',
    'zip_safe', 'classifiers', 'keywords',
    'long_description', 'url', 'download_url',
    'author', 'author_email', 'maintainer', 'maintainer_email',
]

kwdict = {}
for k in known_keywords:
    if k in locals():
        kwdict[k] = locals()[k]

if 'prep_cmd' in locals():
    kwdict['cmdclass'] = prepare_c_source(locals()['prep_cmd'])

# Do not compile ext_modules during build phase - wasteful
if len(sys.argv) > 1 and sys.argv[1] != 'build':
    if 'ext_modules' in locals():
        kwdict['ext_modules'] = [Extension(**x) for x in
                                 locals()['ext_modules']]

# Additional keywords specified by user - shouldn't be required, normally
kwdict.update(ADDL_KWARGS)
setup(**kwdict)
