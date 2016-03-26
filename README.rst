setupext
========

This module contains utility methods for easing writing python
installation scripts (setup.py):

Building C extensions: See setupext/doc/setup-sample.py

-  Specify location of C sources
-  Specify shared library name
-  Specify specific C source files to be compiled

Bundle additional files with package - using get\_dir\_tree()

-  Include and INSTALL C sources under python module directory
-  Include README, LICENSE ando ther files under python module directory

Add a LIST of shell commands or python callables to execute at different
stages of installation:

-  build
-  build\_clib
-  build\_ext
-  build\_py
-  build\_scripts
-  install\_data
-  install\_lib
-  install\_headers

| By setting values in setupext.config, a LIST of shell commands and/or
python code (callables) can be run before or after each ofthese stages.
Note that you need to include this package within your package if you
want
| to use the trigger functionality.

To only use get\_dir\_tree(), just copy that function into your setup.py

ASSUMPTIONS AND PACKAGE LAYOUT
==============================

toplevel --> python package name

This setup.py assumes following layout.

This directory

::

    ├── setup.py - this file
    ├── setupext.py - required in this directory
    ├── LICENSE - typical for github etc but not required
    │       Hard-link to a file under data_dirX to keep at top level
    │       and also install the same file
    │
    ├── README.rst - typical for github etc but not requiredt
    │       Hard-link to a file under data_dirX to keep at top level
    │       and also install the same file
    │
    └── toplevel - python package name
        ├── toplevel.__init__.py
        ├── toplevel.module1.py
        ├── toplevel.module2py
        │
        ├── subpkg1
        │   ├── subpkg1.module1.py
        │   ├── subpkg1.__init__.py
        │   └── subpkg1.module2.py
        │
        ├── data_dir1 - e.g. c_files
        │   ├── data_dir1_file1
        │   ├── data_dir1_file2
        │   └── data_dir1_file3
        │
        └── data_dir2 - e.g. doc
            ├── data_dir2_file1 - e.g. LICENSE
            └── data_dir2_file2 - e.g. README.rst

| If your layout is different, you may need to make changes to the
following:
|  - Under PACKAGE DATA:
|  - Set toplevel to module (dir) under which:
|  - C Extension shared lib if any will be installed
|  - Additional data if any (data\_dirs) will be installed
|  - Setting packages

::

    - Under ADDITIONAL keyword args to setup()
        - Add py_modules=[] to ADDL_KWARGS

    - Under C EXTENSION DETAILS - IFF your package includes a C extension:
        - Setting libpath
        - Setting c_src_list
        - Setting ext_modules

C EXTENSION DETAILS
===================

Put the C files in a dir under toplevel so that the C files can also be
installed using data\_dirs (see ADDITIONAL DATA FILES)

| For simple cases with a single extension, you should only need to set:
|  c\_dir-->str: directory
|  libname-->str: shared library filename without '.so'
|  c\_src\_files-->list of str: C source filenames within c\_dir

ADDITIONAL DATA FILES
=====================

| I use package\_dir and package\_data to specify installing additional
files that are:
|  - Files in directories under toplevel
|  - Wouldn't be AUTOMATICALLY included or installed because of:
|  - py\_modules directive
|  - packages=find\_packages() directive
|  - C source required for an extension
| Examples:
|  - Ship and INSTALL C source under the module directory
|  - Ship and INSTALL any other files - e.g:
|  - Documentation
|  - LICENSE

| With this method, we get following features:
|  - Do NOT require MANIFEST.in
|  - Do NOT require include\_package\_data directive
|  - No code required in setupext.CustomInstallData class

| Preparatory steps:
|  - If package includes a C-source extension:
|  - Put C source in a dir under toplevel
|  - Set c\_dir above to the name of the dir UNDER toplevel

::

    - Create other directories with data under toplevel

    - If you want files in TOP-LEVEL (above toplevel) included,
      HARD LINK those FILES to directories under toplevel - e.g.:
          - LICENSE
          - README.rst
      Alternatively, hard-link these files FROM the directory under
      toplevel to the top-level
      so that these files can be visible at top level (e.g. in github)

    - set data_dirs to LIST of directories under toplevel that
        you want to include

CUSTOM STEPS
============

To add a LIST of shell commands or python callables to execute at
different steps during installation, modify setupext.config as follows:

::

    - setupext.config is a DICT with keys representing installation steps
    - The steps supported are in setupext.known_steps (list of str)
    - Each element of setupext.config is itself a DICT with following keys:
        - 'pre': dict
        - 'post': dict

        'pre' and 'post' dicts can optionally contain the following keys:
            cmdlist-->list
                each element must be one of:
                    str: A shell command to execute with subprocess.call
                        The command is executed with shell=True
                        No additional cmdline parameters are added
                    callable: Will be called with following parameters
                        args=(caller): caller is instance of calling class
                            Typically instance of distutils.cmd.Command
                        pre_post=x: x in ['pre', 'post']
                        callable can retrieve step name using
                            args[0].get_command_name()
                if cmdlist is not set or is [] or None, the corresponding
                    pre / post dict is ignored

                see pydoc setupext.run_in_order

            show_output-->boolean: Display stdout of shell commands
                ignored for callables
                Default: true

            show_err-->boolean: Display stderr of shell commands (on stderr)
                ignored for callables
                Default: true

            ignore_err-->boolean: Continue to next element of cmdlist if
                shell command or callable raises an exception or
                shell command returns a non-zero return code

                Default is stop processing cmdlist (False)

            show_output, show_err and ignore_err apply to ALL elements
                of cmdlist

        cmdlist under 'pre' key is executed BEFORE the corresponding
            installation step

        cmdlist under 'post' key is executed AFTER the corresponding
            installation step

        callables must be defined at time of executing setup.py

        Note that cmdlist will be executed ONLY IF corresponding
        step is executed - e.g.:
            - if byte-compiling is disabled, install_lib won't run
            - If package doesn't define a C extension, build_ext  won't run

EXAMPLE:
========

| Assume you want to do the following:
|  - Run shell\_command\_1 and callable\_1 BEFORE
|  installation build (step: build) begins
|  - Ignore and hide errors running command at build.pre step
|  but show outputs
|  - Run shell\_command\_2 after build\_ext step is completed

Steps:
------

.. code:: python

    # Set to True to get DEBUG on stderr when each step is called
    # Debug messages will appear even if you do not setup custom commands
    # to execute for the step
    setupext.trace_triggers = False

    # Set shell_command_1, shell_command_2
    # shell_command_1 Will return a non-zero return code
    shell_command_1 = 'echo "Starting build"; uname --nosuchoption'
    shell_command_2 = 'echo "build_ext completed"'

    # define a callable
    def mycallable(*args, **kwargs):
        sys.stderr.write('%s %s\n' % (
            args[0].get_command_name(),
            kwargs.get('pre_post', 'Unknown')
        ))

    # Now setup setupext.config
    setupext.config['build']['pre']['cmdlist'] = [shell_command_1, mycallable]
    setupext.config['build']['post']['ignore_err'] = True
    setupext.config['build']['post']['show_err'] = False
    # shell_command_1 will produce stderr output and return non-zero code
    # but stderr will be suppressed and mycallable will still be executed

    setupext.config['build_ext']['post']['cmdlist'] = [shell_command_2]
    # stderr if any from shell_command_2 will be shown (on stderr)

