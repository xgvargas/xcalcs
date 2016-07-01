from pathlib import Path


UIC = 'D:/Projetos/xcalcs/venv/Scripts/pyside-uic'
RCC = 'D:/Projetos/xcalcs/venv/Lib/site-packages/PySide/pyside-rcc'

DOIT_CONFIG = {
    'backend': 'json',
    'dep_file': 'doit-db.json',
}


def task_ui():
    for ui_file in Path('ui').glob('*.ui'):
        out_file = Path('.') / '{}_ui.py'.format(ui_file.stem)
        yield {
            'name': out_file.name,
            'actions': [[UIC, '-o', str(out_file), str(ui_file)]],
            'file_dep': [str(ui_file)],
            'targets': [str(out_file)],
        }

def task_rc():
    for rc_file in Path('ui').glob('*.qrc'):
        out_file = Path('.') / '{}_rc.py'.format(rc_file.stem)
        yield {
            'name': out_file.name,
            'actions': [[RCC, '-py3', '-o', str(out_file), str(rc_file)]],
            'file_dep': [str(rc_file)],
            'targets': [str(out_file)],
        }

# 	$(NIX)\bash.exe d:\bin\svg-extract.sh -f -o ui -s $@ $<

# def task_svg():
#     for svg_file in Path('ui').glob('*.svg'):
#         out_file = Path('.') / '{}.extracted'.format(svg_file.stem)
#         yield {
#             'name': out_file.name,
#             'actions': [[RCC, '-py3', '-o', str(out_file), str(svg_file)]],
#             'file_dep': [str(svg_file)],
#             'targets': [str(out_file)],
#         }
