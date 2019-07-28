from esky import bdist_esky
from distutils.core import setup
from esky.bdist_esky import Executable
from glob import glob


setup(
    name='xcalcs',
    version='0.2.0',
    description='Calculadora RPN',
    scripts=[
        Executable('xcalcs.py', icon='ui/exeicon.ico', gui_only=True),
        # Executable('console.py', icon='ui/exeicon.ico', gui_only=True),
        ],
    options={
        'build_exe': {
            'packages': [],
            'excludes': [],
            'include_msvcr': False,
            },
        'bdist_esky': {
            'freezer_module': 'cx_Freeze',
            'excludes': ['PySide.QtNetwork', 'email', 'lib2to3', 'PySide.imageformats'],
            'includes': ['solver_tab', 'solver_lex'],
            # 'freezer_options': { 'zipIncludes': ['solver_tab.py', 'solver_lex.py']}
            },
        },
    data_files=[
        ('i18n', glob('.\\i18n\\*.qm')),
        # ('', ['xcalcs.cfg']),
        ],
    )
