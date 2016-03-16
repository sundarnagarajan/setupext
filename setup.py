import sys
import os
from setuptools import setup, find_packages


os.chdir(os.path.dirname(sys.argv[0]) or ".")

'''
==============================================================================
PACKAGE DATA
==============================================================================
'''
# You _SHOULD_ set these
toplevel = 'setupext'
version = '0.23-1'
description = toplevel
install_requires = [
]
packages = find_packages()
license = (
    'License :: OSI Approved :: '
    'GNU Lesser General Public License v3 or later (LGPLv3+)'
)

# The following are optional
long_description = open('README.txt').read()
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
    include_package_data=True,
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

# More optional keywords, but which are added conditionally
ext_modules = globals().get('ext_modules', [])
if ext_modules:
    kwdict['ext_modules'] = ext_modules

setup(**kwdict)
