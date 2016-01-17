from esky import bdist_esky
from distutils.core import setup
from esky.bdist_esky import Executable
from glob import glob


# executables = [Executable('xcalcs.py', icon='spam.ico', gui_only=True)]
executables = [Executable('xcalcs.py', gui_only=True)]

setup(name='xcalcs',
        version='0.1.0',
        description='Calculador RPN',
        scripts = executables,
        options={
            'build_exe': {
                'packages': [],
                'excludes': [],
                'include_msvcr': False,
                },
            'bdist_esky': {
                'freezer_module': 'cx_Freeze',
                # 'excludes': ['tkinter', 'sys'],
                'includes': ['solver_tab', 'solver_lex'],
                # 'freezer_options': { 'zipIncludes': ['solver_tab.py', 'solver_lex.py']}
                },
            },
        data_files=[
            ('i18n', glob(r'.\i18n\*.qm')),
            # ('', ['MyApp.xib']),
            # ('files', ['file1', 'file2']),
            # ('img', glob(r'.\img\*.*'))
            ],
        )
