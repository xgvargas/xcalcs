#--------------------------------------------------------------------------
#
#    Makefile for PySide
#
#--------------------------------------------------------------------------

ifdef VIRTUAL_ENV
  UIC = $(VIRTUAL_ENV)/Scripts/pyside-uic
  RCC = $(VIRTUAL_ENV)/Lib/site-packages/PySide/pyside-rcc -py3
  LUP = $(VIRTUAL_ENV)/Lib/site-packages/PySide/pyside-lupdate
  LRL = $(VIRTUAL_ENV)/Lib/site-packages/PySide/lrelease
else
  UIC = c:/Python27/scripts/pyside-uic
  RCC = c:/Python27/Lib/site-packages/PySide/pyside-rcc
  LUP = c:/Python27/Lib/site-packages/PySide/lupdate
  LRL = c:/Python27/Lib/site-packages/PySide/lrelease
endif

VPATH = ui/

UI_FILES          = $(patsubst ui/%.ui,   %_ui.py,        $(wildcard ui/*.ui))
RESOURCE_FILES    = $(patsubst ui/%.qrc,  %_rc.py,        $(wildcard ui/*.qrc))
IMAGE_FILES       = $(patsubst ui/%.svg,  ui/%.extracted, $(wildcard ui/*.svg))
TRANSLATION_FILES = $(patsubst i18n/%.ts, i18n/%.qm,      $(wildcard i18n/*.ts))

ifneq ("$(wildcard ui/icon.svg)","")
  EXTRA_TARGET = ui/exeicon.ico
else
  EXTRA_TARGET =
endif

default: $(UI_FILES) $(RESOURCE_FILES) $(TRANSLATION_FILES) $(EXTRA_TARGET)

.SECONDARY: $(IMAGE_FILES)

%.extracted : %.svg
	bash d:/bin/svg-extract.sh -f -o ui -s $@ $<

%_rc.py : %.qrc $(IMAGE_FILES)
	$(RCC) -o $@ $<

%_ui.py : %.ui
	$(UIC) -o $@ $<

%.qm : %.ts
	$(LRL) $< -qm $@

ui/exeicon.ico : ui/icon.extracted
#	echo -e "from PIL import Image\nImage.open('ui/icon256.png').save('ui/exeicon.ico', sizes=[(16,16), (32, 32), (48, 48)])" | c:/python27/python
	echo -e "from PIL import Image\nImage.open('ui/icon256.png').save('ui/exeicon.ico')" | c:/python27/python

%.lnk : %.ico
	set TARGET='d:/projetos/xcalcs/venv/scripts/pythonw.exe'
	set SHORTCUT='test1.lnk'
	set WORK='d:/projetos/xcalcs'
	set ICON='d:/projetos/xcalcs/ui/exeicon.ico'
	set ARGUMENTS='xcalcs.py'
	set PWS=powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile

	%PWS% -Command "$ws=New-Object -ComObject WScript.Shell; $s=$ws.CreateShortcut(%SHORTCUT%); $s.TargetPath=%TARGET%; $s.WorkingDirectory=%WORK%; $s.IconLocation=%ICON%; $s.Arguments=%ARGUMENTS%; $s.Save()"

clean:
	-rm *_ui.py *_rc.py *.pyc *_lex.py *_tab.py stack.dat
	-rm i18n/*.qm
	-rm -r __pycache__
	-cat ui/*.extracted | xargs rm.exe
	-rm ui/*.extracted ui/exeicon.ico

.PHONY: images dist update

images: $(IMAGE_FILES)

dist:
# versao usando o Esky
	-rm -r dist
	python setup-esky.py bdist_esky
	"c:/Program Files/7-Zip/7z.exe" x -odist/pack dist/*.zip
	"$(ProgramFilesX86)/Inno Setup 5/ISCC.exe" setup.iss

# versao do cx-freeze
# .............

update:
	$(LUP) -verbose -noobsolete $(wildcard i18n/*.pro)
