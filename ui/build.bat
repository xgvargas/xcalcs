for %%r in (*.ui) do pyside-uic %%r -o ..\%%~nr_ui.py
rem c:\Python27\Lib\site-packages\PySide\pyside-rcc xcalcs.qrc -o ..\xcalcs\xcalcs_rc.py
