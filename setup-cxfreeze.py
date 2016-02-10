import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="XcalxS",
    version="0.1.0",
    description="RPN Calculator",
    options={
        "build_exe": {
            "include_msvcr": False,
            "optimize": 2,
            "packages": [],
            "includes": ['atexit', 'solver_tab', 'solver_lex'],
            "excludes": ["email", 'PySide.QtNetwork'],
            "bin_path_includes": [],
            "bin_path_excludes": [],
            "bin_includes": [],
            "bin_excludes": ['imageformats/*.dll'],
            "include_files": [],
            },
        },
    executables=[
        Executable("xcalcs.py", base=base),
        Executable("console.py", base=base)
        ],
    )
